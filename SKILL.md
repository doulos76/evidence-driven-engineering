---
name: evidence-driven-engineering
description: Evidence-first engineering judgment framework for debugging, code review, legacy maintenance, incident analysis, refactoring, and architecture decisions. Use when causes are uncertain, changes are risky, or existing behavior may have hidden constraints.
---

# Evidence Driven Engineering

## Core Principle

Do not treat plausible explanations as verified facts.

Be strict with evidence, humble with interpretation, and skeptical of your own conclusions.

## Four Pillars

- Evidence before conclusions.
- Falsification before confidence.
- Context before modification.
- Verification before claims.

## Apply With Risk-Proportional Depth

Keep trivial, directly verifiable work lightweight.

Use deeper investigation when the task involves uncertainty, unfamiliar or legacy behavior, concurrency, persistence, security, production incidents, destructive operations, migrations, authentication, or other high-regression-risk changes.

## Establish What Is Known

Before choosing a cause on any non-trivial diagnosis — this includes a bare stack trace, crash report, or error log presented with no other context — output this section before proposing a fix, using these exact labels:

```
FACTS:
- ...
ASSUMPTIONS:
- ...
INFERENCES:
- ...
UNKNOWNS:
- ...
CONFLICTING EVIDENCE:
- ...
CLAIMS:
- ...
```

- **FACT** — directly observed or verified
- **ASSUMPTION** — plausible but unverified
- **INFERENCE** — conclusion derived from facts but not directly observed
- **UNKNOWN** — missing information that could materially change the conclusion
- **CONFLICTING EVIDENCE** — evidence that does not fit the current explanation
- **CLAIM** — statement from a comment, ticket, commit, document, or person that still requires verification when material

Omit a category only if it is genuinely empty for this task — do not omit the section itself. A single alarming symptom (a crash, a stack trace) does not make the cause trivial; the diagnosis is still non-trivial even when the fix that follows is a one-line change.

Do not silently turn claims or inferences into facts.

## Investigate Before Fixing

When the cause is materially uncertain:

1. Identify observable facts.
2. Generate at least two plausible hypotheses when that adds real value.
3. For each hypothesis, identify supporting, contradicting, and missing evidence.
4. Attempt to falsify the leading hypothesis.
5. Prefer the cheapest test that meaningfully distinguishes between hypotheses.

Do not manufacture fake alternatives when the cause is already directly proven.

## Reconstruct Context Before Changing Existing Behavior

Before modifying unfamiliar or legacy behavior, inspect relevant context when useful and available:

- callers and call sites
- tests
- git history
- issue or PR context
- neighboring implementations
- lifecycle and concurrency assumptions
- platform/version constraints
- persistence or migration constraints

Ask:

> Why might a reasonable engineer have written this code this way?

This is not an assumption that the code is correct. It is a search for hidden constraints.

## Classify the Conclusion

For any non-trivial diagnosis, state the confidence label on its own line, in this exact form:

```
Conclusion: VERIFIED | STRONGLY SUPPORTED | INFERRED
```

- **VERIFIED** — directly demonstrated
- **STRONGLY SUPPORTED** — supported by multiple pieces of evidence and meaningful alternatives were weakened
- **INFERRED** — best current explanation but not sufficiently proven

A fix that compiles or a plausible-looking cause is not, by itself, grounds for VERIFIED. Do not invent precise confidence percentages without a real measurement basis.

## Change Minimally

Prefer the smallest evidence-supported change that:

- addresses the supported cause
- preserves unrelated behavior
- minimizes regression surface
- is easy to validate
- is easy to revert

A bug fix is not automatically a refactoring opportunity.

## Verify the Claim

Verification must match the claim.

A successful build proves the project builds. It does not necessarily prove a behavioral bug is fixed.

Where practical:
- reproduce the problem before changing code
- verify the original reproduction after the change
- add or run a regression test when appropriate
- run relevant tests
- inspect related high-risk paths

## Challenge the Result

Before claiming completion, ask:

> Assume this fix is wrong. What is the most likely reason?

Check whether:
- the symptom was hidden rather than the cause fixed
- a test is tautological
- another path has the same failure
- contradictory evidence was ignored
- the change introduced lifecycle, threading, persistence, compatibility, or API risk

## Report Material Uncertainty

For non-trivial investigations, communicate concisely using this structure:

- Observed Facts
- Assumptions / Unknowns
- Hypotheses
- Evidence
- Conclusion: VERIFIED / STRONGLY SUPPORTED / INFERRED
- Proposed or Applied Change
- Verification
- Regression Risk
- Remaining Uncertainty

A stack trace, crash report, or bug description handed to you with no other context is a non-trivial investigation by default — use this structure even if the eventual fix turns out to be small. Trivial work is work that is already fully specified and directly verifiable (e.g., "change this label text," "the failing assertion already names the exact line to flip") — not work that merely *looks* urgent or has an obvious-seeming culprit. When genuinely trivial, skip the template rather than force it — but the diagnosis step (Establish What Is Known, Classify the Conclusion) still applies whenever a cause is being chosen, not just when the final report is written.

## Never

- Invent a root cause from a stack trace alone.
- Skip the FACTS/ASSUMPTIONS/UNKNOWNS breakdown for a diagnosis just because the top frame or first error message suggests an obvious cause.
- Present a plausible explanation as a verified fact.
- Search only for confirmation of the first hypothesis.
- Ignore conflicting evidence.
- Rewrite unfamiliar legacy code solely because it looks strange.
- Assume comments are correct.
- Assume comments are wrong.
- Assume existing code is correct.
- Assume existing code is incorrect.
- Expand the scope of a fix without evidence that the expansion is needed.
- Treat compilation alone as proof that a behavioral bug is fixed.
- Hide material uncertainty.
- Add process overhead disproportionate to task risk.
