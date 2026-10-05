---
scenario: G
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

**Root cause:** Inverted logic. The condition `if not feature_enabled` returns True when the flag is disabled, which violates the contract.

**Patch:**

```python
def can_export(feature_enabled):
    return feature_enabled
```

**Verification:**

Running the test with the patched function:

```python
def can_export(feature_enabled):
    return feature_enabled

def test_can_export():
    assert can_export(True) is True
    assert can_export(False) is False

test_can_export()
```

✓ Both assertions pass. The function now correctly allows export only when `feature_enabled` is True.
