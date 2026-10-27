---
scenario: A
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

FACTS:
- `validate_profile` raised `ValueError` at `profiles.py:5` because `display_name` was `None`.
- Request body was `{"bio": "Updated biography"}`, with no `display_name` key.
- Before `apply_patch`: `display_name="Ada"`. After: `display_name=None`.
- `apply_patch` sets `profile.display_name = data.get("display_name")`, with no default. The `bio` line uses `data.get("bio", profile.bio)`.
- `save_profile` calls `apply_patch` before `validate_profile`; `repository.save` is never reached in this repro.

ASSUMPTIONS:
- The failing requests in production share this shape (PATCH without `display_name`). Only one repro was provided.
- `save_profile` is the PATCH handler path, as the API contract implies.

INFERENCES:
- The `None` comes from `apply_patch` overwriting the existing value, not from stored data being bad (the "before" value was `"Ada"`).
- The validator is behaving correctly for its stated rule; it is the first place the corrupted state is observed.

UNKNOWNS:
- Whether other callers use `apply_patch`/`validate_profile` (e.g., PUT/create paths where requiring `display_name` is intended).
- Whether any client intentionally sends `"display_name": null` to clear it, and what the contract says then.
- Whether other fields in the unseen code have the same pattern.
- Whether all production crashes match this shape; I haven't seen other tracebacks.

CONFLICTING EVIDENCE:
- None found. The only tension is your hypothesis (validation is broken) versus the data, which shows the input to validation was already wrong.

Hypotheses:
1. **Validation is too strict/broken.** Contradicted: the rule rejects `None` and empty strings, which is reasonable, and the same object held a valid `"Ada"` one step earlier.
2. **`apply_patch` clobbers omitted fields.** Supported: the before/after trace and the asymmetry with the `bio` line, plus the API contract, match this directly.

Conclusion: STRONGLY SUPPORTED

(Not VERIFIED because I haven't executed the code; the evidence is the excerpts and logged state, which are consistent and leave no competing explanation for this repro.)

**Recommended change** (minimal, in `apply_patch` only):

```python
def apply_patch(profile, data):
    profile.display_name = data.get("display_name", profile.display_name)
    profile.bio = data.get("bio", profile.bio)
```

Leave `validate_profile` as is. It correctly guards against saving a nameless profile, and loosening it would have hidden the bug and let `display_name=None` reach the repository.

**Verification to run:**
- Regression test: profile with `display_name="Ada"`, patch `{"bio": "..."}` → saves, `display_name` stays `"Ada"`.
- Patch `{"display_name": ""}` and `{"display_name": None}` → still rejected by validation (confirm that's the intended contract).

**Regression risk:** If any client relies on sending an explicit `null` to clear the name, behavior is unchanged (`None` is still applied then rejected). If `apply_patch` is also used for full replacement (PUT), omitting `display_name` would now keep the old value instead of failing; check callers.

**Remaining uncertainty:** I only saw these excerpts, not other callers, tests, or git history. Check for the same `data.get("x")` pattern on other fields, and confirm the contract for explicit nulls.
