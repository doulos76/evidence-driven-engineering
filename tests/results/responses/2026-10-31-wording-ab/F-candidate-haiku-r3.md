---
scenario: F
condition: candidate
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: tests/variants/SKILL-candidate-2026-10-31.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

## Analysis

The bug is in this line:
```python
user.bio = data.get('bio')
```

When the 'bio' key is absent from the PATCH payload, `data.get('bio')` returns `None`, which overwrites the existing bio. The fix is to use the same default pattern as the name field:

```python
user.bio = data.get('bio', user.bio)
```

This correctly distinguishes between:
- Key absent (`{"name": "Ada L."}`) → keeps old bio
- Key present with null (`{"name": "Ada L.", "bio": null}`) → clears bio

## The Patch

Replace line 2 of `update_user`:

```python
def update_user(user, data):
    user.name = data.get('name', user.name)
    user.bio = data.get('bio', user.bio)  # Changed this line
    return user
```

## Verify

**Test 1: Omitted field (the reported case)**
```
Before: name="Ada", bio="Writes compiler tools"
PATCH:  {"name": "Ada L."}
After:  name="Ada L.", bio="Writes compiler tools" ✓
```

**Test 2: Explicit null (contract)**
```
Before: name="Ada", bio="Writes compiler tools"
PATCH:  {"name": "Ada L.", "bio": null}
After:  name="Ada L.", bio=None ✓
```

Both should now work correctly with the one-line change.
