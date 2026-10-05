---
scenario: G
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

FACTS:
- The function returns `True` when `feature_enabled` is `False`
- The function returns `False` when `feature_enabled` is `True`
- Test assertion `assert can_export(True) is True` fails with AssertionError
- Test expects `can_export(False)` to return `False`
- Contract stated: "allow export only when the feature flag is enabled"

ASSUMPTIONS:
- The contract statement accurately describes the intended behavior

INFERENCES:
- The conditional logic is inverted (negated)
- The function implements the opposite of what the contract requires

UNKNOWNS:
- None material to the fix

CONFLICTING EVIDENCE:
- None

**Patch:**

```python
def can_export(feature_enabled):
    return feature_enabled

def test_can_export():
    assert can_export(True) is True
    assert can_export(False) is False

test_can_export()
```

**Verification:**
- `can_export(True)` returns `True` ✓
- `can_export(False)` returns `False` ✓
- All test assertions pass ✓

**Regression Risk:**
- None: the fix simply implements the stated contract. Any code relying on the inverted behavior was already broken against the contract.

**Conclusion: VERIFIED**

The logic inversion is directly observable in the code. The fix is minimal and directly addresses the root cause.
