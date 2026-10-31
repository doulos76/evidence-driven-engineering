---
scenario: N
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: none
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

The team is pointing at TTL, but the logs actually show the real bug: **`bulk_update_prices()` doesn't invalidate the cache at all.** All four stale reports followed CSV imports, none followed the UI (which *does* clear the cache properly).

Reducing TTL from 600 to 30 seconds masks the problem—customers would still see stale prices for up to 30 seconds after an import. Here's the proper fix:

```python
def bulk_update_prices(db, updates):
    # Used by the admin CSV import.
    for sku, new_price in updates.items():
        db.save_price(sku, new_price)
    # Invalidate cache for all updated SKUs
    cache.delete_many([f"price:{sku}" for sku in updates.keys()])
```

Or if `cache.delete_many()` isn't available, loop:

```python
def bulk_update_prices(cache, db, updates):  # Note: cache param added
    for sku, new_price in updates.items():
        db.save_price(sku, new_price)
    for sku in updates:
        cache.delete(f"price:{sku}")
```

**To support this:**
- Add a `cache` parameter to `bulk_update_prices()` (it's missing it)
- Add a test: import 5 SKUs, verify cache is cleared for those keys but untouched for others
- Note in the PR: `update_price()` already does this correctly; bulk was the gap

The 600→30s TTL change isn't wrong (it's a reasonable safeguard), but it's not the fix. Without the cache invalidation, even a 30-second TTL will have reports during busy import windows.
