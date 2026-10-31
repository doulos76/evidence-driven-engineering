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

**The Bug:** Line 2 unconditionally sets `user.bio` to the result of `data.get('bio')`, which returns `None` when 'bio' is absent. This violates the contract: omitted fields should be unchanged.

**The Fix:**

```python
def update_user(user, data):
    user.name = data.get('name', user.name)
    if 'bio' in data:
        user.bio = data['bio']
    return user
```

This mirrors the correct logic already in `updateUserForAdmin`. Only set `bio` if it's explicitly provided in the payload.

**How to Verify:**

1. **Before the fix** — PATCH with `{"name": "Ada L."}` should fail:
   ```
   bio before: "Writes compiler tools"
   bio after: None  ← bug confirmed
   ```

2. **After the fix** — same PATCH should preserve bio:
   ```
   bio before: "Writes compiler tools"
   bio after: "Writes compiler tools"  ✓
   ```

3. **Verify the contract still works** — explicit `null` should clear it:
   ```
   PATCH {"name": "Ada L.", "bio": null}
   bio after: None  ✓
   ```
