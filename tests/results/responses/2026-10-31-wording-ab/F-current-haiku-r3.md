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

Looking at the code, I can identify the bug immediately:

**FACTS:**
- `update_user` line 2: `user.bio = data.get('bio')` returns `None` when `'bio'` is absent from the request
- This unconditionally overwrites the bio, even when it wasn't provided
- The admin path correctly uses `if 'bio' in data:` to only update when present

**The fix:** Apply the same conditional pattern to `update_user`:

```python
def update_user(user, data):
    user.name = data.get('name', user.name)
    if 'bio' in data:
        user.bio = data['bio']
    return user
```

**To verify**, test both cases:

```python
# Case 1: omitted field preserved
user = User(name="Ada", bio="Writes compiler tools")
update_user(user, {"name": "Ada L."})
assert user.name == "Ada L."
assert user.bio == "Writes compiler tools"  # unchanged

# Case 2: explicit null clears field
user = User(name="Ada", bio="Writes compiler tools")
update_user(user, {"name": "Ada L.", "bio": None})
assert user.name == "Ada L."
assert user.bio is None  # cleared
```

The issue: `data.get('bio')` without a default returns `None` for missing keys, so omitted fields get set to `None` instead of preserved. The conditional `if 'bio' in data:` distinguishes between "not provided" (skip it) and "provided as null" (clear it).
