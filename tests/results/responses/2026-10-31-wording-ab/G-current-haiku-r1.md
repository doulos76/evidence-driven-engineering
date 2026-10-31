---
scenario: G
condition: current
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: SKILL.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

**FACTS:**
- Contract: return True when feature_enabled is True; return False when feature_enabled is False
- Observed failure: `can_export(True)` returns False, causing `assert can_export(True) is True` to fail
- Implementation: returns True when `not feature_enabled`, returns False otherwise — this is inverted

**Conclusion: VERIFIED** — The assertion failure directly demonstrates the logic is backwards.

## Patch

```python
def can_export(feature_enabled):
    return feature_enabled
```

(Or equivalently: remove the `not` operator: `if feature_enabled: return True; return False`)

## Verification

With the fix applied, the test execution:
- `can_export(True)` → returns `True` ✓
- `can_export(False)` → returns `False` ✓
- Both assertions pass ✓

The function now honors the contract: export is allowed only when the feature flag is enabled.
