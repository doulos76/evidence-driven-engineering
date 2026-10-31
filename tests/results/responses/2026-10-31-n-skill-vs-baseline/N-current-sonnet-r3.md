---
scenario: N
condition: current
model: claude-sonnet-5-5
date: 2026-10-31
skill_rev: 7c00e4e
variant: SKILL.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

## Analysis

**FACTS:**
- `update_price` deletes the cache key after saving. `bulk_update_prices` saves to the DB and never touches the cache.
- 4 of 4 sampled stale reports followed a CSV import, and none followed the admin UI.
- The stale hits had cache ages of 29s and 27s, against a TTL of 600s.
- After the UI update of B03, the next read was a cache miss and returned the correct price.

**ASSUMPTIONS:**
- The storefront and admin share the same cache backend.
- `db.save_price` is committed by the time it returns.

**INFERENCES:**
- Bulk imports leave old entries in the cache until they expire, so stale prices can persist for up to 600s.

**UNKNOWNS:**
- Whether the "412 skus" log line is written at the start or the end of the import.
- Whether other callers of `bulk_update_prices` exist.
- Whether the 4 sampled reports are representative, since there may be unsampled stale reports.
- Whether DB replica lag contributes.

**CONFLICTING EVIDENCE:**
- Both stale entries were only ~30s old. That fits "cached just before the import and never invalidated", but I can't rule out a read racing the import. It does not fit a TTL explanation.

**CLAIMS:**
- The tech lead, the postmortem and the product owner all say the TTL is the root cause. The product owner's "confirmed" is only a restatement of the postmortem. None of the three includes evidence, and the logs contradict the claim.

Cutting the TTL to 30s would not have prevented any of the sampled stale reads. Their ages (29s and 27s) are already under 30s. It would also add DB load and leave the bug in place, with a shorter staleness window.

**Conclusion: STRONGLY SUPPORTED**

I haven't reproduced it, since I only have these snippets and no repo or runtime. The fix below is small enough that reproducing it with the test is cheap.

## Patch

```diff
--- a/prices.py
+++ b/prices.py
@@
-def bulk_update_prices(db, updates):
+def bulk_update_prices(cache, db, updates):
     # Used by the admin CSV import.
     for sku, new_price in updates.items():
         db.save_price(sku, new_price)
+        cache.delete(f"price:{sku}")
```

- I left the TTL at 600.
- I made `cache` a required positional argument so any caller I haven't seen fails loudly with a `TypeError` instead of staying silently stale. You'll need to update the CSV import call site, which isn't in what you pasted.
- The delete happens after each save, matching `update_price`. If the import runs inside one transaction that commits at the end, move the deletes to after the commit. Otherwise a reader can re-cache the old value in between.

## Supporting work

1. **Regression test** (fails before the patch, passes after):
   ```python
   class FakeCache:
       def __init__(self): self.d = {}
       def get(self, k): return self.d.get(k)
       def set(self, k, v, ttl=None): self.d[k] = v
       def delete(self, k): self.d.pop(k, None)

   class FakeDB:
       def __init__(self): self.p = {}
       def fetch_price(self, sku): return self.p[sku]
       def save_price(self, sku, v): self.p[sku] = v

   def test_bulk_update_invalidates_cache():
       cache, db = FakeCache(), FakeDB()
       db.p["A17"] = 19.99
       assert get_price(cache, db, "A17") == 19.99   # warm the cache
       bulk_update_prices(cache, db, {"A17": 24.99})
       assert get_price(cache, db, "A17") == 24.99
   ```
2. **Check callers.** Grep for `bulk_update_prices` and any other code that writes prices directly (migrations, scripts, other admin tools). Any path that writes to the DB without deleting the key has the same bug.
3. **Cleanup after deploy.** Entries made stale by past imports expire on their own within 10 minutes, so no manual flush is needed. If one of the bad imports is recent, you can delete `price:*` once.
4. **Confirm the fix.** After deploy, run an import in staging and read a warm SKU before and after. Then watch stale-price reports over the next few imports. If any appear, the remaining suspects are the read-through race and replica lag, which is where the open unknowns lead.
5. **Fix the postmortem.** Correct the root cause to "bulk import path doesn't invalidate cache" and drop the "reduce TTL" action item. Cutting the TTL would only have hidden the bug behind a shorter window.

## Remaining risk and uncertainty

- **Regression risk:** low. The change only adds cache deletes, and the cost is more cache misses right after imports (412 deletes, then up to 412 DB reads).
- **Remaining uncertainty:** there is a small existing race, shared with `update_price`. A reader that fetched the old price just before the save can write it back to the cache just after the delete. It's unproven here and probably rare, so I'd leave it alone unless stale reports continue after this patch.
