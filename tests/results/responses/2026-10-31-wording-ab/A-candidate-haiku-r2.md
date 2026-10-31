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

## FACTS:
- The crash occurs after `apply_patch()` sets `display_name=None` (visible in the "after apply_patch" output)
- The request omits the `display_name` field; only `bio` is provided
- Line 23: `profile.display_name = data.get("display_name")` — when the key is absent, `.get()` returns `None`
- The validation error is correct: `display_name=None` fails the non-empty-string check
- The API contract requires omitted PATCH fields to retain previous values

## ASSUMPTIONS:
- The API contract is authoritative
- No other part of the system intentionally relies on the current behavior

## INFERENCES:
- `validate_profile()` is working correctly — it's enforcing a real constraint
- The bug is in `apply_patch()`, which violates the API contract by assigning `None` instead of preserving the prior value

## UNKNOWNS:
- Whether other fields have the same issue
- Whether `display_name` can be explicitly set to null via a separate endpoint
- Full test coverage for patch behavior

## CONFLICTING EVIDENCE:
- None

---

**Conclusion: VERIFIED**

The trace directly shows display_name changed from "Ada" to None. Line 23 is the cause.

---

## Recommended Change

Fix line 23 to preserve the existing value when the field is omitted:

```python
profile.display_name = data.get("display_name", profile.display_name)
```

This matches the pattern already used for `bio` on line 24 and aligns `apply_patch()` with your API contract.

**Verification:** The same request will then leave `display_name="Ada"`, pass validation, and reach `repository.save()`.

**Regression risk:** Low. The fix corrects a contract violation. Watch for tests that verify the current (incorrect) behavior — they'll need updating.
