---
scenario: G
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

The bug is an inverted condition: the function returns `True` when the flag is disabled and `False` when it's enabled, the opposite of the contract.

**Patch**

```diff
 def can_export(feature_enabled):
-    if not feature_enabled:
-        return True
-    return False
+    return bool(feature_enabled)
```

`bool(...)` keeps the return type a real `bool`, so the test's `is True` / `is False` identity checks hold even if a truthy non-bool value is passed in. If you'd rather keep it strictly literal, `return feature_enabled` also passes the given test but would leak non-bool values.

**Verification**

I have not run anything, so there is no test result to report. By reading the code against the test:

- `can_export(True)` → `bool(True)` → `True`, so `assert ... is True` should pass.
- `can_export(False)` → `bool(False)` → `False`, so `assert ... is False` should pass.

The observed failure (`assert can_export(True) is True` raising `AssertionError`) matches the old code, which returned `False` for `True`. That is consistent with the inversion being the sole cause. To confirm, run the snippet with the patch applied, e.g. `python3 -I your_file.py`; no output and exit code 0 means the test passed.
