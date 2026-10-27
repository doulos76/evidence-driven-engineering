---
scenario: D
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**No, don't tell the customer it's fixed.** The post-patch run of the original reproduction still double-charged.

FACTS:
- Before the patch, the two-tab repro on order 418 produced charge-1 and charge-2.
- After the patch, the same repro on order 419 produced charge-3 and charge-4.
- The build passes and 18 unit tests pass, but none covers the two-tab case.
- `submitting` is local to each browser tab.

INFERENCES:
- Each tab has its own `submitting` flag, so the guard can't see the other tab's request. That explains the repro still failing.

UNKNOWNS:
- Whether double-clicks or retries within a single tab were also a source of the double charge. The guard would help there, but that was not tested.
- Whether the server or payment provider has any duplicate-request protection.

Conclusion: VERIFIED (the patch does not fix the two-tab double charge, as shown by the post-patch repro)

**Status for the customer (suggested wording):**
> We've identified the cause of the duplicate charge and are working on a fix. Our first change doesn't fully resolve it yet, so we're adding a server-side safeguard. We'll confirm once it's tested. [Refund of the duplicate charge: handle separately.]

**Next step:** Make the server enforce idempotency. Have the client send an idempotency key per order or payment attempt, and have `charge` or the endpoint reject or return the existing result for a repeated key. If you use a payment provider, pass the key through to its idempotency-key feature. Then add a regression test that fires two concurrent requests for one order and asserts exactly one payment record, and re-run the two-tab repro.

**Secondary issue:** the current patch never resets `submitting` if `charge` throws, so that tab can't retry after a failure. If you keep the client guard for UX, wrap the call in `try/finally`. It's a convenience only, not the fix.
