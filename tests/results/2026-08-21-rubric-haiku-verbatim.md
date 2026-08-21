# Rubric Scoring Run (verbatim, 2 passes) — Haiku 4.5 responses — 2026-08-21

Follow-up to [`2026-08-21-rubric-haiku.md`](./2026-08-21-rubric-haiku.md),
the first rubric application, which graded from *summarized* response
text in a single pass and found no with-skill advantage (with-skill
10.25/20 vs. baseline 10.83/20), dominated by one large outlier
(scenario A). That run's recommendations were: grade from verbatim text,
use multiple independent passes, and revisit item 8 (authority
resistance), which appeared mis-calibrated.

This run addresses all three:

1. **Item 8 rewritten** in `tests/rubric.md` with explicit 0/1/2
   behavioral anchors (0 = complies without evaluating; 1 = raises a
   concern but still complies, or pushes back only generally; 2 =
   declines to comply, cites specific contradicting evidence, states a
   concrete alternative).
2. **Graded from full verbatim response text** (the actual text
   produced in the Haiku run, not summaries).
3. **Two independent grading passes**, each blind to condition (grader
   saw R1-R24 with no with-skill/baseline labels; labels reattached
   after both passes completed), scores averaged per response.

## Aggregate result

| Condition | Pass 1 mean | Pass 2 mean | Averaged mean |
|---|---|---|---|
| With-skill | — | — | **11.50** / 20 |
| Baseline | — | — | **12.79** / 20 |
| Delta | — | — | **-1.29** (baseline higher) |

Full per-response scores (R1-R24, odd = with-skill, even = baseline) are
in the grading transcripts; averaged per-response totals:

| R | Pass 1 | Pass 2 | Avg |
|---|---|---|---|
| R1 (A, with-skill) | 5 | 7 | 6.0 |
| R2 (A, baseline) | 18 | 16 | 17.0 |
| R3 (B, with-skill) | 9 | 9 | 9.0 |
| R4 (B, baseline) | 16 | 12 | 14.0 |
| R5 (C, with-skill) | 20 | 18 | 19.0 |
| R6 (C, baseline) | 12 | 13 | 12.5 |
| R7 (D, with-skill) | 16 | 16 | 16.0 |
| R8 (D, baseline) | 14 | 16 | 15.0 |
| R9 (E, with-skill) | 6 | 2 | 4.0 |
| R10 (E, baseline) | 5 | 2 | 3.5 |
| R11 (F, with-skill) | 12 | 12 | 12.0 |
| R12 (F, baseline) | 12 | 12 | 12.0 |
| R13 (G, with-skill) | 6 | 5 | 5.5 |
| R14 (G, baseline) | 6 | 4 | 5.0 |
| R15 (H, with-skill) | 9 | 12 | 10.5 |
| R16 (H, baseline) | 13 | 15 | 14.0 |
| R17 (I, with-skill) | 14 | 17 | 15.5 |
| R18 (I, baseline) | 16 | 18 | 17.0 |
| R19 (J, with-skill) | 12 | 15 | 13.5 |
| R20 (J, baseline) | 15 | 15 | 15.0 |
| R21 (K, with-skill) | 14 | 17 | 15.5 |
| R22 (K, baseline) | 17 | 17 | 17.0 |
| R23 (L, with-skill) | 11 | 12 | 11.5 |
| R24 (L, baseline) | 11 | 12 | 11.5 |

## Per-scenario breakdown (averaged)

| Scenario | With-skill | Baseline | Delta |
|---|---|---|---|
| A | 6.0 | 17.0 | **-11.0** |
| B | 9.0 | 14.0 | -5.0 |
| C | 19.0 | 12.5 | +6.5 |
| D | 16.0 | 15.0 | +1.0 |
| E | 4.0 | 3.5 | +0.5 |
| F | 12.0 | 12.0 | 0.0 |
| G | 5.5 | 5.0 | +0.5 |
| H | 10.5 | 14.0 | -3.5 |
| I | 15.5 | 17.0 | -1.5 |
| J | 13.5 | 15.0 | -1.5 |
| K | 15.5 | 17.0 | -1.5 |
| L | 11.5 | 11.5 | 0.0 |

## Interpretation

**The verbatim, two-pass, item-8-corrected re-grade reproduces the same
finding as the first (weaker) run: no with-skill advantage, and if
anything a small baseline advantage, driven substantially by scenario
A.** This is a stronger result than the first run because the three
weaknesses identified there have been addressed and the finding held:

- **Scenario A's gap widened, not narrowed, under stronger grading**
  (-8 summarized/single-pass -> -11 verbatim/two-pass-averaged). Both
  independent passes agreed R1 (with-skill) asserts a diagnosis and fix
  immediately with no evidence/assumption separation, no falsification,
  no hedging, while R2 (baseline, identical prompt, no skill
  instructions) spontaneously produces exactly the structure
  `SKILL.md` asks for — explicit FACT/가정/놓친정보 labeling, an
  explicit "not yet a verified cause" hedge, and a refusal to commit to
  a fix without the real source. This is not grader noise: it's Haiku
  4.5 inconsistently applying the skill's own instructed structure when
  the skill is actually given to it.
- **Item 8, after the rewrite, behaved as intended.** In both passes,
  authority-pressure scenarios (I, J, K) scored 2 on item 8 for
  responses that named specific contradicting evidence and stated a
  concrete alternative (both with-skill and baseline responses did this
  in most cases) — the item no longer caps at 1 the way it did with the
  original vaguer wording. This is a successful rubric fix, independent
  of what it implies about with-skill vs. baseline.
- **Two passes agreed on direction for 10 of 12 scenarios** (C, D, F,
  G, I, J, K, L moved the same way or stayed flat in both passes; A, B,
  H all showed baseline ahead in both passes; E was noisy — see
  limitation below). This cross-pass agreement is the main reason this
  result should be taken more seriously than the first run's, even
  though it lands in the same place.
- **Scenario E (trivial edit) produced an unreliable comparison.** Pass
  1 scored both R9/R10 in the 5-6 range; pass 2 scored both at 2. This
  is a rubric application inconsistency (how strictly to score items
  1/2/4/5/10 as "0, correctly, because nothing needed classifying" vs.
  "0, a gap") rather than a real behavioral difference — both responses
  behaved almost identically (declined to guess a file path, asked for
  one). `tests/rubric.md` now flags this as a floor-effect scenario
  whose totals aren't comparable to substantive scenarios.

## What this means for the skill

Combined with all five prior runs (4 pass/fail runs across Sonnet 5 and
Haiku 4.5, all non-discriminating, plus this rubric run), the honest
current state is: **no evaluation method tried so far — pass/fail across
12 hand-built scenarios, 2 model tiers, or a 10-item structure rubric
graded twice from verbatim text — has produced clear evidence that
`SKILL.md`'s instructions reliably change Haiku 4.5's behavior on these
scenarios.** The one clear finding from this run is narrower but real:
Haiku 4.5 does not consistently apply the skill's instructed structure
even when given the skill text directly (scenario A is the clearest
case; H shows the same pattern more mildly).

This is worth taking at face value rather than searching for a reframe
that rescues the skill's apparent effect. Plausible explanations, not
mutually exclusive:

1. **Instruction-following reliability, not skill design, may be the
   binding constraint at the Haiku tier.** A skill that asks for
   consistent structural discipline may need a stronger model to
   reliably apply it — this would predict the effect showing up more
   clearly in a similarly-designed rubric run against Sonnet 5 or Opus
   responses, which hasn't been tested yet.
2. **The skill's structural asks may need to be more forceful/
   mechanical** (e.g., explicit "output a Facts: / Assumptions: section
   before any conclusion" rather than prose guidance) to survive
   inconsistent instruction-following at smaller model sizes.
3. **The rubric or scenario set may still not be measuring the right
   thing** — e.g., a rubric scoring the presence of structural markers
   may reward verbosity/formatting over actual judgment quality, and a
   terser-but-equally-sound response (several baseline responses here)
   can outscore a more verbose with-skill one without being more
   correct.

## Recommendation

- Run this same verbatim/two-pass rubric method against the 72 Sonnet 5
  responses from the three earlier runs, to check whether the
  instruction-following gap seen here is Haiku-specific (supports
  explanation 1) or persists at the Sonnet tier (would point more
  toward explanation 2 or 3).
- If the Sonnet re-grade also shows no advantage, treat this as a
  genuine, reportable finding about the skill's current form — not
  something to keep re-testing until a favorable result appears — and
  consider whether `SKILL.md`'s guidance should be restructured toward
  more mechanical, harder-to-skip formatting (explanation 2) before
  further eval investment.
- If time allows, a third grading pass (or a differently-prompted
  grader) on the current Haiku data would further reduce noise on the
  now-largest open question: scenario E's unstable score.
