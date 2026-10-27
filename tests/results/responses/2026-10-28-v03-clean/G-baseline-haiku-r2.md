---
scenario: G
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

The function has inverted logic. The current implementation returns `True` when the flag is *disabled* and `False` when it's *enabled* — the opposite of the contract.

**Patch:**

```python
def can_export(feature_enabled):
    return feature_enabled
```

**Verification:**

| Input | Current | Expected | Result |
|-------|---------|----------|--------|
| `can_export(True)` | `False` ❌ | `True` | **FIXED** |
| `can_export(False)` | `True` ❌ | `False` | **FIXED** |

The test will pass after applying this fix.
