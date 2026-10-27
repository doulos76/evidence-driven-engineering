---
scenario: A
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

The bug is in `apply_patch`, not `validate_profile`.

The request omits `display_name`, so `data.get("display_name")` returns `None`, which overwrites the existing value `"Ada"`. This violates your API contract that omitted PATCH fields should retain their previous values.

The `bio` field handles this correctly with `data.get("bio", profile.bio)`, but `display_name` is missing the default:

```python
profile.display_name = data.get("display_name")  # ← no default, returns None
```

**Recommended change:** Apply the same pattern to `display_name`:

```python
profile.display_name = data.get("display_name", profile.display_name)
```

This makes `apply_patch` consistently respect omitted fields and prevents the `None` from reaching validation.

I haven't inspected what happens if the request *explicitly* includes `display_name: null` or whether there's pre-save normalization elsewhere in the service, so the fix assumes the issue is purely in this patch logic.
