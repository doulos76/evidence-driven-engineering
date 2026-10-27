---
scenario: A
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

## FACTS:
- Request omits `display_name` field
- `apply_patch` executes: `profile.display_name = data.get("display_name")` → returns `None` (key not present)
- Before patch: `display_name="Ada"`; after patch: `display_name=None`
- API contract: omitted fields retain previous values
- `validate_profile` correctly rejects `None` display_name
- Crash occurs *during* validation, before repository save

## ASSUMPTIONS:
- The validation logic itself is correct (non-empty string requirement is intentional)
- This is the only place `apply_patch` is called

## INFERENCES:
- The root cause is **not** in `validate_profile`—the validation is working correctly
- The root cause is in `apply_patch`: it violates the API contract by setting unspecified fields to `None` instead of leaving them unchanged

## UNKNOWNS:
- Whether `apply_patch` is used in other contexts where this behavior might be relied upon
- Whether there are other fields with similar issues

---

**Conclusion: VERIFIED**

The evidence directly demonstrates the cause: `apply_patch` uses `data.get("display_name")` without a fallback, so omitted keys become `None`. This overwrites the prior value and violates the stated API contract.

**Recommended change:**

```python
def apply_patch(profile, data):
    if "display_name" in data:
        profile.display_name = data["display_name"]
    profile.bio = data.get("bio", profile.bio)
```

This preserves the existing `display_name` when it's not in the patch request, matching the contract. The `bio` line already handles this correctly with a fallback default.

**Risk:** Low. This change aligns code with the stated API contract. Verify that no other callers depend on the broken behavior (setting omitted fields to `None`).
