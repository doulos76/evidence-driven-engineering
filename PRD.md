# PRD — Evidence Driven Engineering (EDE)

> **Evidence before conclusions.  
> Falsification before confidence.  
> Context before modification.  
> Verification before claims.**

## 1. Document Status

- Product: Evidence Driven Engineering (EDE)
- Type: Codex Agent Skill / Engineering Judgment Framework
- Version: v0.1.0 PRD
- Primary target: OpenAI Codex
- Secondary target: Agent Skills compatible tools
- Distribution: Public GitHub repository
- License recommendation: MIT
- Status: Draft for implementation

---

## 2. Product Summary

**Evidence Driven Engineering (EDE)** is an engineering judgment skill for AI coding agents.

Its purpose is not to teach an agent merely to write code, test code, or follow a development workflow. EDE teaches the agent **how to decide what is true before acting**.

The core problem EDE addresses is that coding agents can produce plausible explanations and confidently act on them before the underlying cause has been sufficiently verified.

EDE introduces a disciplined reasoning loop:

1. Observe facts.
2. Separate facts from assumptions and unknowns.
3. Generate competing hypotheses when uncertainty exists.
4. Search for evidence that can falsify the leading hypothesis.
5. Reconstruct the context of existing behavior before changing it.
6. Choose the smallest evidence-supported change.
7. Verify actual behavior.
8. Challenge the result.
9. Report remaining uncertainty.

EDE should improve debugging, code review, legacy maintenance, incident analysis, refactoring, and architecture decisions without forcing a heavyweight process onto trivial changes.

---

## 3. Why This Product Exists

AI coding agents are very good at generating plausible explanations.

Plausibility is not verification.

Common failure patterns include:

- inferring a root cause from a stack trace alone
- anchoring on the first plausible explanation
- searching only for confirming evidence
- rewriting unfamiliar legacy code because it looks strange
- treating comments, tickets, or old documentation as ground truth
- assuming existing code is either correct or incorrect
- expanding a bug fix into unrelated refactoring
- declaring success because the project builds
- hiding uncertainty behind confident language

These are not primarily syntax or coding problems.

They are **engineering judgment problems**.

EDE exists to introduce epistemic discipline into agentic software engineering.

---

## 4. Product Philosophy

### 4.1 Core Principle

> **Do not treat plausible explanations as verified facts.**

### 4.2 Engineering Maxim

> **Be strict with evidence, humble with interpretation, and skeptical of your own conclusions.**

### 4.3 Four Pillars

#### Evidence before conclusions

Do not choose a cause before establishing what is actually known.

#### Falsification before confidence

Do not only search for evidence that supports the preferred explanation. Actively search for evidence that could make it wrong.

#### Context before modification

Existing behavior may be accidental, outdated, or incorrect—but it may also be protecting a constraint that is no longer obvious.

#### Verification before claims

A successful build proves compilation. It does not necessarily prove the bug is fixed or the root cause was correct.

---

## 5. Goals

EDE MUST:

1. Separate observations from interpretations.
2. Clearly distinguish facts, assumptions, inferences, unknowns, and conflicting evidence.
3. Avoid premature root-cause claims.
4. Encourage competing hypotheses when material uncertainty exists.
5. Require active falsification of the leading hypothesis.
6. Encourage investigation of callers, tests, history, and constraints before altering unfamiliar behavior.
7. Prefer minimal evidence-supported changes.
8. Evaluate regression risk.
9. Verify behavior rather than relying only on compilation.
10. Communicate residual uncertainty honestly.
11. Adapt investigation depth to task risk.
12. Remain useful across languages, frameworks, and platforms.
13. Be small enough to combine with other specialized skills.

---

## 6. Non-Goals

EDE is NOT:

- a replacement for TDD
- a replacement for static analysis
- a replacement for code review
- a complete SDLC methodology
- a mandatory multi-agent orchestration system
- a bug tracker
- a Git workflow
- a project-management framework
- an architecture style
- a requirement to produce long reports for every code change
- a requirement to generate multiple hypotheses when the cause is already directly proven

EDE should complement existing engineering practices rather than compete with them.

---

## 7. Target Users

### Primary

Developers using Codex for:

- debugging
- code review
- legacy maintenance
- refactoring
- incident analysis
- architecture decisions
- production issue investigation

### Secondary

Teams that want a consistent engineering reasoning standard for AI-assisted development.

---

## 8. Primary Use Cases

### UC-01 — Debugging an uncertain crash

Given:
- a stack trace
- partial logs
- unfamiliar code

EDE should prevent the agent from claiming the top stack frame is automatically the root cause.

Expected behavior:
- identify verified observations
- produce plausible competing causes
- inspect surrounding code paths
- attempt to falsify the strongest hypothesis
- fix only after evidence is sufficient

### UC-02 — Legacy code modification

Given:
- strange-looking old implementation
- user asks to simplify or fix it

Expected behavior:
- inspect call sites and tests
- inspect version/platform constraints when relevant
- inspect git history when useful and available
- explain what behavior the implementation may be protecting
- avoid broad rewrite without evidence

### UC-03 — Pull request review

Expected behavior:
- distinguish verified defects from concerns or style preferences
- identify assumptions in the review
- challenge high-impact conclusions
- prioritize correctness and regression risk over cosmetic preference

### UC-04 — Production incident

Expected behavior:
- create an evidence timeline
- separate symptom, trigger, contributing factor, and root cause
- avoid retrospective certainty
- state what remains unknown
- recommend follow-up instrumentation where evidence is insufficient

### UC-05 — Architecture decision

Expected behavior:
- distinguish current constraints from assumed future needs
- identify evidence supporting the proposed architecture
- examine alternative explanations/options
- avoid redesigning architecture in response to a local bug without evidence

---

## 9. Risk-Adaptive Depth

A major product requirement is that EDE MUST NOT turn trivial work into bureaucracy.

### LOW Risk

Examples:
- typo
- text copy change
- obvious compiler error
- localized padding adjustment
- mechanical rename with full compiler coverage

Expected EDE depth:
- lightweight
- verify change
- no forced hypothesis table

### MEDIUM Risk

Examples:
- bug with multiple plausible causes
- unfamiliar module
- behavioral refactor
- API integration issue

Expected EDE depth:
- facts vs assumptions
- competing hypotheses when useful
- evidence check
- regression review
- explicit verification

### HIGH Risk

Examples:
- concurrency
- persistence/data migration
- security
- production incident
- financial logic
- destructive operation
- large legacy subsystem
- authentication
- distributed consistency
- irreversible behavior

Expected EDE depth:
- full investigation workflow
- explicit falsification
- context reconstruction
- rollback/regression analysis
- strong completion gate
- explicit residual uncertainty

The skill should infer risk from task context. It should not ask the user to classify risk unless necessary.

---

## 10. Evidence Model

EDE should use the following evidence taxonomy internally and, for non-trivial investigations, expose it when useful.

### FACT

Directly observed or independently verified.

Examples:
- a reproducible crash
- test output
- runtime log
- source code behavior
- compiler output
- confirmed API documentation

### ASSUMPTION

A working belief not yet verified.

Example:
- "This function is only called from the main actor."

### INFERENCE

A conclusion derived from facts but not directly observed.

Example:
- "The object probably crossed an actor boundary."

### UNKNOWN

Information that may materially change the conclusion.

Example:
- whether the issue exists in previous app versions

### CONFLICTING EVIDENCE

Evidence that does not fit the current explanation.

This category is important. The agent must not silently discard it.

### CLAIM

A statement made by a source that should not automatically be treated as truth.

Sources may include:
- comments
- tickets
- commit messages
- developer recollections
- documentation
- incident notes

A claim can become a fact only when independently verified or directly supported.

---

## 11. EDE Core Workflow

### Phase 1 — Observe

Collect observable facts before explaining them.

Questions:
- What actually happened?
- What can be reproduced?
- What do logs or tests directly show?
- What is the smallest indisputable statement?

### Phase 2 — Classify

Separate:
- Fact
- Assumption
- Inference
- Unknown
- Conflicting Evidence
- Claim

### Phase 3 — Generate Competing Hypotheses

When the cause is materially uncertain, create at least two plausible hypotheses.

For each:

- supporting evidence
- contradicting evidence
- missing evidence
- cheapest useful test

Do not invent artificial alternatives if the cause is already directly demonstrated.

### Phase 4 — Falsify

For the leading hypothesis ask:

- What observation would make this wrong?
- What evidence should exist if this hypothesis is true?
- Is that evidence present?
- Could another explanation fit the same observations?

The agent should actively seek disconfirming evidence.

### Phase 5 — Reconstruct Context

Before modifying unfamiliar or legacy behavior inspect, where useful and available:

- callers and call sites
- tests
- git history
- blame/history around suspicious lines
- issue/PR context
- neighboring implementations
- lifecycle assumptions
- platform/version constraints
- persistence/migration constraints
- concurrency boundaries

Key question:

> **Why might a reasonable engineer have written this code this way?**

This question is not an assumption that the old code is correct. It is a method for discovering hidden constraints.

### Phase 6 — Decide

Classify the current conclusion as one of:

- **VERIFIED** — directly demonstrated by evidence
- **STRONGLY SUPPORTED** — multiple evidence sources support it and meaningful alternatives were weakened
- **INFERRED** — best current explanation but not sufficiently proven

Avoid fake numeric confidence percentages unless there is a real measurement basis.

### Phase 7 — Change Minimally

Prefer the smallest change that:

- addresses the supported cause
- preserves unrelated behavior
- minimizes regression surface
- is easy to verify
- is easy to revert

Principle:

> **A bug fix is not automatically a refactoring opportunity.**

### Phase 8 — Verify

Verification must match the claim.

Examples:

Claim: "It compiles."
Evidence: successful build.

Claim: "The bug is fixed."
Evidence should include:
- original reproduction no longer fails
- relevant regression test or equivalent validation
- related paths checked where appropriate

Claim: "No regression."
Evidence:
- relevant test suite / targeted behavioral checks

### Phase 9 — Challenge the Result

Before claiming completion:

> **Assume this fix is wrong. What is the most likely reason?**

Check:
- Did the fix suppress the symptom instead of fixing the cause?
- Could the test be tautological?
- Is there another code path with the same failure?
- Did the change create a lifecycle/threading/persistence issue?
- Did the investigation ignore conflicting evidence?

### Phase 10 — Report

For non-trivial work, report:

- Observed Facts
- Assumptions / Unknowns
- Hypotheses
- Evidence
- Conclusion classification
- Change
- Verification
- Regression Risk
- Remaining Uncertainty

Do not force this format onto simple changes.

---

## 12. Required Agent Behavior

EDE MUST instruct Codex to:

- continue investigating when available evidence does not support a confident root-cause claim
- use available repository tools before guessing
- prefer reading code/tests/history over asking the user questions that the repository can answer
- preserve explicit user requirements even if EDE would otherwise prefer deeper investigation
- keep changes scoped
- clearly label unsupported assumptions
- revise conclusions when new evidence contradicts them

EDE MUST NOT instruct Codex to expose private chain-of-thought.

The skill should request concise evidence summaries and decision rationale, not hidden reasoning traces.

---

## 13. Never Rules

The skill MUST explicitly prohibit the following:

- Invent a root cause from a stack trace alone.
- Present a plausible explanation as a verified fact.
- Search only for confirmation of the first hypothesis.
- Ignore conflicting evidence.
- Rewrite unfamiliar legacy code solely because it looks strange.
- Assume comments are correct.
- Assume comments are wrong.
- Assume existing code is correct.
- Assume existing code is incorrect.
- Expand the scope of a fix without evidence.
- Call a build success proof that a behavioral bug is fixed.
- Hide material uncertainty.
- Manufacture multiple hypotheses when the cause is already verified.
- Introduce process overhead disproportionate to task risk.

---

## 14. Interaction With Existing Engineering Practices

### TDD

EDE complements TDD.

For reproducible bugs:
- regression test first is strongly preferred where practical

But EDE should not require TDD for every task.

### Code Review

EDE distinguishes:
- verified defect
- likely defect
- risk
- preference

### Static Analysis

Static analyzer output is evidence, not automatically root cause.

### Documentation

Documentation is a source. It may be stale.

### Git History

History is contextual evidence. Old commit messages are claims, not unquestionable truth.

---

## 15. Skill Package Requirements

The repository SHOULD have the following structure:

```text
evidence-driven-engineering/
├── SKILL.md
├── README.md
├── PRD.md
├── LICENSE
├── CHANGELOG.md
├── references/
│   ├── evidence-model.md
│   ├── examples.md
│   └── anti-patterns.md
└── tests/
    └── scenarios.md
```

### Required

`SKILL.md`
- concise operational instructions
- YAML metadata
- optimized for agent use, not human explanation

`README.md`
- human-facing explanation
- installation guidance
- examples

`PRD.md`
- full product specification

### Optional but recommended

`references/`
- deeper material that does not need to remain in the main skill prompt

`tests/scenarios.md`
- adversarial examples used to evaluate whether the skill changes agent behavior

---

## 16. Codex Skill Design Requirements

The skill follows the Agent Skills folder convention:

```text
evidence-driven-engineering/
└── SKILL.md
```

`SKILL.md` must begin with metadata similar to:

```yaml
---
name: evidence-driven-engineering
description: Evidence-first engineering judgment framework for debugging, code review, legacy maintenance, incident analysis, refactoring, and architecture decisions. Use when causes are uncertain, changes are risky, or existing behavior may have hidden constraints.
---
```

The description should make automatic activation likely for:
- debugging
- production incidents
- unfamiliar code
- legacy changes
- code review with uncertain correctness
- high-risk refactors

It should NOT activate unnecessarily for trivial text or mechanical edits.

---

## 17. Proposed SKILL.md Behavioral Skeleton

The implementation should contain approximately these sections:

1. Core Principle
2. When to Apply
3. Risk-Adaptive Depth
4. Evidence Taxonomy
5. Investigation Workflow
6. Minimal Change Rule
7. Verification Gate
8. Completion Challenge
9. Output Guidance
10. Never Rules

Target:
- concise enough to load efficiently
- strong enough to materially change agent behavior
- detailed reference material moved into `references/`

---

## 18. Evaluation Plan

EDE should be evaluated against baseline Codex behavior.

### Scenario A — Stack Trace Anchoring

Prompt:
- provide stack trace with top frame that is not root cause

Pass:
- agent does not assert top frame is root cause without supporting evidence

### Scenario B — Strange Legacy Code

Prompt:
- ask agent to simplify weird compatibility code

Pass:
- agent checks callers/tests/history/version constraints before deleting behavior

### Scenario C — Confirmation Bias

Prompt:
- provide evidence supporting H1 plus subtle evidence contradicting H1

Pass:
- agent surfaces contradictory evidence

### Scenario D — Build Is Not Fix

Prompt:
- create bug where project builds after change but runtime behavior remains wrong

Pass:
- agent does not declare bug fixed based only on build success

### Scenario E — Trivial Edit

Prompt:
- change a string

Pass:
- agent does not generate a heavyweight investigation report

### Scenario F — Speculative Refactor

Prompt:
- bug can be fixed in one line, but surrounding architecture is messy

Pass:
- agent fixes the supported issue and does not opportunistically rewrite architecture

### Scenario G — Already Verified Cause

Prompt:
- failing test directly demonstrates incorrect branch condition

Pass:
- agent does not manufacture fake competing hypotheses merely to satisfy process

---

## 19. Acceptance Criteria

MVP is complete when:

- [ ] repository contains a valid `SKILL.md`
- [ ] skill has name and description metadata
- [ ] skill states the four EDE pillars
- [ ] skill implements risk-adaptive depth
- [ ] skill distinguishes facts from assumptions/unknowns
- [ ] skill includes falsification behavior
- [ ] skill includes context reconstruction before legacy changes
- [ ] skill prefers minimal evidence-supported changes
- [ ] skill requires verification proportional to the claim
- [ ] skill reports remaining uncertainty
- [ ] skill avoids fake numerical confidence
- [ ] skill does not force heavyweight workflow for trivial work
- [ ] README explains installation and usage
- [ ] at least seven behavioral test scenarios exist
- [ ] public repository contains a license
- [ ] examples contain no proprietary code or private data

---

## 20. MVP Scope

### v0.1

Single core EDE Skill.

Focus:
- debugging
- legacy changes
- code review
- incident reasoning

No subskills yet.

Reason:
A single core skill is easier to evaluate and avoids unclear skill-selection behavior.

### v0.2

Add reference playbooks:

- debugging
- code-review
- legacy-investigation
- incident-analysis

These should be references or lightweight playbooks before becoming independent skills.

### v0.3

Add:
- architecture decision playbook
- structured evidence receipt
- sample CI/evaluation harness
- measured comparison against baseline agent behavior

---

## 21. Future Opportunities

Possible future components:

```text
EDE
├── Core Judgment
├── Debugging Playbook
├── Code Review Playbook
├── Legacy Investigation
├── Incident Analysis
├── Architecture Decision
└── Evaluation Harness
```

Potential integrations:
- Crashlytics
- GitHub Issues / PRs
- CI logs
- observability platforms
- ADR generation
- incident postmortems

These are future directions, not MVP requirements.

---

## 22. Open Source Positioning

Recommended positioning:

> **Evidence Driven Engineering is a lightweight engineering judgment framework for AI coding agents. It helps agents distinguish evidence from assumption, challenge their own hypotheses, understand existing context before modifying code, and verify behavior before making claims.**

Avoid positioning EDE as:
- "the correct way to develop software"
- "a replacement for TDD"
- "a complete autonomous engineering system"

The strongest differentiator is **epistemic discipline**.

---

## 23. README Tagline Candidates

Recommended:

> **Teach your coding agent not to confuse plausibility with truth.**

Alternative:

> **Engineering judgment for AI coding agents.**

Alternative:

> **Evidence before conclusions. Verification before claims.**

---

## 24. Codex Implementation Prompt

The following prompt can be given directly to Codex after this PRD is added to an empty repository:

```text
Implement the Evidence Driven Engineering (EDE) Agent Skill described in PRD.md.

Requirements:
- Treat PRD.md as the source of product requirements.
- Create a production-quality public GitHub repository.
- Implement SKILL.md using the Agent Skills format.
- Keep SKILL.md operational and concise; move deeper explanations to references/.
- Create README.md with purpose, philosophy, installation, usage examples, and limitations.
- Create references/evidence-model.md, references/examples.md, and references/anti-patterns.md.
- Create tests/scenarios.md containing the behavioral scenarios from the PRD plus expected pass/fail criteria.
- Add MIT LICENSE and CHANGELOG.md.
- Do not invent unsupported Codex-specific configuration files.
- Do not make this a heavyweight SDLC framework.
- Preserve the core differentiator: evidence classification, competing hypotheses when warranted, falsification, context reconstruction, minimal change, verification, and explicit uncertainty.
- Make investigation depth risk-adaptive.
- Ensure trivial edits remain lightweight.
- Review the final repository against every acceptance criterion in PRD.md before claiming completion.
```

---

## 25. Definition of Done

EDE v0.1 is done when a developer can:

1. clone the repository
2. install/copy the skill into a compatible Agent Skills environment
3. ask Codex to debug or inspect an uncertain engineering problem
4. observe materially different behavior from a baseline prompt:
   - less premature certainty
   - clearer evidence separation
   - active falsification
   - more context-aware edits
   - smaller changes
   - stronger verification
5. use the skill without excessive overhead for trivial work

---

## 26. Closing Principle

EDE is not primarily about making an AI agent think longer.

It is about making the agent **earn its conclusions**.

> **Evidence before conclusions.  
> Falsification before confidence.  
> Context before modification.  
> Verification before claims.**
