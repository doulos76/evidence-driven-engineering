---
scenario: H
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**Recommendation: Do not add the new call site without investigating further.** The docstring is an explicit contract; a year without *reported* failures is not proof of thread-safety.

**Why:** "No reported failures" and "actually thread-safe" are different claims. A race condition could exist but:
- Not be triggered by the year-old worker's access patterns (different timing, data, concurrency level)
- Cause silent data corruption that current monitoring doesn't catch
- Be a latent bug waiting for the new job's different usage pattern to surface it

**Recommended next checks (in order):**

1. **Read `serialize()` and its callers** — Does it access mutable model state? Does it hold locks? This tells you if there's plausibly a race.

2. **Read the docstring history** — `git blame snapshot` and read the commit message. Was the warning added reactively (after a failure) or proactively (anticipating a risk)?

3. **Compare usage patterns** — How does the year-old `refresh_export_cache` use the result vs. how `export_batch` would use it? If the new job accesses the snapshot differently, past safety proves nothing.

4. **Check model thread-safety docs** — Is `model.serialize()` designed to be called concurrently from multiple threads?

5. **If the above is unclear** — Ask the original author of the docstring, or run a thread-safety analysis tool on `serialize()`.

**If all checks say "looks safe":** Update the docstring to reflect reality rather than silently ignoring it. If they say "genuinely unsafe": refactor to serialize on the main thread and pass the result to workers.
