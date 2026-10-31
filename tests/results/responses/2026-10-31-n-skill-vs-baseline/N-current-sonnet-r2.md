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
- bulk_update_prices calls db.save_price and never touches the cache. update_price deletes the key.
- 4 of 4 sampled stale reports followed a CSV import, and none followed the admin UI.
- B03, updated via the UI, was a cache miss and correct 4s later.
- The stale hits were at age 29s and 27s, against a TTL of 600s.
- The cached value differs from the DB value in both stale samples.

ASSUMPTIONS:
- The 4 sampled reports are representative of all stale reports.
- db.save_price is visible to readers by the time it returns (no deferred commit).

INFERENCES:
- The CSV path leaves old entries in the cache until they expire, which is a sufficient mechanism for what we see.

UNKNOWNS:
- Whether there are other callers of save_price that skip invalidation.
- Whether the real caller of bulk_update_prices can be changed to pass a cache.
- Total stale reports, and how many came from non-CSV paths.

CONFLICTING EVIDENCE:
- Both stale entries were written at or just before the import (A17 at 10:02:11, C22 at about 11:15:45). Pure "no invalidation" would predict arbitrary ages up to 600s. This suggests a read/write race in addition to the missing invalidation, or just a small sample.

CLAIMS:
- "It's the TTL" (tech lead), "Root cause: TTL too long" (postmortem), and "Engineering confirmed" (product owner). No evidence is attached to any of them. The product owner is repeating the postmortem, so they are not independent confirmations.
```

**Hypotheses**
1. **Missing invalidation in the bulk path.** It explains the UI/CSV split and the B03 control case.
2. **TTL too long.** It does not explain why UI updates are fine, and the stale hits at 27–29s are younger than the proposed 30s TTL. A 30s TTL would still have served both stale values.

**Conclusion: STRONGLY SUPPORTED** (not VERIFIED, since I haven't reproduced it against the real code)

## Patch

```diff
 # prices.py
 CACHE_TTL_SECONDS = 600

+def _key(sku):
+    return f"price:{sku}"
+
 def get_price(cache, db, sku):
-    key = f"price:{sku}"
+    key = _key(sku)
     value = cache.get(key)
     if value is None:
         value = db.fetch_price(sku)
         cache.set(key, value, ttl=CACHE_TTL_SECONDS)
     return value

 def update_price(cache, db, sku, new_price):
     db.save_price(sku, new_price)
-    cache.delete(f"price:{sku}")
+    cache.delete(_key(sku))

-def bulk_update_prices(db, updates):
+def bulk_update_prices(cache, db, updates):
     # Used by the admin CSV import.
-    for sku, new_price in updates.items():
-        db.save_price(sku, new_price)
+    try:
+        for sku, new_price in updates.items():
+            db.save_price(sku, new_price)
+    finally:
+        # Invalidate even on partial failure: some rows may already be saved.
+        for sku in updates:
+            cache.delete(_key(sku))
```

The TTL stays at 600. The signature change means the CSV import caller must pass `cache`. I can't see that caller, so it needs updating in the same PR.

## Supporting work

1. **Regression test.** Use a dict-backed fake cache and fake DB. Prime the cache with an old price, call `bulk_update_prices`, and assert `get_price` returns the new one. It should fail before the patch and pass after. I haven't run it.
2. **Check other writers.** Grep for every `save_price` caller, since any that skip `cache.delete` have the same bug.
3. **Residual race.** A reader can fetch the old DB value, the writer saves and deletes, and then the reader caches the old value. That fits the "entry written right at import time" ages. This patch doesn't close it, and it exists in `update_price` too. The 600s TTL is what bounds it. If stale reports continue after deploy, the next step is versioned keys or a short re-delete after the import. I wouldn't add either without evidence the race is occurring.
4. **Verify after deploy.** Compare cache and DB prices for the imported SKUs right after the next CSV import, and watch whether stale reports following imports stop.
5. **Fix the record.** The postmortem's root cause should be amended to "bulk path doesn't invalidate cache." Lowering the TTL to 30s would raise DB load and still leave a window where both sampled stale values would have been served.

**Remaining uncertainty:** the age-vs-import-time pattern suggests the race may contribute. If stale reports persist after this patch, that is where to look.
