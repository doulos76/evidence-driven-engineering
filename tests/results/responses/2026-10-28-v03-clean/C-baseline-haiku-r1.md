---
scenario: C
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**Conclusion:**

The timing correlation is suggestive but the evidence doesn't isolate pool size as the root cause. The constant flat load (95–105 req/sec) would produce constant timeouts at 20 connections if that were truly the bottleneck. Instead, timeouts clustered in a 15-minute window correlate strongly with the accounting export start time—not with the pool reduction per se.

The actual root cause is **the combined connection demand of the API + export now exceeds the reduced pool size, and that demand was never measured.** The engineer is right that 20 is too small for the combined workload, but reverting to 40 treats the symptom, not the problem: **we don't know how many connections the export actually uses or whether 40 has sufficient margin.**

---

**Proposed next action:**

1. **Instrument the 02:00–02:15 window** to capture active database connections during export execution, separate from idle.
2. **Measure export connection footprint** (peak concurrent connections needed).
3. **Set pool size based on observed peak demand** (API + export) **+ 50% safety margin**, not on guesswork.
4. **Document baseline metrics** so the next pool-size decision is data-driven, not tribal knowledge.

Revert to 40 immediately to stop the incident, but use the next 24 hours (next export run) to instrument it. That data decides the permanent pool size.
