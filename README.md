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

v0.1.0 is implemented and published. `SKILL.md` is complete, and all 8
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

`tests/scenarios.md` defines 8 adversarial scenarios (stack-trace anchoring,
legacy code removal, contradictory evidence, build-vs-fix, trivial edits,
speculative refactoring, already-verified causes, stale comments) designed
to catch specific failure modes EDE targets.

Each scenario has been run with-skill vs. baseline (no skill) and the
results recorded under `tests/results/`. Current finding: at the Sonnet 5
model tier, baseline behavior already avoids these specific failure modes,
so the suite currently functions as a **regression guard** rather than a
sharp discriminator — see `tests/results/2026-08-21-run.md` and
`2026-08-21-run-cfh.md` for the full writeup, including where a measurable
with-skill vs. baseline gap did show up (structured evidence labeling and
explicit falsification, not the final recommendation) and suggestions for
designing harder scenarios.

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
