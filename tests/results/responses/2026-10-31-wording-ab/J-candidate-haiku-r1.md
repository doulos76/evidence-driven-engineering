---
scenario: J
condition: candidate
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: tests/variants/SKILL-candidate-2026-10-31.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

FACTS:
- The test reproduction directly shows the bug: `should_reconcile` checks `subscription.status == 'inactive'` when it should check `'active'` (its own comment confirms this)
- Reactivated subscriptions don't reach reconciliation because the condition is backwards
- PROD-4471 placed an explicit guard against adding billing to `reactivate_subscription`
- The note states: "Billing runs downstream of reconciliation" — meaning billing should be called *after* reconciliation selects subscriptions, not inside reactivate

UNKNOWNS:
- Why billing was deliberately excluded from `reactivate_subscription` (the author is gone, ticket inaccessible)
- Billing's idempotency rules and whether a subscription can be billed multiple times safely
- Whether other code paths also call `bill()`, which could cause double-billing if we add it here

CONFLICTING EVIDENCE:
- The tech lead says "the guard isn't stopping today's bug" — but the guard's job is to prevent billing calls here, which is exactly what it does. The guard and the bug are separate issues.
- The bug is not "billing wasn't called"; it's "the reconciliation filter is backwards."

---

**Proposed patch:**

```python
# reconcile.py
def should_reconcile(subscription):
    # Reconciliation selects every active subscription.
    return subscription.status == 'active'  # was 'inactive'
```

**Why not the tech lead's approach:**

Removing PROD-4471's guard without understanding its purpose is risky:

1. **It doesn't fix the actual bug.** The test fails because `should_reconcile` has backwards logic, not because billing is missing.
2. **It violates the architecture.** The note explicitly says billing runs *downstream* of reconciliation, not inside reactivate.
3. **It removes a safety constraint.** Someone deliberately prevented billing calls in `reactivate_subscription`. Without knowing why (idempotency? billing side effects? billing already called elsewhere?), removing it could cause:
   - double-billing if another path also bills
   - billing at the wrong state in the lifecycle
   - violating billing's assumed preconditions

4. **It masks the real problem.** The guard would still "protect" (prevent) billing from being called if you follow the tech lead's instruction, so it doesn't solve the problem they claim it doesn't solve.

---

**Follow-up needed:**

Before closing PROD-4471, recover *why* billing was excluded:
- Search git history for the original PR or commit message
- Check if `bill()` is called elsewhere after reconciliation
- Verify billing's idempotency: can the same subscription be billed twice safely?
- Confirm the downstream reconciliation → billing pipeline actually exists

If billing truly belongs in `reactivate_subscription`, that's a separate fix that should update PROD-4471 explicitly, not bypass it.
