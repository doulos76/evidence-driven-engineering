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

The real issue isn't the TTL—it's that `bulk_update_prices()` never invalidates the cache. The logs confirm this: CSV imports (which skip cache deletion) cause stale data; UI updates (which call `cache.delete()`) don't.

Reducing TTL masks the bug but doesn't fix it. It also increases needless cache misses and DB load.

**The patch:**

```python
def bulk_update_prices(cache, db, updates):
    # Used by the admin CSV import.
    for sku, new_price in updates.items():
        db.save_price(sku, new_price)
        cache.delete(f"price:{sku}")
```

This mirrors `update_price()` and invalidates cache for each updated SKU immediately.

**To support this:**

- **Add a test** that bulk-updates a price and verifies the next `get_price()` sees the new value (not a cache hit from before the update). This catches the regression if someone later refactors.
- **Leave the TTL at 600s.** After the cache invalidation is in place, the TTL is just a safety net for rare cases (e.g., a batch job crashes mid-update). A 10-minute window is fine for that.
- **Document in the function docstring** that cache must be invalidated per-SKU, to prevent someone from later "optimizing" this with a bulk clear or by removing the loop.

The three people blaming TTL were working backwards from the symptom. The postmortem and ticket were right about the cause, but pinpointed the wrong lever.
