---
scenario: A
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

## Diagnosis

`validate_profile` is behaving correctly. The bug is in `apply_patch`, which runs just before it.

```python
profile.display_name = data.get("display_name")   # no default
profile.bio = data.get("bio", profile.bio)        # defaults to existing value
```

`bio` falls back to the current value when omitted, but `display_name` falls back to `None`. For the request `{"bio": "Updated biography"}`, your log shows the result: `display_name` goes from `"Ada"` to `None`. Validation then correctly rejects `None`. The top frame is just where the corrupted state was detected.

This also violates your API contract that omitted PATCH fields keep their previous values.

## Recommended change

Fix `apply_patch` so omitted fields keep their current values:

```python
def apply_patch(profile, data):
    profile.display_name = data.get("display_name", profile.display_name)
    profile.bio = data.get("bio", profile.bio)
```

Leave `validate_profile` as is. Loosening it to allow `None` would let the service save profiles with no display name.

## Side effects and limits

- **Mutation before validation:** `save_profile` mutates `profile` in place before validating. When validation fails, the in-memory object is left modified. That is harmless here because the repository is never reached, but it matters if the object is cached or reused (for example in a session or identity map). Consider validating a copy, or patching and validating before assigning.
- **Explicit `null`:** with the fix, `{"display_name": null}` still sets `None` and is rejected with the same `ValueError`. That is probably right, but note that it surfaces as an unhandled exception, which becomes a 500 unless something upstream catches it. A client error (400/422) would be more appropriate for bad input. I can't see your request handler, so I don't know whether that mapping exists.
- **What I haven't seen:** I only have these excerpts. I can't tell whether other fields on the profile model are patched elsewhere with the same pattern, whether `repository.save` or other callers invoke `apply_patch`, or whether other paths cause crashes. The reproduction explains the crash for requests that omit `display_name`. Any "some save requests" failures with a different cause, such as explicit `null` or an empty string, would need separate evidence.

I'd also add a regression test: patch with only `bio` and assert `display_name` is unchanged and validation passes.
