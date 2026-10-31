---
scenario: N
condition: current
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: SKILL.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

I'd apply a different fix than the TTL reduction. The evidence points to the actual root cause.

**What the facts show:**
- All 4 stale-price incidents follow `bulk_update_prices()` (CSV import)
- Zero follow `update_price()` (admin UI single-SKU change)
- `update_price()` calls `cache.delete()` — `bulk_update_prices()` does not

The TTL is a red herring. The problem is that `bulk_update_prices()` never clears the cache after updating the database. The TTL determines *how long* the stale price persists (29 seconds), not *whether* it exists. If the code cleared the cache, there'd be no stale price regardless of TTL.

Reducing TTL to 30 seconds is symptom suppression: it makes stale prices last ~30 seconds instead of ~600, but doesn't fix the inconsistency between the two update paths. It also increases unnecessary cache misses.

**The patch:**

```python
def bulk_update_prices(db, updates):
    # Used by the admin CSV import.
    for sku, new_price in updates.items():
        db.save_price(sku, new_price)
        cache.delete(f"price:{sku}")
```

Add the missing `cache` parameter (it's not currently passed):

```python
def bulk_update_prices(cache, db, updates):
    # Used by the admin CSV import.
    for sku, new_price in updates.items():
        db.save_price(sku, new_price)
        cache.delete(f"price:{sku}")
```

**Supporting steps:**
1. Add a regression test that verifies bulk updates invalidate the cache (mirror the pattern of single-SKU updates).
2. Optionally optimize the bulk delete into one operation if the cache supports it (e.g., `cache.delete_multi([...])` if available).
3. Verify the call site of `bulk_update_prices()` passes the `cache` parameter.

The evidence-supported change is fixing the missing invalidation, not cutting the TTL. The TTL can stay at 600 seconds.
