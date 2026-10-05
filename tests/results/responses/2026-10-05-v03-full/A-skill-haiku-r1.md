---
scenario: A
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Diagnosis

FACTS:
- The exception occurs in `validate_profile` when `display_name` is `None`
- The request body contains only `{"bio": "Updated biography"}` — no `display_name` field
- Before `apply_patch`: `display_name="Ada"`
- After `apply_patch`: `display_name=None`
- The API contract requires omitted PATCH fields to retain their previous values
- The `validate_profile` function correctly rejects `None` values

ASSUMPTIONS:
- The provided code excerpts are complete for this flow
- The request truly contains only the `bio` field

INFERENCES:
- `apply_patch` is the source of the data corruption, not `validate_profile`
- `data.get("display_name")` returns `None` when the key is absent, which unconditionally overwrites the stored value
- `validate_profile` is functioning as intended — it's rejecting invalid data that `apply_patch` created

UNKNOWNS:
- None that would change the diagnosis

CONFLICTING EVIDENCE:
- None

CLAIMS:
- Your claim that "validation is broken" — this is contradicted by the code itself; the validation correctly rejects the invalid state

**Conclusion: VERIFIED**

The root cause is directly demonstrated in the code.

---

## Recommended Change

The bug is in `apply_patch`. It violates the API contract by overwriting `display_name` with `None` when that field is omitted from the request.

**Change:**
```python
def apply_patch(profile, data):
    if "display_name" in data:
        profile.display_name = data["display_name"]
    profile.bio = data.get("bio", profile.bio)
```

This makes `display_name` consistent with `bio`: both only update if explicitly provided. Omitted fields now preserve their previous values, honoring the API contract.

---

## Verification

- The fix prevents `display_name` from being set to `None` when absent from the request
- `validate_profile` will no longer reject valid profiles that omit `display_name`
- `save_profile` will reach `repository.save()`
- Regression risk is minimal: the only change is fixing the violation of the stated API contract

The original assumption (that validation is broken) masked the actual problem (that patching corrupted the data before validation could see it).
