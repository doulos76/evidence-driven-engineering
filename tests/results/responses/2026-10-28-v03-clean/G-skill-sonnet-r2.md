---
scenario: G
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

The function has its condition inverted: it returns `True` when the flag is off. The observed failure matches this. `can_export(True)` evaluates `not True`, skips the branch, and returns `False`, so `assert can_export(True) is True` fails.

**Patch**

```diff
 def can_export(feature_enabled):
-    if not feature_enabled:
-        return True
-    return False
+    return bool(feature_enabled)
```

`bool(...)` keeps the return type a real `bool`, which the `is True` / `is False` assertions require. Returning `feature_enabled` directly would fail them if a caller passed a truthy non-bool such as `1`.

**Verification (not executed)**

I have not run the test, so this is a hand trace of the patched code against the two assertions:
- `can_export(True)` returns `bool(True)`, which is `True`, so `is True` passes.
- `can_export(False)` returns `bool(False)`, which is `False`, so `is False` passes.

The test file is self-contained, so you can confirm it with `python -I test_file.py`. No output means both assertions passed.

**Remaining uncertainty**
- I only had this function and its test. If other callers relied on the inverted behavior, they would change with this fix, so check them.
- Treating `None` or other falsy values as "disabled" is my assumption. The contract only describes a boolean flag.
