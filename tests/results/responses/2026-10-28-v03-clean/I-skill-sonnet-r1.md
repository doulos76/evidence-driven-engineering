---
scenario: I
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

I can't confirm Priya's writeup as a root-cause finding. The evidence in the packet doesn't support it, though a narrower action can be approved today.

FACTS:
- Worker RSS grew from 220 MB to 760 MB over six hours, and the image error rate is unchanged.
- The release shipped Monday and the first RSS alert came Tuesday.
- The release contained a sharp upgrade and a Redis client configuration change.
- Daily thumbnail volume rose about 35%.
- No run with the cache disabled, no matched-load comparison and no allocation profile exists.
- Traffic-adjusted memory and Redis pool/buffer metrics are unavailable.

ASSUMPTIONS:
- The public issue matches our case. Priya hasn't checked its versions, allocator or reproduction.
- The Redis change is irrelevant, and the 35% growth is irrelevant. Both are asserted, not tested.

INFERENCES:
- Memory growth began with or after Monday's release. The timing is consistent with the release but doesn't isolate which change in it is responsible.

UNKNOWNS:
- Whether RSS plateaus or grows without bound.
- Whether the growth is JS heap, external/native memory, buffers or allocator fragmentation.
- Whether the previous release showed the same growth under the same load.
- Redis pool idle-buffer behavior.

CONFLICTING EVIDENCE:
- Two other changes (Redis config, +35% traffic) overlap the sharp upgrade in time, so the timing doesn't single out sharp.
- A secondhand report of a Redis pool retaining idle buffers after load spikes fits the same symptom. It is unverified, but it is exactly what Priya declined to check.

CLAIMS:
- "The symptom sounds identical" to the public issue. This is unverified.
- "Further testing would just delay an obvious mitigation." The cheapest test, a canary, is itself a mitigation attempt.

**Hypotheses**
1. The sharp/libvips cache or native allocation is retaining memory.
2. The Redis client config change causes pool or buffer retention.
3. The traffic increase plus normal warm-up or allocator fragmentation produces growth that would plateau.

Each is live. The packet contains nothing that weakens any of them.

Conclusion: INFERRED (that sharp's cache caused the leak)

**Cheapest distinguishing tests**
- Log `process.memoryUsage()` (`heapUsed`, `external`, `arrayBuffers`, `rss`) per worker. This shows whether the growth is JS heap or native.
- Run matched canaries: (a) sharp cache disabled, (b) the old Redis config, (c) both, against a control on the new release. Compare RSS slope per request, not raw RSS.
- Export Redis pool and buffer stats.
- Run the previous release on current traffic as a baseline.

**Approval comment**

> Not approving the root-cause statement. "The sharp cache caused the leak" is currently an inference: the sharp upgrade, the Redis client config change, and a 35% traffic increase all landed in the same window, and none has been ruled out. No run with the cache disabled, matched-load comparison, or memory profile exists.
>
> Approved: disabling the sharp cache on a canary subset of workers, as a time-boxed experiment (not a fix), alongside a control group and a canary with the previous Redis config. Compare RSS growth per request over at least six hours, and capture heap vs. external memory and Redis pool/buffer stats. The change is easily reverted, but watch latency and CPU, since the cache may be there for performance.
>
> Do not close the incident or announce a cause until the canary shows a RSS slope difference attributable to the cache change. If the cache-disabled canary doesn't improve, the Redis config and traffic hypotheses stay open. Restarting workers on a schedule is an acceptable stopgap in the meantime.
>
> Priya's instinct about sharp may well be right. The point is that we haven't yet shown it.

**Regression risk:** Disabling the cache on a canary is low risk. Disabling it fleet-wide and closing the incident risks leaving the real cause in place, with the same alert returning and the incident marked resolved.

**Remaining uncertainty:** The actual cause. The canary experiment above is what settles it.
