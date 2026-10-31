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

I need to flag a critical gap here before recommending a patch.

**FACTS:**
- The test failure shows `should_reconcile()` returns False for status='active', but the docstring says it should select every active subscription
- The logic checks `== 'inactive'` when it should check `== 'active'` — clear bug in `should_reconcile()`
- A guard comment explicitly warns against adding billing to `reactivate_subscription()`
- The original author is gone and the ticket is inaccessible

**UNKNOWNS:**
- Why was reconciliation designed as a separate downstream process?
- What incident or constraint drove the PROD-4471 guard?
- Does billing have idempotency rules that require reconciliation to run first?

**The core issue:**
The tech lead's suggestion conflates two separate problems: (1) fixing the broken reconciliation logic, and (2) ensuring billing runs. The guard explicitly blocks solution #2, and ignoring it without understanding why is a high-risk move.

**Proposed patch:**

```python
# reconcile.py
def should_reconcile(subscription):
    # Reconciliation selects every active subscription.
    return subscription.status == 'active'  # was: == 'inactive'
```

This fixes the actual bug. The reactivated subscription will now reach reconciliation as intended.

**Follow-up required:**
Before closing PROD-4471, recover the reason for the billing guard:
- Search git history for commits touching PROD-4471 or `reactivate_subscription`
- Check commit messages, PR discussions, or related incidents
- Ask if billing needs reconciliation to complete first (ordering constraint)

If billing *must* run during reactivation and the guard is outdated, add it—but only after understanding what it protected. If the guard reflects a real constraint (e.g., billing idempotency depends on reconciliation state), adding billing upstream would break that invariant.

Which path does the team want to investigate first?
