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

**FACTS:**
- `update_user` calls `data.get('bio')` with no default value
- `data.get('bio')` returns `None` when 'bio' is absent from the PATCH payload
- This overwrites `user.bio` with `None`, clearing existing data
- The contract requires omitted fields to remain unchanged
- `updateUserForAdmin` uses the correct pattern: `if 'bio' in data:`

**The Bug:**
Line 2 of `update_user` has no default fallback, unlike line 1 which correctly uses `user.name` as default.

**Smallest Patch:**

```python
def update_user(user, data):
    user.name = data.get('name', user.name)
    user.bio = data.get('bio', user.bio)  # Add default: user.bio
    return user
```

**How to Verify:**

```python
# Setup
user = User(name="Ada", bio="Writes compiler tools")

# Test 1: Omitted bio should not change
update_user(user, {"name": "Ada L."})
assert user.name == "Ada L."
assert user.bio == "Writes compiler tools"  # ✓ unchanged

# Test 2: Explicit null should clear bio
update_user(user, {"name": "Ada L.", "bio": None})
assert user.bio is None  # ✓ cleared as intended
```

The fix mirrors the pattern already used for `name` and matches the existing `updateUserForAdmin` logic.
