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

The patch below fixes `bulk_update_prices`, and it leaves the TTL alone.

## Root cause

`bulk_update_prices` writes to the DB but never invalidates the cache. `update_price` does invalidate it. The log fits that explanation:

- All 4 stale reports followed a CSV import, and none followed the admin UI. After the UI edit, B03 was a cache miss and served the fresh price.
- A17 was served stale at cache age 29s. A 30s TTL would not have prevented that, and neither would any other TTL. Shortening it only shrinks the window. Every bulk update would still leave stale prices for up to the TTL.

The TTL claim has been repeated by three people and in a postmortem, but nobody has tested it against these logs, and the logs contradict it.

## Patch

```diff
--- a/prices.py
+++ b/prices.py
@@
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
+        # Invalidate even if the import fails midway: SKUs already
+        # saved must not keep serving cached old prices.
+        for sku in updates:
+            cache.delete(_key(sku))
```

Notes on the patch:
- **Signature change:** `bulk_update_prices` now takes `cache`. Update the CSV import caller, and grep for any others. A missed caller fails loudly with a `TypeError`, which is better than failing silently.
- **`finally`:** deleting keys that were never written is harmless. Skipping deletes for rows that were written is the bug.
- **Batching:** if the cache client has `delete_many`, use it instead of the loop. That matters for 400+ SKUs.

## Supporting steps

1. **Regression test**, which fails before the patch and passes after:
   ```python
   def test_bulk_update_invalidates_cache():
       cache, db = FakeCache(), FakeDB({"A17": 24.99})
       cache.set("price:A17", 19.99, ttl=600)
       bulk_update_prices(cache, db, {"A17": 24.99})
       assert get_price(cache, db, "A17") == 24.99
   ```
   Add a second test where `db.save_price` raises on the second SKU and the first SKU's key is still invalidated.
2. **Deploy:** nothing needs purging. Entries cached before the fix expire within 10 minutes. If a recent import is still fresh in people's minds, run a one-off `delete` of the affected SKUs.
3. **Race:** a storefront read between `save_price` and `delete` can re-cache the old value. That is a narrow window in both paths and is not what these logs show. If it shows up later, the fix is versioned keys or short-TTL negative caching, not a global TTL cut.
4. **Postmortem:** amend it. The root cause is a missing cache invalidation in the bulk path, and the action item "reduce TTL" should be dropped. Cutting the TTL to 30s would have cost roughly 20x more DB reads and still left stale prices after every import. Tell the product owner the TTL theory is disproven by the log evidence, so the ticket reflects the real cause.
5. **Follow-up:** route all price writes through one function, so a new write path can't skip invalidation again.
