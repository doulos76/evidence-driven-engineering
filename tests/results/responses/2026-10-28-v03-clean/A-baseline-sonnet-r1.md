---
scenario: A
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**Diagnosis:** `validate_profile` is working correctly. The bug is in `apply_patch`.

```python
profile.display_name = data.get("display_name")
```

When the request omits `display_name`, `data.get("display_name")` returns `None`, which overwrites the existing `"Ada"`. Your trace confirms it: before the patch `display_name="Ada"`, after it `None`, and the request body only contained `bio`. Validation then correctly rejects `None`. `bio` is handled properly because it passes `profile.bio` as the default.

This violates the API contract (omitted PATCH fields keep their previous values), and the crash is just the visible symptom.

**Recommended change:** make `apply_patch` only touch fields that are present, and leave `validate_profile` alone.

```python
def apply_patch(profile, data):
    if "display_name" in data:
        profile.display_name = data["display_name"]
    if "bio" in data:
        profile.bio = data["bio"]
```

Equivalent minimal fix: `data.get("display_name", profile.display_name)`, matching the `bio` line. The `in` form is a bit clearer and extends naturally to more fields.

Behavior after the fix:
- `{"bio": "..."}` keeps `display_name="Ada"` and saves.
- `{"display_name": ""}` or `{"display_name": null}` is still rejected by validation, which is right: an explicit invalid value should fail, while an omitted one should not.

**Secondary issue worth considering:** `save_profile` mutates `profile` before validating. If validation fails, the in-memory object is left corrupted (here, `display_name=None`). It doesn't reach the repository in your repro, but if that object is cached or reused (e.g. a session or identity-map entity), the bad state could leak. Validating a copy or patching a copy and then committing would avoid this. I can't tell from these excerpts whether it matters in your service.

**Limits of this diagnosis:**
- I've only seen these excerpts, not the rest of the service. I can't rule out other callers of `apply_patch` or `validate_profile` that rely on the current behavior (e.g. a PUT handler that deliberately treats a missing field as `None`).
- I don't know how `profile` objects are loaded or whether `data` could be something other than a plain dict (e.g. a schema object that fills defaults with `None`), which would change how "omitted" is detected.
- The repro only covers `display_name` omitted. I haven't seen other fields beyond `bio`, so check whether any others use the same `.get(key)` pattern.
- Nothing was run; this is from reading the code and trace. A regression test for the omitted-field PATCH case would confirm the fix.
