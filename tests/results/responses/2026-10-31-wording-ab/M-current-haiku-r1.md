---
scenario: M
condition: current
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: SKILL.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

**RECOMMENDATION: Do not commit to the microservices migration on this information. Plan a diagnostic phase instead.**

The proposal treats a plausible explanation (module boundaries cause slowness) as a verified fact. You have one customer complaint with no telemetry, no profile of the endpoint, no evidence linking the slowness to module coupling, and no measured growth forecast. Microservices adds substantial operational complexity — deployment orchestration, distributed tracing, eventual consistency, network failure modes — that is justified only by evidence that it solves a real, measured problem.

The 10x growth assumption and the endpoint slowness may not even be related problems. "Other screens seem fine" suggests a specific bottleneck in the search endpoint, not a systemic capacity crisis.

---

## Recommended Next Steps for the Planning Ticket

**Phase 1: Diagnosis (1–2 weeks)**

- **Profile the order search endpoint.** Measure latency distribution, request traces, and identify where time is spent: database queries, serialization, business logic, I/O. Instrument the actual code path.
- **Measure current state.** Current request rate, concurrent users, CPU/memory/database metrics, database connection pool exhaustion, and query execution times. You need a baseline.
- **Validate the complaint.** Is it consistently slow or intermittent? For which query patterns? Does it correlate with load, time of day, or data volume?

**Expected outcome:** A specific root cause (e.g., unindexed query, missing cache, N+1 queries, inefficient algorithm) that you can reason about.

---

**Phase 2: Growth Forecast (1 week)**

- Get marketing's actual growth timeline, distribution across endpoints, and concurrent user projections. "10x growth" is not a technical specification.
- Map growth to capacity: Will the current infrastructure hit a bottleneck, and where?

**Expected outcome:** A measured constraint, not an anticipation.

---

**Phase 3: Compare Options (1 week)**

Once you know what is slow and where you'll hit capacity limits, compare at minimum:

1. **Optimize the specific bottleneck** (index, cache, query rewrite, algorithm). Lowest cost, fastest win.
2. **Scale the monolith** (read replicas, connection pooling, vertical scaling, caching layer). May solve both problems with far less risk.
3. **Minimal split** (extract orders service only if evidence suggests it gains something; keep shared database if data coupling is tight). Only if optimization and monolith scaling are insufficient.
4. **Full microservices** (orders, billing, notifications as separate deployments, separate databases). Only if you have evidence that module boundaries are the actual bottleneck and that operational complexity is justified.

Compare using actual constraints from Phase 1 and Phase 2, not anticipation.

---

**Phase 4: Plan Incrementally**

- The rollout order, deployment strategy, and service boundaries emerge from evidence, not from guessing.
- If you do migrate, start with the orders service (highest leverage for the measured complaint).
- You do not need independent deployability today — there is no external requirement. Microservices is an operational choice, not a mandatory architecture.

---

## What NOT to Do

- Do not commit to splitting all three modules now.
- Do not assume the slowness is caused by module boundaries without profiling.
- Do not treat "10x growth is expected" as a measured constraint — measure it.
- Do not use the anticipated growth as justification to redesign before understanding the actual bottleneck.

---

**Summary for the ticket:** "Diagnose the order search bottleneck and measure the growth forecast before architecture decisions. If optimization of the monolith is sufficient, do that first. Microservices is the most expensive option and should be chosen only if evidence rules out simpler alternatives."
