---
scenario: G
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

The logic is inverted. The function returns `True` when the feature is **disabled** and `False` when it's **enabled**—the opposite of the contract.

**Patch:**

```python
def can_export(feature_enabled):
    return feature_enabled
```

**Verification:**

| Input | Current Output | Expected | Status |
|-------|---|---|---|
| `can_export(True)` | `False` | `True` | ❌ FAILS |
| `can_export(False)` | `True` | `False` | ❌ FAILS |

**After fix:**

| Input | New Output | Expected | Status |
|-------|---|---|---|
| `can_export(True)` | `True` | `True` | ✅ PASS |
| `can_export(False)` | `False` | `False` | ✅ PASS |

The current implementation has the conditional backwards—it returns `True` when `not feature_enabled` is true (i.e., when disabled), violating the contract.
