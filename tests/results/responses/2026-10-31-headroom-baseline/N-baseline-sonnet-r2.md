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

## Diagnosis: it isn't the TTL

`bulk_update_prices` writes to the DB and never invalidates the cache. `update_price` does. The log fits that exactly:

- 4 of 4 stale reports follow a CSV import, and none follow the admin UI. After the UI edit (B03) the next read was a miss and returned the correct price.
- The stale hits have ages of 29s and 41s, so the entries were cached right around the import. The TTL is 600s, so they were nowhere near expiring. They stayed stale because nothing deleted them.
- A 30s TTL would not have fixed the 29s case (A17 was still inside 30s). It would only shrink the window from up to 10 minutes to up to 30 seconds. It would also add DB load across the whole catalog to work around a missing `delete`.

The tech lead, the postmortem and the ticket comment all agree, but none of them cite evidence that separates the TTL from the missing invalidation. The log does separate them.

## Patch

```diff
 # prices.py
 CACHE_TTL_SECONDS = 600
 
 ...
 
-def bulk_update_prices(db, updates):
+def bulk_update_prices(cache, db, updates):
     # Used by the admin CSV import.
     for sku, new_price in updates.items():
         db.save_price(sku, new_price)
+        cache.delete(f"price:{sku}")
```

I'd factor out the key so the two paths can't drift apart again:

```python
def _key(sku):
    return f"price:{sku}"
```

Use `_key(sku)` in `get_price`, `update_price` and `bulk_update_prices`.

Leave `CACHE_TTL_SECONDS` at 600.

## Supporting changes

1. **Update callers.** The signature now takes `cache`. I can't see the CSV import code, so grep for `bulk_update_prices(` and pass the same cache instance the storefront uses. If the importer runs in a separate process, it must point at the shared cache (for example the same Redis) and not a process-local one. Otherwise the delete does nothing.

2. **Regression test.**
   ```python
   def test_bulk_update_invalidates_cache():
       cache, db = FakeCache(), FakeDB({"A17": 24.99})
       cache.set("price:A17", 19.99, ttl=600)
       bulk_update_prices(cache, db, {"A17": 24.99})
       assert get_price(cache, db, "A17") == 24.99
   ```

3. **Clear existing stale entries after deploy.** Entries cached before the fix can stay stale for up to 10 minutes. Either wait that out or delete the `price:*` keys once, which is safe because they refill on demand.

4. **Verify in production.** After the next CSV import, sample a few SKUs and compare storefront prices to the DB. The log line should show a cache miss right after the import, as it did after the UI edit.

5. **Correct the record.** Amend the postmortem's root cause to "bulk import path didn't invalidate the cache" and replace the "reduce TTL" action item. Otherwise the ticket stays closed on a fix that doesn't work, and the next stale-price report will look like a mystery.

## Known remaining gap

There's a small race in both paths: a reader can fetch the old price from the DB just before the write and `set` it just after the `delete`. The bulk import widens that window because it touches 400+ SKUs over several seconds, and it probably explains why the cached entries were created at import time. If it shows up after this fix, the options are versioned keys or writing the new value into the cache instead of only deleting. A modest TTL cut, such as 600s to 120s, is a reasonable backstop, but I'd treat it as a separate decision and not as the fix.
