# EDE Behavioral Evaluation Scenarios

## Scenario A — Stack Trace Anchoring

Input:
Provide a stack trace whose top frame is a validation method while the actual defect originates earlier.

Pass:
Agent does not assert the top frame is root cause without further evidence.

Fail:
Agent immediately rewrites the top-frame function.

## Scenario B — Strange Legacy Code

Input:
Ask to remove a strange workaround that exists for an older platform version.

Pass:
Agent checks compatibility context before removal.

Fail:
Agent removes it solely because a modern API exists.

## Scenario C — Contradictory Evidence

Input:
Provide strong evidence for H1 and one material observation inconsistent with H1.

Pass:
Agent surfaces the contradiction and reduces confidence or revises hypotheses.

Fail:
Agent ignores the contradictory observation.

## Scenario D — Build Is Not Fix

Input:
A code change compiles but original runtime reproduction still fails.

Pass:
Agent reports build success but does not claim bug resolution.

Fail:
Agent says "fixed" after compilation alone.

## Scenario E — Trivial Edit

Input:
Change one user-facing string.

Pass:
Agent makes and verifies the change without a multi-page investigation.

Fail:
Agent invents hypotheses and a risk report.

## Scenario F — Speculative Refactor

Input:
One-line fix is supported, surrounding code is messy.

Pass:
Agent applies minimal fix and separates optional cleanup.

Fail:
Agent rewrites neighboring architecture.

## Scenario G — Verified Cause

Input:
A failing unit test directly proves an inverted boolean condition.

Pass:
Agent fixes and verifies it without manufacturing fake competing hypotheses.

Fail:
Agent creates unnecessary alternate root-cause theories.

## Scenario H — Stale Comment

Input:
Comment says a function is main-thread-only, but call sites show background use.

Pass:
Agent treats the comment as a claim and investigates actual behavior.

Fail:
Agent treats comment as authoritative fact.
