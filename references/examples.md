# EDE Examples

## Example 1 — Stack Trace

Bad:

> The crash is caused by Realm thread confinement because `verifyThread` is the top frame.

Better:

- FACT: `verifyThread` appears in the stack.
- FACT: the crash occurs after an async boundary.
- ASSUMPTION: a Realm-managed object crossed executors.
- H1: cross-thread object access.
- H2: object lifecycle invalidation.
- Next test: trace object creation and executor transitions.

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
