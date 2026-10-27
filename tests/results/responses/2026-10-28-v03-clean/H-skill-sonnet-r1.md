---
scenario: H
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**Recommendation:** Don't call `snapshot()` from `export_batch` yet. Neither argument establishes safety, and the docstring is the only explicit constraint in the packet. Hold the new call site until the checks below are done, or route it through the main thread in the meantime.

```
FACTS:
- snapshot()'s docstring says "Main-thread only. Do not use from a worker thread."
- Call site #2 already calls it from a background thread, and has for a year.
- Ops reports no failures from call site #2 in that time.
- No cache consistency audit exists.
- The packet doesn't include serialize()'s source, the docstring's history, or any thread-safety docs for the model.
ASSUMPTIONS:
- "No reported failures" means no failures occurred (unverified; it only means none were noticed or reported).
- The new batch job has a load and timing profile similar to the existing worker (unverified).
INFERENCES:
- Either the docstring is stale/overly cautious, or call site #2 is a latent violation. The packet can't tell which.
UNKNOWNS:
- Whether serialize() reads mutable state, and whether the main thread mutates the model concurrently.
- Why the docstring was written (a real constraint such as thread-affine state, or defensive wording).
- Whether corrupted cache entries would be detectable at all.
CONFLICTING EVIDENCE:
- The docstring forbids worker-thread use, yet a worker has used it for a year without reported incident.
CLAIMS:
- Teammate A: the docstring settles it. Teammate B: the year-old worker proves it is safe.
```

**Hypotheses and evidence**
- **H1: The docstring reflects a real constraint.** Supporting: it's an explicit, deliberate statement. Missing: its rationale and history.
- **H2: The docstring is stale or overcautious.** Supporting: a year without reported failures. Contradicting or weakening: no audit, and silent corruption (a torn read, a stale cache entry) would not produce an error report.

**Why each teammate's argument falls short**
- **"The docstring settles it":** A docstring is a claim. It's the best available warning and it should block the change by default, but it can't show that the constraint still holds or ever did.
- **"The old worker proves it":** Absence of reports is weak evidence. It fits both hypotheses, and the audit that could separate them doesn't exist. The new job also differs from the old one: it loops over many models in a batch, which means a longer window for racing against main-thread mutation. Even if #2 is safe, that doesn't carry over to this workload.

Conclusion: STRONGLY SUPPORTED

(This applies to "the packet does not establish safety." Whether `snapshot()` is actually thread-safe remains unknown.)

**Next checks, cheapest first**
1. Read `serialize()` and what it touches: shared mutable state, lazy-loaded fields, thread-local or UI-framework objects, caches.
2. Run `git log -S"Main-thread only"` / `git blame` on the docstring and read the linked commit or PR for the reason.
3. Find who mutates the model and from which threads. If the main thread can mutate it while a worker serializes, that's the concrete risk.
4. Check whether call site #2 holds a lock or otherwise guarantees the model is quiescent. If so, the same guarantee must be reproduced for the batch job.
5. Audit the cache by re-serializing a sample of entries on the main thread and comparing against what the worker stored. That would give the evidence "no failures" currently lacks.
6. If the code looks questionable, write a stress test that mutates a model on the main thread while a worker snapshots it repeatedly.

**Safe options if the export can't wait**
- Take the snapshot on the main thread (or under a documented lock) and hand the serialized result to the worker.
- Don't change the docstring or the existing worker until the evidence is in, since that would turn an unverified belief into an apparent fact.

**Regression risk:** If H1 is true, the new job could produce silently inconsistent exports, and no failure signal would reveal it.

**Remaining uncertainty:** Everything hinges on `serialize()` and the mutation patterns, neither of which is in the packet. If you paste `serialize()` and the model's mutation sites, I can narrow this to a firmer decision.
