---
scenario: A
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

## FACTS:
- The request omits `display_name`; `data.get("display_name")` returns `None`
- `apply_patch` unconditionally assigns `profile.display_name = data.get("display_name")`, setting it to `None`
- `validate_profile` correctly rejects `None` for a required field
- The bio field in `apply_patch` uses the correct pattern: `data.get("bio", profile.bio)`
- The API contract requires omitted fields to retain their values

## ASSUMPTIONS:
- `display_name` is a required field in the profile schema

## INFERENCES:
- The validation is not broken; it's working correctly by rejecting invalid state
- The bug is in `apply_patch`: it violates the API contract for `display_name` by not providing a default value
- This only crashes on PATCH requests that omit `display_name`

## UNKNOWNS:
- Whether other fields have the same bug
- Why `display_name` and `bio` were handled inconsistently (likely an oversight)

---

## Conclusion: VERIFIED

The root cause is `apply_patch` line 2:
```python
profile.display_name = data.get("display_name")  # Returns None when omitted
```

This violates the API contract. The bio field on line 3 shows the correct pattern.

## Recommended Change

Replace that line to match the bio pattern:
```python
profile.display_name = data.get("display_name", profile.display_name)
```

This preserves the existing `display_name` when it's omitted from the patch, letting validation pass for valid prior state.
