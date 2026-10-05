---
scenario: H
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Establish What Is Known

**FACTS:**
- `snapshot()` has a docstring stating "Main-thread only. Do not use from a worker thread."
- Call site #2 (background worker) has been deployed for one year.
- No reported failures from call site #2 in the last year.
- `snapshot()` calls `model.serialize()`.
- `export_batch()` would be a second background worker calling `snapshot()`.

**ASSUMPTIONS:**
- Teammate citing the docstring assumes the implementation enforces thread-safety constraints.
- Teammate citing the year-old worker assumes no-failures implies the constraint is not actually enforced or not necessary.
- The absence of reported failures indicates the deployed code path is safe.

**UNKNOWNS:**
- **Critical:** The source and thread-safety properties of `serialize()` are not provided.
- Is `serialize()` thread-safe? Does it mutate shared state? Acquire locks?
- Why was the docstring written? Was it based on known unsafe patterns, or is it overly cautious?
- Has call site #2 exercised the same code paths and concurrency patterns as `export_batch()` would?
- Are failures in call site #2 masked? (e.g., silently dropped cache entries, corrupted serialization, exceptions caught and logged elsewhere).
- Cache consistency audit: none available—we cannot verify whether call site #2 has silently introduced subtle corruption.

**CONFLICTING EVIDENCE:**
- The docstring forbids worker threads; the year of no failures suggests the forbiddance is either not enforced or unnecessary.
- No reported failures vs. no audit: absence of *reported* issues does not equal absence of issues, especially for data consistency problems that may be subtle.

**CLAIMS:**
- The docstring is a truth about the intended contract (not yet verified against the implementation).
- The year-old worker "proves it is safe" (this claim conflates "no reported failures" with "verified thread-safe").

## Hypotheses and Evidence

**Hypothesis A:** `serialize()` is thread-unsafe. Call site #2 happened to avoid triggering the race condition (lucky timing, or insufficient concurrency load). **Risk if wrong:** `export_batch()` introduces a latent threading bug.
- Supporting: Docstring explicitly forbids worker threads.
- Contradicting: One year of production use without reported failures.
- Missing evidence: Thread-safety analysis of `serialize()`, cache audit, concurrency load profile of both call sites.

**Hypothesis B:** `serialize()` is thread-safe. The docstring is overly cautious or documents a legacy constraint no longer relevant. **Risk if wrong:** False confidence that the code is safe when it is not.
- Supporting: One year of no reported failures.
- Contradicting: Why write "Main-thread only" if it is not a real constraint?
- Missing evidence: Author's intent for the docstring, thread-safety documentation, source of `serialize()`.

**Hypothesis C:** `serialize()` has subtle thread-safety bugs that have not manifested in call site #2 but may appear under the load pattern of `export_batch()` (e.g., higher concurrency, different timing).
- Supporting: Docstring warning; subtle concurrency bugs are common.
- Contradicting: Year of no reported failures.
- Missing evidence: Stress testing, load profiles, timing-sensitive race conditions.

## Recommendation

**Do not call `snapshot()` from `export_batch()` without further evidence.**

The docstring is the strongest evidence we have about the intent. One year of no reported failures is *weak* evidence of thread-safety because:
1. It does not rule out silent data corruption (call site #2 may have corrupted cache entries undetected).
2. It does not rule out rare race conditions that have not triggered under the actual load of call site #2.
3. Different concurrency patterns in `export_batch()` (batch size, timing, scheduling) may expose issues that call site #2 avoided.

## Next Checks (in priority order)

1. **Read the source of `serialize()`** and the model's implementation. Ask:
   - Does it mutate shared state? Acquire locks? Use thread-local storage?
   - Is there any synchronization? Any documented assumptions about caller threads?

2. **Inspect thread-safety documentation** for the model class. If none exists, this is a red flag.

3. **Audit the cache** from call site #2:
   - Are cached entries correct? Compare them to on-demand serialization of the same models.
   - Is there evidence of corruption (truncation, partial updates, mismatched IDs)?

4. **Stress-test call site #2** with the load pattern `export_batch()` would use (e.g., concurrent calls, batch sizes). If failures appear, the docstring is vindicated.

5. **Check the git history** of `snapshot()` and `serialize()`:
   - Why was the docstring written? Was there a bug or a known issue?
   - Have thread-safety changes been made to `serialize()` after the docstring was written?

6. **If evidence is insufficient:** Add a thread-safe wrapper around `snapshot()` (e.g., acquire a lock or run on the main thread via a message queue) rather than calling it directly from `export_batch()`. This is the minimal change that eliminates the risk.

## Conclusion: INFERRED

One year of no reported failures is not sufficient evidence to override the docstring. The decision is riskiest for data consistency bugs, which are often silent. Without access to the implementation, the safest recommendation is to avoid the call unless the source of `serialize()` demonstrates thread-safety or an audit of call site #2 shows no corruption.

Confidence label: **INFERRED** — the most likely explanation fits the evidence (the docstring reflects a real constraint), but the year of no failures is contradictory. Only the source code can resolve this with a VERIFIED or STRONGLY SUPPORTED conclusion.
