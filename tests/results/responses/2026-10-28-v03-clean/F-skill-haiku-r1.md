---
scenario: F
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

FACTS:
- `update_user()` uses `data.get('bio')` with no default, which returns `None` when 'bio' is absent from the request
- The test case confirms: PATCH `{"name": "Ada L."}` (no 'bio' key) results in `bio=None`
- The admin path correctly distinguishes omitted vs. explicit-null using `if 'bio' in data`
- The contract requires: omitted fields unchanged, explicit `null` clears the field

INFERENCES:
- `data.get('bio')` treats omitted and explicit-null identically (both return None)
- The fix is to use the same default pattern as the name field

Conclusion: VERIFIED

**The fix:**

```python
def update_user(user, data):
    user.name = data.get('name', user.name)
    user.bio = data.get('bio', user.bio)
    return user
```

Change line 2: add `user.bio` as the default, so omitted 'bio' preserves the existing value.

**How to verify:**

1. **Omitted field test** (the reported bug):
   ```
   Before: name="Ada", bio="Writes compiler tools"
   PATCH: {"name": "Ada L."}
   After: name="Ada L.", bio="Writes compiler tools" ✓
   ```

2. **Explicit null test** (contract requirement):
   ```
   Before: name="Ada", bio="Writes compiler tools"
   PATCH: {"name": "Ada L.", "bio": null}
   After: name="Ada L.", bio=None ✓
   ```

3. **Explicit value test**:
   ```
   Before: name="Ada", bio="Writes compiler tools"
   PATCH: {"name": "Ada L.", "bio": "New bio"}
   After: name="Ada L.", bio="New bio" ✓
   ```
