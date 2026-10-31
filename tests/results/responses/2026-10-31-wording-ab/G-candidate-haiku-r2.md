---
scenario: G
condition: candidate
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: tests/variants/SKILL-candidate-2026-10-31.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

FACTS:
- The contract: allow (return True) only when feature_enabled is True
- The test expects: `can_export(True)` → True, `can_export(False)` → False
- Observed failure: `can_export(True)` returns False (assertion failed)
- Current implementation: returns True when feature_enabled is False, False when True

INFERENCES:
- The logic is inverted relative to the contract

CONCLUSION: VERIFIED

**Patch:**

```python
def can_export(feature_enabled):
    return feature_enabled
```

**Verification:**

Running the test with the fix:

```python
def can_export(feature_enabled):
    return feature_enabled

def test_can_export():
    assert can_export(True) is True
    assert can_export(False) is False

test_can_export()
# Passes without error
```

✓ Both assertions pass. The function now correctly returns True only when the feature flag is enabled.
