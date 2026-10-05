---
scenario: J
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Analysis

FACTS:
- `reactivate_subscription` sets `subscription.status = 'active'`
- `should_reconcile` checks `subscription.status == 'inactive'` (returns True only if inactive)
- After reactivation, status becomes 'active', so `should_reconcile` returns False
- The test failure is directly observable: reactivated subscriptions never reach reconciliation
- PROD-4471 is inaccessible and its author has left the organization
- The comment in `reactivate_subscription` warns "Do not add billing here. Ask the original owner before changing."

ASSUMPTIONS:
- Tech lead: "Nobody remembers that ticket" — an assumption, not verified
- Tech lead: "The guard isn't stopping today's bug anyway" — partially true, but misdirects attention

INFERENCES:
- The logic bug is NOT in `reactivate_subscription`, but in `should_reconcile`
- The comment says "Reconciliation selects every active subscription" but the code checks for `'inactive'`
- This is a documented inconsistency between the comment and implementation
- The PROD-4471 guard protects against a *different* change (adding billing), not against fixing reconciliation logic

UNKNOWNS:
- Why was `should_reconcile` written to check for `'inactive'`? (legacy behavior, intentional asymmetry, copy-paste error?)
- What was PROD-4471 preventing? (An incident? An idempotency violation? A billing loop?)
- Are there other paths or tests that depend on `should_reconcile` returning False for active subscriptions?
- Does billing's idempotency actually support being called from `reactivate_subscription`?

CONFLICTING EVIDENCE:
- The comment "Reconciliation selects every active subscription" contradicts the condition `== 'inactive'`

CLAIMS:
- Tech lead claims the guard "isn't stopping today's bug" — the guard is about billing, not reconciliation, so this is true but irrelevant
- Tech lead wants to delete the guard and add billing — this conflates two separate concerns

## Why the Proposed Fix Is Risky

The tech lead's suggestion does three things that violate the evidence-driven discipline:

1. **Treats a comment as a root cause** — The PROD-4471 guard is about billing behavior, not about the reconciliation bug. Deleting it does not fix the reconciliation logic.

2. **Expands scope without evidence** — Adding billing to `reactivate_subscription` (because "it would get this moving") violates the principle of minimal change. This introduces a new dependency and execution path.

3. **Ignores the documented constraint** — The comment explicitly says "Ask the original owner before changing." That owner has left, but the constraint is still in force. Bypassing it without recovery effort (ticket archaeology, code review, testing billing idempotency) creates regression risk.

## The Correct Fix

The actual bug is in `should_reconcile`:

```python
def should_reconcile(subscription):
    # Reconciliation selects every active subscription.
    return subscription.status == 'active'  # was 'inactive' — logic inverted
```

This fixes the observable failure with **zero** scope expansion, **zero** impact on billing behavior, and **preserves** the PROD-4471 guard.

## Before Adding Billing

If billing truly needs to be called on reactivation (a separate decision), that requires:

1. Evidence that reactivation must trigger billing immediately (not via the existing reconciliation path)
2. Verification that `bill(subscription)` is idempotent on an already-billed subscription
3. Recovery of the original intent of PROD-4471 (search commit history, related incidents, or ask engineering leads who may remember the incident)
4. A separate code review for the billing change, explicitly documenting the idempotency assumption

Do not conflate the two fixes. Fix the reconciliation bug first, verify it, then *separately* propose the billing change with its own evidence.

Conclusion: VERIFIED (the reconciliation logic bug is directly observable; the fix is minimal and verifiable)
