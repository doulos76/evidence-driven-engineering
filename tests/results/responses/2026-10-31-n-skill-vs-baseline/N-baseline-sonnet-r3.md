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

The TTL isn't the root cause. `bulk_update_prices` writes to the DB and never invalidates the cache, and the evidence points there.

- **All 4 stale reports followed a CSV import, and none followed the admin UI.** `update_price` deletes the key. `bulk_update_prices` doesn't.
- **A shorter TTL wouldn't have prevented the sampled reports.** The stale hits were at age 29s and 27s, which are inside a 30s TTL. Cutting to 30s would still serve those wrong prices, and it would add DB load for every SKU all the time.
- **The B03 line confirms the UI path works.** Four seconds after the update, it was a cache miss and returned the correct price.

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
     for sku, new_price in updates.items():
         db.save_price(sku, new_price)
+        # Invalidate per SKU right after its write, so a failure partway
+        # through the import can't leave already-saved SKUs stale.
+        cache.delete(_key(sku))
```

The TTL stays at 600s. It's a backstop, not the consistency mechanism.

## Supporting work

1. **Update callers.** The signature gained `cache`. I can't see the CSV import code, so grep for `bulk_update_prices(` and fix each call site. A missed one fails loudly with a `TypeError`, which is better than silently staying stale.
2. **Add a regression test.** Warm the cache for a SKU, call `bulk_update_prices` with a new price, then assert `get_price` returns the new price. Run the same test against `update_price` so the two paths can't diverge again.
3. **Verify after deploy.** Check that stale-price reports stop after the next CSV import. Entries cached before the deploy expire within 10 minutes, so no manual flush is needed.
4. **Correct the postmortem and ticket.** The "TTL too long" root cause should become "bulk update path didn't invalidate the cache", with the log excerpt as evidence. Otherwise the action item "reduce TTL" will get done, the bug will persist, and the team will conclude the fix wasn't aggressive enough.
5. **Known remaining gap (not fixed here).** There's a small race in `get_price`: a reader can fetch the old DB value, the writer saves and deletes, then the reader sets the old value into the cache. That would be stale for up to the TTL. It's rare and unrelated to these reports, and the TTL bounds it. If it ever matters, the usual fixes are versioned keys or a short TTL on a write-through path.

For the tech lead: a 30s TTL is a cost trade-off, not a fix. If a lower TTL is wanted for other reasons, it can be decided separately.
