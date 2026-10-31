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

FACTS:
- `validate_profile` raises `ValueError` when `display_name` is `None` or not a string
- `apply_patch` sets `profile.display_name = data.get("display_name")`, which returns `None` when the key is absent
- The request omits `display_name`; state changes from `"Ada"` → `None`
- The API contract requires omitted fields to retain previous values
- The validation never executes on a valid state

ASSUMPTIONS:
- The code excerpts are complete and representative

INFERENCES:
- `validate_profile` logic is correct—it properly validates the constraint
- `apply_patch` violates the API contract on the first line only

UNKNOWNS:
- Whether other callers of `apply_patch` have been affected

CONFLICTING EVIDENCE:
- None—the facts align

---

**The bug is in `apply_patch`, not `validate_profile`.** The validation is working exactly as intended.

Line 2 of `apply_patch` correctly implements the contract:
```python
profile.bio = data.get("bio", profile.bio)
```

Line 1 does not:
```python
profile.display_name = data.get("display_name")  # Returns None, overwrites Ada
```

**Recommended change:**

```python
def apply_patch(profile, data):
    profile.display_name = data.get("display_name", profile.display_name)
    profile.bio = data.get("bio", profile.bio)
```

This makes both fields consistent: omitted keys fall back to the existing value, preserving it per the API contract.

---

**Conclusion: VERIFIED** — The bug is directly observable in the code flow and state trace. The one-line fix addresses the root cause (missing default in `data.get()`) without changing the validation logic.
