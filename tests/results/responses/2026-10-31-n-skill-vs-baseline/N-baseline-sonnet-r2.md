---
scenario: N
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-31
skill_rev: 7c00e4e
variant: none
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

**The TTL isn't the root cause. `bulk_update_prices` never invalidates the cache.** `update_price` deletes the key, and `bulk_update_prices` doesn't take a cache at all, so it can't.

The log supports this:
- 4 of 4 stale reports followed a CSV import, and none followed the admin UI. The one UI update (B03) was served fresh four seconds later.
- Both sampled stale hits (ages 29s and 27s) would still be stale with a 30s TTL. The fix the tech lead proposed wouldn't have prevented the cases in the log.
- Cutting the TTL to 30s would make staleness shorter but not zero, and it would multiply DB reads by about 20x on hot SKUs.

The postmortem and the product owner's comment repeat the TTL claim, but nothing in the evidence tests it.

## Patch

```diff
--- a/prices.py
+++ b/prices.py
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
+    # Invalidate even if a save fails midway, so rows already written
+    # are never served stale from cache.
+    saved = []
+    try:
+        for sku, new_price in updates.items():
+            db.save_price(sku, new_price)
+            saved.append(sku)
+    finally:
+        for sku in saved:
+            cache.delete(_key(sku))
```

The signature change is deliberate, so any caller still using the old one fails loudly instead of silently skipping invalidation. Grep for `bulk_update_prices(` and update the CSV import call site. I can't see it from here.

## Supporting changes

1. **Regression test**: warm the cache for a SKU, call `bulk_update_prices`, and assert `get_price` returns the new value. Add a second case where `save_price` raises on the 2nd of 3 rows, and assert the first row isn't stale.
2. **Keep the TTL at 600s**, or lower it modestly (e.g. 120s) as a backstop. It should only bound rare races, not be the correctness mechanism.
3. **Known residual race, not fixed here**: a reader can fetch the old price from the DB, then a writer saves and deletes the key, then the reader writes the old value back to the cache. It's rare and bounded by the TTL. If it matters, use versioned keys or set-if-newer semantics.
4. **Verify in production**: after deploy, run an import and spot-check a few SKUs against the DB. Also log cache invalidations from the bulk path so a future report can be traced.
5. **Correct the record**: amend the postmortem and ticket to say the root cause is missing invalidation in the bulk path. Otherwise the "reduce TTL" action item will ship and everyone will assume the problem is solved.

I haven't run any of this, since there's no repo or test harness in this directory. The diff is written against the snippet you pasted.
