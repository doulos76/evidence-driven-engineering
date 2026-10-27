---
scenario: F
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**Cause:** `update_user` does `user.bio = data.get('bio')`. When `bio` is omitted from the payload, `.get` returns `None` and overwrites the stored value. An explicit `"bio": null` also yields `None`, so the contract's clear-on-null behavior already works and must stay.

Conclusion: VERIFIED (by reading the code against the reproduced case; I haven't executed it, since the file isn't in the working directory).

**Smallest patch**

```diff
 def update_user(user, data):
     user.name = data.get('name', user.name)
-    user.bio = data.get('bio')
+    if 'bio' in data:
+        user.bio = data['bio']
     return user
```

This uses the same `'bio' in data` idiom `updateUserForAdmin` already uses, so it matches the surrounding code.

**Verify**

```python
from types import SimpleNamespace

def make():
    return SimpleNamespace(name="Ada", bio="Writes compiler tools")

def test_name_only_keeps_bio():
    u = update_user(make(), {"name": "Ada L."})
    assert (u.name, u.bio) == ("Ada L.", "Writes compiler tools")  # the reported repro

def test_explicit_null_clears_bio():
    assert update_user(make(), {"bio": None}).bio is None

def test_bio_update():
    assert update_user(make(), {"bio": "New"}).bio == "New"
```

Before the patch, the first test fails with `bio=None`, which matches the report. After it, all three should pass. Also replay the original PATCH request end to end, since this only tests the function and not how the request handler builds `data`.

**Regression risk and uncertainty**
- Any caller that relied on omitted `bio` clearing it will change behavior. That contradicts the stated contract, but I haven't seen the callers.
- If the handler fills missing keys with `None` before calling `update_user`, the unit tests would pass but the request would still fail. Your repro suggests it doesn't, but the end-to-end replay is what confirms it.
- I deliberately left `updateUserForAdmin`, its TODO, and the duplicate label helpers untouched, as they're outside this bug.
