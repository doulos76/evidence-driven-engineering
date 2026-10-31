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

**Recommendation: Do not commit to the microservices migration yet.**

There is no evidence that module boundaries are the cause of slowness, that microservices will solve it, or that 10x growth requires architectural change. The order search complaint is localized; other endpoints are not slow. Splitting the system now is a high-risk, high-cost bet on an unverified hypothesis.

**Why this matters:**
- Microservices solve specific problems (independent scaling, deployment, team ownership). They create new problems (latency across boundaries, distributed state, operational complexity). The choice should be driven by measured constraints, not anticipation.
- The product lead's suggestion to split all three modules assumes dependencies and bottlenecks that haven't been identified. Splitting blindly often pushes the bottleneck elsewhere.
- You have no load forecast, no latency profile, and no evidence of what actually needs to scale.

---

## Proposed Work Plan (in order)

**Phase 1: Understand the problem (1-2 weeks)**
- Profile the slow endpoint: database query time, application logic time, serialization, I/O wait.
- Measure current load: request rate, concurrent users, latency distribution (p50/p95/p99), CPU/memory/database utilization.
- Identify the actual bottleneck (likely to be: a missing index, unoptimized query, or inefficient search logic — not module boundaries).
- Forecast 10x load: what does the database, application, and infrastructure see if all metrics scale 10x?

**Phase 2: Fix the identified bottleneck (timeline: depends on root cause)**
- If database query: optimize the query, add indexing, or consider a dedicated read replica or search index (Elasticsearch, etc.).
- If application logic: refactor the search algorithm.
- If contention: measure whether module isolation actually helps, or if a simpler fix (caching, rate limiting) is sufficient.
- Validate the fix with a before/after latency measurement.

**Phase 3: Plan scaling strategy (after Phase 1 results)**
- Revisit the microservices question with measured constraints. Example hypotheticals:
  - If search is CPU-bound, split orders to its own service and scale independently.
  - If search is database-bound, a read replica may be enough.
  - If growth spreads evenly across modules, keep the monolith and scale horizontally.

---

## What to Put in the Ticket

> **Current Blocker:** Order search endpoint is reported slow. No measurement has been performed. Microservices is a proposed solution, but we lack evidence that module boundaries are the cause, that splitting will fix it, or that 10x growth requires this architecture.
>
> **Next Step:** Profile the slow endpoint and measure current load. Identify the actual bottleneck (query plan, application logic, resource contention, or something else). Forecast 10x load against measured baseline.
>
> **Outcome:** We will have data to decide whether the fix is a query optimization, a dedicated search service, a read replica, or eventually a microservice split — and which modules, if any, need to scale independently.

Do not start the migration until Phase 1 is complete. Microservices are not a shortcut; they are a tool for a specific, measured problem.
