---
scenario: G
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**Bug:** the condition is inverted. It returns `True` when the flag is *disabled* and `False` when enabled, which is the opposite of the contract. That matches the observed failure: `can_export(True)` returns `False`, so the first assertion fails.

**Patch:**

```diff
 def can_export(feature_enabled):
-    if not feature_enabled:
-        return True
-    return False
+    return feature_enabled is True
```

I used `is True` rather than `bool(feature_enabled)` so the function always returns an actual `bool` and the test's `is True` / `is False` checks hold. It also means truthy non-boolean values like `1` or `"yes"` are denied. If you want truthy values to count as enabled, use `return bool(feature_enabled)` instead.

**Verification:** I did not run the test, so there is no run result to report. By reading the code against the test:
- `can_export(True)` → `True is True` → `True`, so the first assertion passes.
- `can_export(False)` → `False is True` → `False`, so the second assertion passes.

I can run it if you'd like, but the code isn't saved to a file here, so I'd need to create one first.
