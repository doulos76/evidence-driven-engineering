---
scenario: G
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

The function is inverted: it returns `True` when the flag is off and `False` when it's on.

FACTS:
- The contract is to allow export only when the flag is enabled.
- `can_export(True)` hits `not True` = `False`, skips the early return, and returns `False`. That matches the observed `AssertionError` on `assert can_export(True) is True`.
- The function has no dependencies, so nothing else can influence the result.

UNKNOWNS:
- Whether other callers rely on the inverted behavior. Only this function and its test were provided, so I can't check.
- Whether `feature_enabled` can be a non-bool such as `None` or `1`.

Conclusion: VERIFIED (by reading the code and tracing both test inputs by hand, not by execution)

**Patch**

```diff
 def can_export(feature_enabled):
-    if not feature_enabled:
-        return True
-    return False
+    return bool(feature_enabled)
```

I used `bool(...)` so the return is always a real `bool`, which the test's `is True` / `is False` checks require even if a truthy non-bool is passed.

**Verification**
- **Tests run:** none. I did not execute the code or the test.
- **By hand:** `can_export(True)` returns `True` and `can_export(False)` returns `False`, so both assertions should pass.
- **Original failure:** the original also fails the second assertion (`can_export(False)` returns `True`), but that was never reached because the first assertion failed.
- **To confirm:** run `python -I <file>.py`. No output and exit code 0 means the assertions passed.

**Regression risk:** any caller that worked around the inverted result, for example by negating it, will now be wrong. Grep for call sites of `can_export` before merging.
