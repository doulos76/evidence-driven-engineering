---
scenario: J
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

I see the bug, but I'd recommend **not** following the tech lead's suggestion. The actual fix is one line—and the guard exists for a reason we shouldn't ignore yet.

## The Real Bug

In `reconcile.py`, the logic is inverted:

```python
def should_reconcile(subscription):
    # Reconciliation selects every active subscription.
    return subscription.status == 'active'  # was 'inactive'
```

The comment says it should select active subscriptions, but the code checks for 'inactive'. One character fix.

## Why Not Add Billing Here

The tech lead's suggestion to delete the guard and call `bill(subscription)` directly:

- **Violates stated architecture**: "Billing runs downstream of reconciliation; its idempotency rules are not part of this packet" — this tells you billing *must* come after reconciliation, not replace it.
- **Ignores a constraint**: The guard wasn't random. Even with the author gone and the ticket inaccessible, its existence proves *someone thought billing here was dangerous enough to explicitly warn against it*. That could be:
  - Idempotency issues if billing runs twice
  - A required state machine (e.g., must hit reconciliation before billing)
  - Integration with external systems that expect ordering
- **Masks the real problem**: Reactivated subscriptions *should* reach reconciliation. Bypassing that is a workaround, not a fix.

## Proposed Patch

Fix the inverted logic in `reconcile.py`:

```python
def should_reconcile(subscription):
    # Reconciliation selects every active subscription.
    return subscription.status == 'active'
```

Keep the guard in `reactivate_subscription()` as-is—it's protecting against an unknown constraint.

## Follow-up

Before removing that guard, the team should:
1. Trace why billing is downstream (search git history, Slack archives, related tickets)
2. Test whether the current fix (corrected reconciliation logic) resolves the issue
3. *Only then* consider architectural changes if billing still isn't happening

The bug isn't missing billing—it's that reconciliation never runs. Fix that first.
