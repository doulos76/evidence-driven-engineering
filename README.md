# Evidence Driven Engineering (EDE)

> **Teach your coding agent not to confuse plausibility with truth.**

Evidence Driven Engineering is a lightweight engineering judgment framework for AI coding agents.

It helps an agent:

- distinguish facts from assumptions
- avoid anchoring on the first plausible root cause
- search for evidence that disproves its own hypothesis
- understand legacy context before changing code
- prefer the smallest supported change
- verify behavior before claiming success
- communicate remaining uncertainty

## Core Principles

> **Evidence before conclusions.**  
> **Falsification before confidence.**  
> **Context before modification.**  
> **Verification before claims.**

And:

> **Be strict with evidence, humble with interpretation, and skeptical of your own conclusions.**

## What EDE Is Not

EDE is not a replacement for TDD, code review, static analysis, or your development process.

It is a reasoning layer that complements them.

## Repository Status

v0.2.0 is implemented and published. `SKILL.md` is complete, and all 12
behavioral scenarios in `tests/scenarios.md` have been run and recorded —
see [Behavioral Testing](#behavioral-testing) below.

See [PRD.md](./PRD.md) for the full product requirements.

## Repository Structure

```text
evidence-driven-engineering/
├── SKILL.md
├── README.md
├── PRD.md
├── CONTRIBUTING.md
├── LICENSE
├── CHANGELOG.md
├── references/
│   ├── evidence-model.md
│   ├── examples.md
│   └── anti-patterns.md
└── tests/
    ├── scenarios.md
    └── results/
        └── *.md
```

## Example Prompts

```text
Use evidence-driven-engineering to investigate this crash.
Do not assume the top stack frame is the root cause.
```

```text
Review this legacy implementation using EDE.
Before changing it, determine what behavior it may be protecting.
```

```text
Analyze this PR using EDE.
Separate verified defects from risks, assumptions, and preferences.
```

## Installation

EDE is a standard Agent Skill (`SKILL.md` + optional supporting resources).
It's portable across any tool that supports that format — the sections
below cover the environments this repo has been tested with.

### Claude Code

Copy the skill into your personal skills directory so it's available in
every project:

```bash
mkdir -p ~/.claude/skills/evidence-driven-engineering
cp SKILL.md ~/.claude/skills/evidence-driven-engineering/
cp -r references tests ~/.claude/skills/evidence-driven-engineering/
```

Claude Code picks up personal skills automatically — no restart required
for new sessions.

### Claude.ai (web / desktop app)

Package the repo as a `.skill` file and upload it under
**Settings → Capabilities → Skills**:

```bash
python -m scripts.package_skill /path/to/evidence-driven-engineering
```

(`package_skill.py` ships with Anthropic's `skill-creator` skill; see its
docs if you don't already have it available.)

### Codex

Codex supports Agent Skills composed of a `SKILL.md` file plus optional supporting resources and scripts. Install this repository as a compatible skill bundle or copy the skill into the location used by your Codex environment.

Because Codex installation and UI details may evolve, this project intentionally keeps the skill itself portable and based on the Agent Skills format rather than relying on undocumented Codex-specific configuration.

## Behavioral Testing

`tests/scenarios.md` defines 12 adversarial scenarios (stack-trace
anchoring, legacy code removal, contradictory evidence, build-vs-fix,
trivial edits, speculative refactoring, already-verified causes, stale
comments, plus four scenarios adding authority pressure and longer, noisier
context: authoritative misdiagnosis, pressure to delete an unexplained
guard, a statistically implausible fix, and a justified-looking custom
implementation) designed to catch specific failure modes EDE targets.

Two evaluation methods are used, because they measure different things:

- **Pass/fail** — did the agent reach a defensible conclusion. Across 4
  independent runs (2 model tiers × with-skill/baseline), this has been
  **non-discriminating**: baseline behavior already avoids these specific
  failure modes at both tiers tested, so the suite functions as a
  regression guard here, not a sharp discriminator.
- **Rubric scoring (0–20)** — *how rigorously* the agent got there:
  explicit evidence labeling, named falsification attempts, explicit
  uncertainty classification, resistance to authority pressure, and more
  (`tests/rubric.md`). This is where a real, measurable gap shows up.

### EDE Rubric Benchmark

Verbatim two-pass blind grading (see `tests/rubric.md` and
`tests/results/2026-08-21-rubric-v2-full-verbatim.md`), 12 scenarios ×
with-skill/baseline, one response per condition per scenario per tier:

| Model | No Skill | EDE | Lift |
|---|---|---|---|
| Claude Sonnet 5 | 13.5 / 20 | 16.3 / 20 | **+2.8** |
| Claude Haiku 4.5 | 9.7 / 20 | 15.1 / 20 | **+5.4** |

Evaluation: verbatim response text (not summaries), graded blind to
condition (with-skill/baseline labels hidden from the grader), two
independent grading passes averaged per response, 10-item rubric scored
0–2 each. No human spot-check has been performed on this grading yet —
see `tests/results/` for the full history, including an earlier `SKILL.md`
revision where this same method found a *negative* result at the Haiku
tier, driven by the skill's structure being silently skipped on one
scenario, which motivated the format-hardening change reflected in the
numbers above.

If you change `SKILL.md`, see [CONTRIBUTING.md](./CONTRIBUTING.md) for what
to re-run and record.

## Contributing

This repository uses [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
— `main` is releasable and tagged, `develop` is the integration branch and
default branch, and work happens on `feature/*`, `release/*`, and
`hotfix/*` branches. See [CONTRIBUTING.md](./CONTRIBUTING.md) for branch
conventions and the exact command sequences.

## License

MIT
