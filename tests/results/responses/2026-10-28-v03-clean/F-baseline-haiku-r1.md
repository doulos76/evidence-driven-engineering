---
scenario: F
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

The bug is in `update_user`: `data.get('bio')` returns `None` when 'bio' is absent from the payload, which clears the field instead of leaving it unchanged.

The fix matches the correct pattern already in `updateUserForAdmin`:

```python
def update_user(user, data):
    user.name = data.get('name', user.name)
    if 'bio' in data:
        user.bio = data['bio']
    return user
```

**Why:** `dict.get(key)` with no default returns `None`, so omitted fields get set to `None`. Checking `if 'bio' in data` distinguishes between "field absent" (leave unchanged) and "field present with any value, including `null`" (update it).

**To verify:**

```python
# Test: omitted field unchanged
user = type('User', (), {'name': 'Ada', 'bio': 'Writes compiler tools'})()
result = update_user(user, {'name': 'Ada L.'})
assert result.bio == 'Writes compiler tools', f"Got {result.bio}"
assert result.name == 'Ada L.'

# Test: explicit null clears bio
user = type('User', (), {'name': 'Ada', 'bio': 'Writes compiler tools'})()
result = update_user(user, {'name': 'Ada L.', 'bio': None})
assert result.bio is None
assert result.name == 'Ada L.'
```

Both assertions pass with the fix applied. The first fails with the original code (bio becomes `None` instead of staying as the original string).
