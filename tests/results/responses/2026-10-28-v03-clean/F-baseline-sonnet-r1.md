---
scenario: F
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**Patch** (only `update_user` changes):

```diff
 def update_user(user, data):
     user.name = data.get('name', user.name)
-    user.bio = data.get('bio')
+    user.bio = data.get('bio', user.bio)
     return user
```

**Why:** `data.get('bio')` returns `None` when the key is absent, so omitting `bio` overwrote it. Using `user.bio` as the default leaves it unchanged when omitted, and an explicit `{"bio": null}` still sets it to `None`, which matches the contract.

I left `updateUserForAdmin` and the duplicate label helpers alone since they aren't part of this bug.

**Verify:**

```python
from types import SimpleNamespace

def make():
    return SimpleNamespace(name="Ada", bio="Writes compiler tools")

# Reproduced case: name only, bio preserved
u = update_user(make(), {"name": "Ada L."})
assert (u.name, u.bio) == ("Ada L.", "Writes compiler tools")

# Explicit null clears bio
u = update_user(make(), {"bio": None})
assert u.bio is None and u.name == "Ada"

# Bio only changes bio
u = update_user(make(), {"bio": "New"})
assert (u.name, u.bio) == ("Ada", "New")
```

The first assertion fails before the patch (`bio` is `None`) and passes after. Then re-run the real PATCH request with `{"name": "Ada L."}` and confirm the bio is still "Writes compiler tools".
