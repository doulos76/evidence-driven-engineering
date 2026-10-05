# EDE Examples

## Example 1 — Stack Trace

Bad:

> The crash is caused by Realm thread confinement because `verifyThread` is the top frame.

Better:

```text
FACTS:
- `verifyThread` appears in the supplied Realm stack trace.
- The crash occurs after an async boundary.
ASSUMPTIONS:
- A Realm-managed object may have crossed executors; its ownership has not been traced.
INFERENCES:
- Cross-thread access is a candidate explanation, but lifecycle invalidation remains a viable alternative.
UNKNOWNS:
- The object's creation executor, access executor, and validity at the failing access.
CONFLICTING EVIDENCE:
- None supplied; the absence of contradicting observations does not establish the cause.
CLAIMS:
- The proposed diagnosis says that the top `verifyThread` frame proves thread confinement caused the crash; that claim is unverified.

Conclusion: INFERRED
```

Next test: trace object creation and executor transitions, and inspect
object validity at the failing access. If creation and access occur on the
same executor, that weakens the cross-thread explanation; compare the
lifecycle evidence before proposing a fix.

## Example 2 — Legacy Code

Bad:

> This workaround is ugly. Replace it with the modern API.

Better:

Before replacing it:
- inspect deployment target
- inspect version guards
- inspect callers
- inspect tests
- inspect history if useful

Then determine whether the workaround still protects supported versions or behavior.

## Example 3 — Verification

Bad:

> Fixed. Build succeeds.

Better:

> The project builds successfully. The original runtime reproduction also no longer fails, and the regression test passes. The root cause is STRONGLY SUPPORTED because ...
