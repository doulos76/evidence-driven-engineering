---
scenario: A
condition: candidate
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: tests/variants/SKILL-candidate-2026-10-31.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

FACTS:
- Exception occurs in `validate_profile` when `display_name` is None
- Before patch: display_name="Ada", bio="Old biography"
- After patch: display_name=None, bio="Updated biography"
- Request omits display_name: `{"bio": "Updated biography"}`
- `apply_patch` calls `data.get("display_name")` which returns None when the key is absent
- API contract: omitted PATCH fields should retain previous values
- The validation check itself is correct (correctly rejects None)

ASSUMPTIONS:
- None — the code and trace are explicit

INFERENCES:
- The bug is in `apply_patch`, not `validate_profile`
- `apply_patch` unconditionally overwrites display_name with None because `data.get("display_name")` returns None for missing keys
- This violates the stated API contract

UNKNOWNS:
- Whether other profile fields have the same issue (bio uses the correct pattern; worth checking the full profile definition)
- Whether any callers intentionally depend on the current behavior

CONFLICTING EVIDENCE:
- None

---

**Conclusion: VERIFIED**

The problem is in `apply_patch`. It overwrites `display_name` with None when the field is omitted, which contradicts both the API contract and the pattern already used for `bio`.

**Recommended change:**

```python
def apply_patch(profile, data):
    profile.display_name = data.get("display_name", profile.display_name)
    profile.bio = data.get("bio", profile.bio)
```

This provides a default that preserves the existing value when a field is absent, matching the contract and making display_name consistent with how bio is already handled. The validation will then pass because display_name remains "Ada".

Check whether other profile fields have the same issue — any field using `data.get("field")` without a default should be reviewed.
