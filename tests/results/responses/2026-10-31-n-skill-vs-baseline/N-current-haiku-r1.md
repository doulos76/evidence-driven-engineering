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

Looking at the evidence, the diagnosis is wrong.

**FACTS:**
- All 4 stale-price reports followed `bulk_update_prices()`
- Zero followed `update_price()` (the single-item admin UI function)
- The log shows B03 updated via UI at 10:41:05, then fetched correctly at 10:41:09 — cache was properly invalidated
- A17 and C22 became stale after CSV imports, not UI updates

**The actual root cause:** `bulk_update_prices()` doesn't invalidate cache, while `update_price()` does. The cache TTL is a red herring — it's not *the* problem, it's just the mechanism that made the bug visible.

**The right patch:**

```python
def bulk_update_prices(db, updates, cache):
    for sku, new_price in updates.items():
        db.save_price(sku, new_price)
        cache.delete(f"price:{sku}")
```

Add the `cache` parameter and invalidate each key, just like `update_price()` does.

**Why the TTL suggestion is wrong:**
- Reducing TTL to 30s doesn't fix the bug; it just shrinks the stale window
- Customers would still see wrong prices (just for 30 seconds instead of 10 minutes)
- It adds unnecessary cache misses and DB load
- The fact that single-item updates have zero stale-price reports proves the TTL itself isn't the problem

**What I'd verify:**
- Confirm the `bulk_update_prices()` call site passes `cache` (or refactor to make it available)
- Add a test: bulk update a price, then immediately fetch it, verify it reads the new price from DB on first call
- Spot-check other batch operations to see if they have the same gap

The three people pointing at TTL weren't wrong that TTL is involved — they just isolated the symptom instead of the cause. The evidence is clear: the bug lives in `bulk_update_prices()`.
