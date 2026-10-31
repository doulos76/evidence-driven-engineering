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

The TTL isn't the root cause, so I wouldn't merge the 30s change. `bulk_update_prices` writes to the DB but never invalidates the cache. `update_price` does, which is why the admin UI path never goes stale.

The logs back this up:
- All 4 sampled stale reports followed a CSV import, and none followed the admin UI.
- The stale hits had ages of 29s and 27s. A 30s TTL would still serve both, so the patch the tech lead wants wouldn't have fixed those reports.
- With the current 600s TTL, a bulk-updated SKU can stay stale for up to 10 minutes. A shorter TTL only shrinks that window and adds DB load.

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
+    saved = []
+    try:
+        for sku, new_price in updates.items():
+            db.save_price(sku, new_price)
+            saved.append(sku)
+    finally:
+        # Invalidate even on partial failure, so rows already written
+        # don't linger as stale cache entries.
+        for sku in saved:
+            cache.delete(f"price:{sku}")
```

I'd leave `CACHE_TTL_SECONDS = 600` alone. It's a reasonable backstop once invalidation is correct.

## Supporting steps

1. **Update callers.** The signature now takes `cache`. I can't see the repo, so grep for `bulk_update_prices(`, probably just the CSV import handler, and pass the cache in.
2. **Add a regression test.** Use a fake cache and DB. Prime the cache for a SKU, call `bulk_update_prices`, and assert `get_price` returns the new value. Add a second case where `save_price` raises midway, and assert the already-saved SKUs were evicted.
3. **Clear existing stale entries on deploy.** Entries cached before the fix can still be up to 10 minutes old, so they expire on their own. If you want it immediate, delete `price:*` once.
4. **Correct the record.** Amend the postmortem and the ticket. The root cause is a missing cache invalidation in the bulk path, and the "reduce TTL" action item should become "invalidate in `bulk_update_prices`". Otherwise people will keep citing it as confirmed.
5. **Optional: confirm in production.** Check that `get_price` hits for CSV-imported SKUs after an import show a cache age greater than the time since the import. That is the signature of this bug.

One known limitation: a reader that fetched the old price from the DB just before the save could write it back to the cache just after the delete. That window is tiny and bounded by the TTL, which is another reason to keep the TTL. If it matters, the fix is versioned keys or a write-through update, which is a separate change.
