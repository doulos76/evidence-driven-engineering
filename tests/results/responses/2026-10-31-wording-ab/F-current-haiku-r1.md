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

I can see the bug clearly. In `update_user`, the line `user.bio = data.get('bio')` returns `None` when `'bio'` is absent from the request, silently overwriting the existing biography. The `updateUserForAdmin` function already shows the correct pattern.

**The minimal fix:**

```python
def update_user(user, data):
    user.name = data.get('name', user.name)
    if 'bio' in data:
        user.bio = data['bio']
    return user
```

**How to verify it:**

1. **Reproduction test** — confirm the bug exists:
   ```python
   user = User(name="Ada", bio="Writes compiler tools")
   update_user(user, {"name": "Ada L."})
   assert user.bio == "Writes compiler tools"  # fails before fix, passes after
   ```

2. **Contract tests** — verify both cases:
   ```python
   # Case 1: omitted bio is unchanged
   user = User(name="Ada", bio="Original")
   update_user(user, {"name": "Ada L."})
   assert user.name == "Ada L." and user.bio == "Original"
   
   # Case 2: explicit bio=null clears it
   user = User(name="Ada", bio="Original")
   update_user(user, {"name": "Ada L.", "bio": None})
   assert user.name == "Ada L." and user.bio is None
   ```

The fix applies the same defensive check already present in `updateUserForAdmin` (the `if 'bio' in data` guard), ensuring fields are only updated when explicitly provided.
