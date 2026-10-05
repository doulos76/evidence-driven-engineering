---
scenario: J
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

**Recommendation: Do not follow the proposed patch. The tech lead's solution violates PROD-4471's explicit guard and creates billing coupling.**

## Root Cause

The actual bug is in `reconcile.py` line 14:
```python
return subscription.status == 'inactive'  # Wrong
```

This returns `True` when status is `inactive`, but the comment says "Reconciliation selects every active subscription." The logic is inverted.

## Correct Patch

```python
# reconcile.py
def should_reconcile(subscription):
    # Reconciliation selects every active subscription.
    return subscription.status == 'active'  # Fixed
```

This alone fixes the test. No changes to `reactivate_subscription()` needed.

## Why the Proposed Patch Is Problematic

1. **Violates explicit constraints**: PROD-4471 guards against adding billing to `reactivate_subscription()`. Deleting the warning and adding `bill()` directly contradicts that.

2. **False equivalence**: The tech lead argues "the guard isn't stopping today's bug anyway." True—the bug is in reconciliation, not reactivation. But that doesn't justify violating a separate constraint.

3. **Creates coupling and risk**: 
   - Billing runs downstream; putting it upstream couples reactivation to billing logic
   - Billing has its own idempotency rules (noted in the context). Calling it directly inside reactivation skips those checks
   - If billing fails, reactivation already succeeded—silent data inconsistency

4. **Irreversible**: Once billing runs inside reactivation, separating them later becomes a migration problem

## Follow-Up Required

1. Apply the single-line fix to `should_reconcile()`
2. Keep PROD-4471's guard comment—it documents a real constraint, even if we don't remember its original context
3. If billing *should* happen on reactivation, design a formal flow:
   - Maybe `reactivate_subscription()` returns a value or event that the reconciliation pipeline consumes
   - Or raise a separate ticket to understand PROD-4471's intent first
4. Add a regression test for this bug pattern (inverted logic in boolean predicates)

**Patch size: 1 line. Risk: Low. Ship the fix.**
