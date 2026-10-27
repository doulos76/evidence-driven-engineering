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

v0.3.0 is implemented and published. `SKILL.md` is complete, and all 13
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
├── TODO.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── markdown-link-check.json
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── CODEX_HANDOFF.md
├── scripts/
│   ├── check_test_record.py
│   ├── package_skill.py
│   └── validate_skill.py
├── references/
│   ├── examples.md
│   └── anti-patterns.md
└── tests/
    ├── scenarios.md
    ├── rubric.md          (v2: structure and substance scored separately)
    ├── rubric-v1.md       (superseded; graded every run through 2026-10-28)
    ├── tools/regrade.py
    └── results/
        ├── README.md
        └── 2026-08-21-*.md
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
# tests/ contains evaluation records, not runtime resources.
cp -r references ~/.claude/skills/evidence-driven-engineering/
```

Claude Code picks up personal skills automatically — no restart required
for new sessions.

### Claude.ai (web / desktop app)

Package the repo as a `.skill` file and upload it under
**Settings → Capabilities → Skills**:

```bash
python3 scripts/package_skill.py        # Run from the repo root; the .skill file is created there.
```

The script lives in `scripts/` in this repo.

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
  (`tests/rubric-v1.md`; v2, `tests/rubric.md`, scores structure and
substance separately). This is where a measurable gap shows up.

### EDE Rubric Benchmark

Current run (`SKILL.md` at `7c00e4e`, 2026-10-28, **clean environment**):
verbatim two-pass blind grading (rubric v1, `tests/rubric-v1.md`; see
`tests/results/2026-10-28-rubric-v03-clean-env.md`), 13 scenarios ×
with-skill/baseline, one response per cell per tier (two for scenarios A
and G). The responses were generated with no user-level instructions,
memory, plugins or hooks in context:

| Model | No Skill | EDE | Lift |
|---|---|---|---|
| Claude Sonnet 5.5 | 17.6 / 20 | 19.1 / 20 | **+1.5** |
| Claude Haiku 4.5 | 14.9 / 20 | 16.8 / 20 | **+2.0** |

How to read this: the skill is at or above baseline in most scenarios at
both tiers, with no over-processing of the trivial-edit scenario. **About
80% of the Sonnet lift and two thirds of the Haiku lift sit on two rubric
items — evidence classification and uncertainty classification — i.e. on
making the structure and confidence label explicit.** The items that
measure substance (falsification, scope, verification, authority
resistance) barely move. The rubric cannot tell whether that explicitness
reflects better engineering or only better labeling. A first human spot-check
(one reader, four response pairs) found the same conclusions and actions in
all four pairs, judged the content equal on one pair and better with the skill
on two, and overall read the skill as improving labeling and structure more
than content — suggestive, not conclusive. The numbers are not directly comparable to the v0.2.0
benchmark below (different model versions, regenerated baselines, a
different grader and skill-delivery method), and pass/fail was not rerun for
this run.

An earlier full run on 2026-10-05 (`tests/results/2026-10-05-rubric-v03-full-verbatim.md`,
Sonnet +0.1, Haiku +2.3) was generated in an environment that carried the
maintainer's own instructions asking for fact/assumption separation; its
baselines were inflated and it is superseded by the clean run above.

Previous benchmark (v0.2.0, `SKILL.md` v2, 12 scenarios, 2026-08-21,
`tests/results/2026-08-21-rubric-v2-full-verbatim.md`):

| Model | No Skill | EDE | Lift |
|---|---|---|---|
| Claude Sonnet 5 | 13.5 / 20 | 16.3 / 20 | **+2.8** |
| Claude Haiku 4.5 | 9.7 / 20 | 15.1 / 20 | **+5.4** |

Evaluation: verbatim response text (not summaries), graded blind to
condition (with-skill/baseline labels hidden from the grader), two
independent grading passes averaged per response, 10-item rubric scored
0–2 each. A single-reader human spot-check of four pairs is recorded in
`tests/results/2026-10-28-human-spotcheck-materials.md`. See
`tests/results/` for the full history, including an earlier `SKILL.md`
revision where this same method found a *negative* result at the Haiku
tier, driven by the skill's structure being silently skipped on one
scenario, which motivated the format-hardening change.

After any `SKILL.md` change, these numbers describe the preceding revision
and remain reference values until the benchmark is rerun.

If you change `SKILL.md`, see [CONTRIBUTING.md](./CONTRIBUTING.md) for what
to re-run and record. See [TODO.md](./TODO.md) for known follow-up work,
including a human spot-check of the LLM grading above that hasn't been
done yet.

## Contributing

This repository uses [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
— `main` is releasable and tagged, `develop` is the integration branch and
default branch, and work happens on `feature/*`, `release/*`, and
`hotfix/*` branches. See [CONTRIBUTING.md](./CONTRIBUTING.md) for branch
conventions and the exact command sequences.

## License

MIT
