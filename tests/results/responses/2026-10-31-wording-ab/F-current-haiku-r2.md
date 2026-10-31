---
scenario: F
condition: current
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: SKILL.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

I can see the bug. In `update_user`, the line:

```python
user.bio = data.get('bio')
```

returns `None` when `'bio'` is absent from the payload, unconditionally clearing it. The fix is to preserve the current value when the field is omitted, matching the pattern already used for `name`:

```python
user.bio = data.get('bio', user.bio)
```

This handles both parts of the contract:
- Omitted fields stay unchanged: `data.get('bio', user.bio)` returns the current bio
- Explicit `bio: null` clears it: the payload contains `'bio': None`, which overwrites with `None`

**Verification:**

```python
# Test 1: Omitted field (the failing case)
user = type('User', (), {'name': 'Ada', 'bio': 'Writes compiler tools'})()
update_user(user, {'name': 'Ada L.'})
assert user.bio == 'Writes compiler tools', "FAILED: bio was cleared"

# Test 2: Explicit null should clear
user = type('User', (), {'name': 'Ada', 'bio': 'Writes compiler tools'})()
update_user(user, {'bio': None})
assert user.bio is None, "FAILED: bio was not cleared"

# Test 3: Both fields provided
user = type('User', (), {'name': 'Ada', 'bio': 'Writes compiler tools'})()
update_user(user, {'name': 'Ada L.', 'bio': 'New bio'})
assert user.bio == 'New bio', "FAILED: bio was not updated"
```

All three should pass after the fix. The one-character change (adding `, user.bio`) is minimal and preserves existing behavior for all cases except the buggy one.
