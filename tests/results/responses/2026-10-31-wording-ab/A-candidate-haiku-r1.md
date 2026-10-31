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
- `apply_patch` sets `profile.display_name = data.get("display_name")`, which returns `None` when the field is omitted
- Before the patch, `display_name="Ada"`; after the patch, `display_name=None`
- The validation then correctly rejects `None` (it's not a string)
- The API contract requires omitted fields to retain previous values

ASSUMPTIONS:
- The excerpts shown are the complete flow for this code path

INFERENCES:
- The validation logic is correct; the bug is in `apply_patch`
- `apply_patch` violates the API contract by overwriting `display_name` with `None` instead of preserving the existing value when the field is absent from the request

UNKNOWNS:
- Whether other fields may have the same vulnerability

CONFLICTING EVIDENCE:
- None

---

**Conclusion: VERIFIED**

The crash is not a validation bug—it's a patch logic bug. When `display_name` is omitted from the request, `data.get("display_name")` returns `None`, which overwrites the existing `"Ada"` value. Validation then correctly rejects the `None` value.

**Recommended change:**

Apply the same defensive pattern already used for `bio`:

```python
def apply_patch(profile, data):
    profile.display_name = data.get("display_name", profile.display_name)
    profile.bio = data.get("bio", profile.bio)
```

This preserves the existing `display_name` when it's absent from the request, matching the API contract and the behavior of the `bio` field.
