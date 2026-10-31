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

Looking at the logs, I see a different root cause than what those three people identified. **Every stale-price report follows `bulk_update_prices`, and zero follow `update_price`** — which is the only function that clears the cache.

The bug: `bulk_update_prices` saves to the database but doesn't invalidate the cache. `update_price` (the single-SKU UI path) does clear it, so users never see stale prices from UI updates, only from CSV imports.

Reducing TTL would slow down the problem's manifestation, but wouldn't fix it.

Here's the patch I'd merge:

```python
def bulk_update_prices(db, updates):
    # Used by the admin CSV import.
    for sku, new_price in updates.items():
        db.save_price(sku, new_price)
        cache.delete(f"price:{sku}")  # Add this line
```

Or pass cache in and do it in a batch at the end (faster for 400+ SKUs):

```python
def bulk_update_prices(cache, db, updates):
    # Used by the admin CSV import.
    for sku, new_price in updates.items():
        db.save_price(sku, new_price)
    for sku in updates:
        cache.delete(f"price:{sku}")
```

**To support this**: Add a test that calls `bulk_update_prices`, then `get_price` immediately, and asserts the returned value matches what was written (not a stale cached value). The current test suite presumably didn't catch this because it never validated that bulk updates invalidate the cache.
