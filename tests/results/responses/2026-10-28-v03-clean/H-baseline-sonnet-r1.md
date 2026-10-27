---
scenario: H
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**Recommendation: don't call `snapshot()` from the new export job yet.** Either gate it on the checks below, or have the worker hand off to the main thread in the meantime.

**Why neither argument settles it**

- **The docstring** is an explicit contract from the author: "Main-thread only." It's the only direct evidence in the packet, and it says no. But it's a claim without a rationale. It may reflect a real hazard in `serialize()` or the model, or it may be a conservative note that's now stale. Without the source or history, we can't tell which. It does shift the burden: the caller needs to show it's safe, not the other way around.
- **The year-old worker** is weak evidence. Absence of reported failures doesn't show absence of races, because:
  - Races in serialization are typically intermittent and may produce a subtly inconsistent snapshot, not a crash. Nobody would report that, and the cache consistency audit that could detect it doesn't exist.
  - Call site #2 already violates the docstring, so it is itself a possible latent bug, not a precedent.
  - The new job differs in load. It iterates over a batch, so it holds the model longer and probably runs concurrently with UI edits more often than a single-model cache refresh does. Safe at one scale doesn't carry over.

**What the packet supports:** the contract says unsafe, the usage evidence is inconclusive, and the implementation is unknown. That's not enough to approve a violation of a documented constraint.

**Next checks, in order of value**

1. **Read `serialize()` and what it touches.** Look for iteration over mutable collections, lazy-loaded fields, caches, Qt/UI-toolkit objects, thread-affine resources, or shared global state.
2. **Check the docstring's history** (`git blame`/`log -S`). The commit or PR that added "Main-thread only" may state the reason. Also ask the author.
3. **Find the model's threading model.** Is it mutated on the main thread only? Is there a lock, or an intended copy-on-read pattern?
4. **Audit call site #2.** Compare cached entries against fresh main-thread snapshots for the same model version. This tests whether the existing worker has actually been producing bad data.
5. **If the code is unsafe or still unclear,** use one of these designs:
   - Dispatch `snapshot()` to the main thread (queued call or signal), then do the heavy export work off-thread on the returned data.
   - Add a locked or immutable-copy API on the model for background readers.
6. **If it's safe,** update the docstring and add a test that runs `snapshot()` concurrently with mutations. Then fix or confirm call site #2 as well.

I can dig into `serialize()` and the history if you point me at the repo; the working directory here isn't a git repository and doesn't contain this code.
