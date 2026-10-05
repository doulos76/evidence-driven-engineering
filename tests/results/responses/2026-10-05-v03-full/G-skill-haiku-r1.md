---
scenario: G
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Establish What Is Known

FACTS:
- Contract requires: "allow export only when the feature flag is enabled"
- Test expects: `can_export(True)` → `True` and `can_export(False)` → `False`
- Observed failure: `assert can_export(True) is True` raises AssertionError
- Current implementation: `if not feature_enabled: return True` followed by `return False`
- Logic trace: When `feature_enabled=True`, condition `not True` is `False`, so execution skips to `return False` (wrong)
- No external dependencies or state involved

ASSUMPTIONS:
- The contract and test reflect the intended behavior
- No hidden requirement exists that would justify the inverted logic

INFERENCES:
- The function logic is inverted: it returns `True` when the feature is disabled, and `False` when enabled

UNKNOWNS:
- None — the problem is fully specified and directly traceable

CONFLICTING EVIDENCE:
- None

CLAIMS:
- None — only facts are observable here

Conclusion: VERIFIED

The logic inversion is directly demonstrable by tracing execution: the condition `not feature_enabled` inverts the expected return values.

## Proposed Fix

```python
def can_export(feature_enabled):
    return feature_enabled
```

## Verification

Running the test with the fix:

```python
def can_export(feature_enabled):
    return feature_enabled

def test_can_export():
    assert can_export(True) is True
    assert can_export(False) is False

test_can_export()
# Passes without assertion error
```

- `can_export(True)` returns `True` ✓
- `can_export(False)` returns `False` ✓
- Both assertions pass

## Regression Risk

Minimal. The change directly inverts the broken logic to match the stated contract. Since the previous behavior violated the contract, any code relying on the inverted behavior would itself be a bug. The test was already present and failing, confirming that the old behavior was unintended.

## Remaining Uncertainty

None — the contract, test, and required fix are fully determined by the specification.
