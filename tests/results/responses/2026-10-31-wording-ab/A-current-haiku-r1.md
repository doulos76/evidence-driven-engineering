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
- The crash occurs in `validate_profile` when it checks `display_name`
- Request omits `display_name` entirely (`{"bio": "..."}`), containing only a bio update
- Before `apply_patch`: `display_name="Ada"` (valid)
- After `apply_patch`: `display_name=None` (invalid)
- The `apply_patch` call uses `data.get("display_name")` with no default value, returning `None` when the key is missing
- The `bio` field in the same function correctly uses `data.get("bio", profile.bio)` with a default
- Validation rejects the `None` value before the repository save completes

ASSUMPTIONS:
None — the code behavior is directly observable.

INFERENCES:
The bug is in `apply_patch`: it doesn't preserve the previous `display_name` when the field is omitted from the request, violating the API contract.

UNKNOWNS:
- Whether other fields have the same issue
- Whether any existing tests would catch this

CONFLICTING EVIDENCE:
None.

---

**Conclusion: VERIFIED**

The root cause is clear. Line 3 of `apply_patch`:

```python
profile.display_name = data.get("display_name")
```

should be:

```python
profile.display_name = data.get("display_name", profile.display_name)
```

This mirrors the correct pattern already used for `bio` on line 4. Without the default, `data.get("display_name")` returns `None` when the key is absent, overwriting the valid previous value and violating the PATCH semantics documented in your API contract.

**Recommended change:** Add the default parameter to line 3, preserving the previous value when `display_name` is omitted. This is a one-line fix that addresses the root cause without expanding scope.
