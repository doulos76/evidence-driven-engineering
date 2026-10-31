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

## Diagnosis

```
FACTS:
- bulk_update_prices(db, updates) calls db.save_price and never touches the cache. It doesn't even receive one.
- update_price deletes the cache key after saving.
- In the log, 4 of 4 sampled stale reports followed a CSV import, and none followed the admin UI.
- The UI case (B03) shows a cache miss 4s after the update, with the correct price.
- Stale hits had cache ages of 29s (A17) and 27s (C22), measured 29s and 22s after the imports.
ASSUMPTIONS:
- The storefront and admin share one cache backend.
- The CSV import calls bulk_update_prices, as the code comment says.
INFERENCES:
- The A17 and C22 entries were cached just before their imports (10:02:11 and ~11:15:45), so the import left them in place.
UNKNOWNS:
- How the 4 sampled reports were chosen ("sampled"), so there may be a selection bias.
- Whether stale reports exist after UI edits that weren't sampled.
- Whether the cache client has delete_many, and what the import's callers look like (not visible here).
CONFLICTING EVIDENCE:
- A 30s TTL doesn't explain the logs. Both stale hits were younger than 30s, so they would still be served stale.
CLAIMS:
- "Root cause: TTL too long" (tech lead, postmortem, product owner). Three people repeating it is not three pieces of evidence, and nothing in the logs shows the TTL as the cause.
```

**Hypotheses**
- **H1, TTL too long:** predicts staleness after both UI and CSV edits, with ages up to 600s. The logs show only CSV cases, and the stale ages are under 30s. Cutting the TTL to 30s would still have served both logged stale reads.
- **H2, bulk path never invalidates:** predicts staleness only after imports, for SKUs cached before the import. That matches every log line, including the clean UI case.

Conclusion: STRONGLY SUPPORTED

It is not VERIFIED because I haven't run a reproduction, and the sample is small and possibly biased. The regression test below is the cheapest direct check.

## Patch

```diff
--- a/prices.py
+++ b/prices.py
@@
-def bulk_update_prices(db, updates):
+def bulk_update_prices(cache, db, updates):
     # Used by the admin CSV import.
-    for sku, new_price in updates.items():
-        db.save_price(sku, new_price)
+    try:
+        for sku, new_price in updates.items():
+            db.save_price(sku, new_price)
+    finally:
+        # Invalidate after saving, even on partial failure, so rows already
+        # written are not hidden behind stale cache entries.
+        for sku in updates:
+            cache.delete(f"price:{sku}")
```

- **TTL:** I left it at 600. Changing it is unsupported by the evidence and would cost more DB load without fixing this bug.
- **Signature:** `cache` is now a required first argument, matching `update_price`. Any caller I can't see, such as the CSV import, will fail loudly instead of silently skipping invalidation. Update it in the same PR.
- **Cache calls:** I used per-key `delete` rather than assuming `delete_many` exists.

## Regression test

```python
class FakeCache:
    def __init__(self): self.d = {}
    def get(self, k): return self.d.get(k)
    def set(self, k, v, ttl=None): self.d[k] = v
    def delete(self, k): self.d.pop(k, None)

class FakeDB:
    def __init__(self, p): self.p = dict(p)
    def fetch_price(self, sku): return self.p[sku]
    def save_price(self, sku, v): self.p[sku] = v

def test_bulk_update_invalidates_cache():
    cache, db = FakeCache(), FakeDB({"A17": 19.99})
    assert get_price(cache, db, "A17") == 19.99   # warm the cache
    bulk_update_prices(cache, db, {"A17": 24.99})
    assert get_price(cache, db, "A17") == 24.99   # fails before the patch
```

Run it against the unpatched code first to confirm it fails. That turns the diagnosis into a demonstrated cause.

## Supporting steps

1. **Check the callers:** grep for every `bulk_update_prices` call site, and for any other `save_price` caller that skips invalidation.
2. **Check the logs after deploy:** stale reports after imports should stop. If any appear, H2 is incomplete.
3. **Look at unsampled reports:** if any follow UI edits, there's a second cause. One candidate is a read-through race in `get_price`/`update_price`. A reader can fetch the old DB value, the admin can save and delete, and then the reader can `set` the old value, which would then live for up to 600s. I haven't verified this and it isn't what the logs show, so I'm not patching it. If it shows up, the fix is versioned keys or a shorter TTL.
4. **Fix the record:** correct the postmortem and the ticket comment. They currently state an unverified cause as confirmed, and the action item (reduce TTL) wouldn't have prevented the logged incidents.

**Regression risk:** low. The change adds deletes after writes that already happen. The only side effect is extra cache misses for imported SKUs, which is the intended behavior.

**Remaining uncertainty:** sampling bias in the 4 reports, and the possible race above.
