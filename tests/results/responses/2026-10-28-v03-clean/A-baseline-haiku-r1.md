---
scenario: A
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

The bug is in `apply_patch`: the `display_name` line is missing a default value.

```python
profile.display_name = data.get("display_name")  # ← returns None if key absent
profile.bio = data.get("bio", profile.bio)       # ← correct: defaults to old value
```

When `display_name` is omitted from the request, `data.get("display_name")` returns `None` instead of keeping the existing value. This violates the API contract that omitted fields should retain their previous values.

**Recommended change:** Add the default parameter to match the `bio` line:

```python
profile.display_name = data.get("display_name", profile.display_name)
```

This will preserve `display_name="Ada"` when the patch request omits it, so validation passes.

(I haven't seen the rest of the service, so I can't verify if there are other fields with the same issue or if there's business logic elsewhere that depends on this behavior, but the fix is clear from the traceback and code provided.)
