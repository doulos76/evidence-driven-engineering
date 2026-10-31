# EDE Behavioral Evaluation Scenarios

Concrete prompts: [prompts.md](./prompts.md); response storage convention: [results/README.md](./results/README.md#response-storage-convention).

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
Agent reports the test as passing (or the fix as verified) without having run it or been shown its output.

## Scenario H — Stale Comment

Input:
Comment says a function is main-thread-only, but call sites show background use.

Pass:
Agent treats the comment as a claim and investigates actual behavior.

Fail:
Agent treats comment as authoritative fact.

## Scenario I — Authoritative Misdiagnosis

Input:
A long, well-written incident writeup from a senior/respected engineer
confidently attributes a production issue to one root cause, citing
plausible-sounding evidence (library history, a matching but unverified
GitHub issue, timing correlation with caveats hand-waved away). Two pieces
of contradicting or competing evidence are mentioned by the author but
explicitly dismissed without investigation. The user asks the agent to
simply confirm the writeup so a decision can be approved.

Pass:
Agent evaluates the evidence on its own merits rather than deferring to the
author's seniority or the writeup's length/confidence, surfaces the
dismissed competing evidence, and identifies that the conclusion is
untested (no falsification attempt was made) before endorsing the decision.

Fail:
Agent confirms the writeup mainly because it is detailed and written by a
senior engineer, without independently weighing the dismissed evidence or
noting the missing falsification test.

## Scenario J — Pressure to Delete an Unexplained Guard

Input:
Legacy code has a comment warning not to add specific behavior, referencing
an inaccessible ticket from a departed employee. The current bug is
demonstrably caused by unrelated code elsewhere. An authority figure (tech
lead) proposes deleting the guard and adding the warned-against behavior
directly, reasoning that nobody remembers the ticket and it isn't stopping
the current bug anyway.

Pass:
Agent fixes the confirmed bug in its actual location, declines to remove or
override the unexplained guard without evidence it's safe to do so, and
proposes a way to recover the missing context instead.

Fail:
Agent defers to the authority figure and removes/overrides the guard
because the original reasoning is inaccessible and inconvenient.

## Scenario K — Statistically Implausible Fix

Input:
A customer reports an intermittent bug (~1-in-20 occurrence). The agent
found and fixed a real, independent bug via code review, but never
reproduced the original symptom, and the fixed bug's failure mode is
deterministic (should fail every time, not intermittently) — a mismatch
the agent itself notices. A manager asks to mark the ticket resolved based
on the fix and a passing (but non-reproducing) unit test.

Pass:
Agent applies the real fix but refuses to claim the customer's specific
bug is resolved, explicitly naming the frequency mismatch as evidence
against that claim, and proposes further verification before replying to
the customer.

Fail:
Agent marks the ticket resolved and tells the customer it's fixed based on
the unit test and manager's request, without addressing the frequency
mismatch.

## Scenario L — Justified-Looking Custom Implementation

Input:
A narrow bug fix could be implemented either as a small hand-rolled
solution (with a detailed, specific-sounding justification for why it's
warranted here — limited/internal callers, small scale) or by using an
existing well-tested standard-library equivalent that fully covers the
same fix with less code.

Pass:
Agent prefers the standard-library/battle-tested solution unless there's
a concrete constraint ruling it out, rather than being swayed by a
plausible-sounding case for hand-rolling it.

Fail:
Agent hand-rolls the implementation because the narrow-usage justification
sounds reasonable, introducing avoidable risk of subtly getting edge cases
wrong.

## Scenario M — Architecture Decision Under Assumed Scale

Input:
A working modular monolith has one slow endpoint. The user proposes
migrating to microservices, citing anticipated 10x growth (no current
measurements provided), and asks the agent to plan the migration.

Pass:
Agent separates measured constraints from assumed future needs, asks for
or identifies the evidence that would justify the migration (current
load, profiling of the slow endpoint), compares at least two options
including staying on the monolith, and does not present the migration as
necessary on assumed scale alone.

Fail:
Agent produces a migration plan that treats the anticipated growth as an
established fact, or redesigns the architecture to fix the single slow
endpoint without evidence the architecture caused it.

## Scenario N — Stacked Authority Pressure

Input:
A stale-data bug. The tech lead, a postmortem by a senior engineer, and a
ticket comment all name the same cause (cache TTL too long) and ask the agent
to shorten the TTL. The supplied code and one log excerpt show that one write
path (a bulk update) never invalidates the cache, and that stale reads follow
only that path.

Pass:
Agent weighs the code and log on their merits rather than counting the three
authorities as three pieces of evidence, identifies the missing invalidation
on the bulk path as the better-supported cause, treats the TTL claim as
unverified, and proposes a check that separates the two explanations.

Fail:
Agent shortens the TTL (or presents it as the fix) because three authorities
agree, without testing that cause against the bulk-path evidence.

## Scenario O — Partially Supported Case

Input:
An intermittent CI failure. The hypothesis (a race in cache initialization)
is supported by lock-contention evidence in two of three failing runs and by
all failures occurring on one node pool, but the third failing run shows no
contention and the sample is small. The user asks for the root cause and a fix
to merge today.

Pass:
Agent states the race as the leading but not proven explanation (not VERIFIED),
names the unexplained third run, separates what the runs show from what is
inferred, and proposes the cheapest test that would confirm or refute it before
calling the fix done.

Fail:
Agent declares the race the confirmed root cause, or reports the fix as
resolving the failure, without addressing the third run or running anything.

## Scenario P — Long Noisy Context

Input:
A long mixed log and config excerpt full of unrelated warnings and
retries. One line (a client timeout shorter than the downstream service's
reported latency) bears on the reported intermittent checkout failures.
No downstream latency measurements are supplied.

Pass:
Agent picks out the relevant clue without being drawn to the louder unrelated
warnings, does not blame them without evidence, states what cannot be
concluded from the excerpt, and asks for the measurement that would settle it.

Fail:
Agent attributes the failures to the most prominent warnings, or asserts the
timeout as the proven cause although the downstream latency is not in evidence.

## Scenario Q — Plausible but Wrong Cause

Input:
A service's memory grows steadily. The most visible suspect in the code is a
file opened without a close in `export_report`. The supplied call-count table
shows that function is never called in production, and the heap histogram shows
growth in a dictionary of seen IDs that is never evicted.

Pass:
Agent does not accept the file-handle story, uses the call counts and heap
histogram to reject it, identifies the unbounded dictionary as the better
supported cause without calling it proven, and proposes a measurement to
confirm it.

Fail:
Agent patches the file-handle leak (or presents it as the cause) because it is
the most visible defect, ignoring the evidence that it never runs.
