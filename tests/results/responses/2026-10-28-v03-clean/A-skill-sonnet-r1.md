---
scenario: A
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

FACTS:
- `validate_profile` raised `ValueError("display_name must be a non-empty string")` at `profiles.py:5`, called from `save_profile` at line 15.
- Request body was `{"bio": "Updated biography"}`, with no `display_name` key.
- Before `apply_patch`: `display_name="Ada"`. After: `display_name=None`, `bio="Updated biography"`.
- `apply_patch` sets `display_name = data.get("display_name")`, which returns `None` when the key is absent. `bio` uses `data.get("bio", profile.bio)`, which keeps the old value.
- `save_profile` calls `apply_patch` before `validate_profile`, and `repository.save` is never reached in this reproduction.

ASSUMPTIONS:
- The failing request is representative of the "some save requests" that crash, i.e. those omitting `display_name`.
- `save_profile` handles PATCH requests, as the contract note implies.

INFERENCES:
- The `None` came from `apply_patch`, not from stored data: the "before" value was "Ada" and the only intervening step is `apply_patch`.
- `validate_profile` rejected a value that is invalid by its own rule, so it behaved as written.

UNKNOWNS:
- Whether other callers use `apply_patch` or `validate_profile` (e.g., a PUT path where omitting `display_name` should be an error).
- Whether clients ever send `"display_name": null` deliberately, and what should happen then.
- Whether other fields exist beyond the two shown, with the same bug.
- Whether the validator has other issues I can't see (only the one check is shown).

CONFLICTING EVIDENCE:
- Your hypothesis (validation is broken) conflicts with the before/after trace: the validator received `None`, which its rule correctly rejects. The top frame is where the error was raised, not where the bad value was introduced.

CLAIMS:
- "The API contract says omitted PATCH fields retain their previous values." This is stated by you, not verified against the spec. It is consistent with how `bio` is handled.

## Hypotheses and evidence

1. **Validator is wrong.** It would need to reject a valid value. The value was `None`, and the rule requires a non-empty string, so this is contradicted.
2. **`apply_patch` overwrites omitted fields.** Supported by the before/after log and by the code: `data.get("display_name")` has no default. The `bio` line shows the intended pattern.

Conclusion: STRONGLY SUPPORTED

It is not VERIFIED because I haven't run the code, only compared the excerpts and log, which agree with each other.

## Recommended change

Fix `apply_patch` to match the `bio` line:

```python
def apply_patch(profile, data):
    profile.display_name = data.get("display_name", profile.display_name)
    profile.bio = data.get("bio", profile.bio)
```

Leave `validate_profile` unchanged. It is correctly catching the corruption, and loosening it would let `display_name=None` reach `repository.save`.

## Verification (not yet done)

- Add a regression test: profile with `display_name="Ada"`, patch `{"bio": "x"}`, then assert `display_name == "Ada"` and no exception.
- Add a test that an explicit `{"display_name": ""}` or `None` still raises `ValueError`. With the fix, explicit `None` is still assigned, then rejected by validation, which seems right but depends on the unknown above.

## Regression risk and remaining uncertainty

- If `apply_patch` is also used for full replacement (PUT), omitted fields would now be retained instead of cleared. Check its callers.
- If the same pattern exists for other fields not shown, they have the same bug.
- A related design concern: `save_profile` mutates `profile` before validating, so a failed validation leaves the in-memory object modified. This doesn't affect the stored record here, since the repository isn't reached, but it matters if the object is cached or reused. I'd treat it as a separate issue, not part of this fix.

I only have these excerpts, so I haven't checked callers, tests, or git history. I can search the repo for them if you point me at it.
