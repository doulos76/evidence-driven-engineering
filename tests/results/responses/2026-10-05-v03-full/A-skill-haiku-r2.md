---
scenario: A
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

FACTS:
- Exception raised from `validate_profile` on line 10, triggered by `display_name=None` after `apply_patch`
- Request body omits `display_name` entirely: `{"bio": "Updated biography"}`
- Before `apply_patch`: `display_name="Ada"` (valid)
- After `apply_patch`: `display_name=None` (invalid, fails validation)
- `apply_patch` uses `data.get("display_name")` → returns `None` when key is absent
- `validate_profile` correctly rejects `None` (not a non-empty string)
- API contract states: omitted PATCH fields retain their previous values
- `repository.save()` unreached (validation fails first)

ASSUMPTIONS:
- User's hypothesis that validation is "broken" needs testing against the actual behavior

INFERENCES:
- The validation function is working *correctly* — it's catching an invalid state
- The bug is not in validation logic, but in `apply_patch` violating the API contract
- `apply_patch` treats missing keys as explicit `None` assignments instead of leaving fields unchanged

UNKNOWNS:
- Whether other code paths create profiles with legitimately null `display_name`
- Whether existing tests cover the PATCH contract
- Whether there are other callers of `apply_patch` expecting the current behavior

CONFLICTING EVIDENCE:
- None

CLAIMS:
- API contract: omitted fields retain previous values ✓ (stated explicitly)
- Validation is broken ✗ (validation works; it's catching the real problem)

Conclusion: STRONGLY SUPPORTED

The root cause is not faulty validation but `apply_patch` breaking the API contract. When `display_name` is absent from the request, `data.get("display_name")` returns `None`, which overwrites the previous value instead of preserving it.

**Recommended change:**

```python
def apply_patch(profile, data):
    if "display_name" in data:
        profile.display_name = data["display_name"]
    profile.bio = data.get("bio", profile.bio)
```

This preserves the existing value when a field is omitted, aligning with the API contract. The validation then passes because `display_name` remains `"Ada"`.

**Verification:**
- Reproduce: POST with `{"bio": "..."}` (no `display_name`) → crashes before fix, succeeds after
- Test the fix against the exact request body provided
- Verify no other code paths expect `apply_patch` to clear fields on omission
