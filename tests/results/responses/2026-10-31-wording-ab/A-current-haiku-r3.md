---
scenario: A
condition: current
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: SKILL.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

**FACTS:**
- The crash occurs in `validate_profile`, which correctly rejects a None `display_name`
- The request omits `display_name` (only contains `{"bio": "Updated biography"}`)
- Before `apply_patch`: `display_name="Ada"` (the existing value)
- After `apply_patch`: `display_name=None` (overwritten)
- The stated API contract: omitted PATCH fields retain their previous values

**ASSUMPTIONS:**
- None; the behavior is directly observable from the code

**INFERENCES:**
- `apply_patch` is the source of the problem: `data.get("display_name")` returns `None` when the key is absent, unconditionally overwriting the existing value
- The validation is working correctly—it properly rejects the invalid state that `apply_patch` created
- This violates the API contract

**UNKNOWNS:**
- Whether other fields have the same vulnerability (the pattern suggests `bio` does not, because it uses a fallback: `data.get("bio", profile.bio)`)
- Broader context around whether there are other callers or code paths

**Conclusion: VERIFIED**

---

## Diagnosis

The bug is in `apply_patch`, not `validate_profile`. The line:

```python
profile.display_name = data.get("display_name")
```

will set `display_name` to `None` when the key is absent from the request. This directly violates the API contract that omitted fields should retain their previous values.

## Recommended Change

Use a fallback for `display_name` consistent with the `bio` field:

```python
def apply_patch(profile, data):
    profile.display_name = data.get("display_name", profile.display_name)
    profile.bio = data.get("bio", profile.bio)
```

This ensures that when `display_name` is omitted, the existing value is preserved, and the subsequent validation will pass (assuming the original profile has a valid display_name).
