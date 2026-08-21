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

This repository currently contains the v0.1 product specification and an initial `SKILL.md` draft.

See [PRD.md](./PRD.md) for the full product requirements.

## Suggested Repository Structure

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

## Codex

Codex supports Agent Skills composed of a `SKILL.md` file plus optional supporting resources and scripts. Install this repository as a compatible skill bundle or copy the skill into the location used by your Codex environment.

Because Codex installation and UI details may evolve, this project intentionally keeps the skill itself portable and based on the Agent Skills format rather than relying on undocumented Codex-specific configuration.

## License

MIT
