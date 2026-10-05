---
scenario: M
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Recommendation

**Do not commit to the microservices migration now.** The current information is insufficient to justify an irreversible architectural change. Instead, implement a two-phase approach:

1. **Phase 1 (1-2 weeks):** Gather evidence about the actual bottleneck
2. **Phase 2:** Make a documented architecture decision with measured constraints in hand

---

## Evidence Analysis

### FACTS:
- Customer reports order search is slow; other screens appear normal
- Application is currently a working modular monolith
- Functional tests pass
- No external requirement mandates independent module deployment

### ASSUMPTIONS:
- "Slow" is a subjective user perception without measured baseline or SLA
- "10x growth" is an anticipated scenario, not a measured forecast
- The slowness is caused by architectural boundaries (not verified)
- Microservices will solve both the current latency and future scaling (unproven in this context)

### INFERENCES:
- The search slowness is localized to one endpoint, suggesting the problem may be order-specific (query complexity, data volume, index design, database contention) rather than architectural
- If module boundaries were the bottleneck, the application would be noticeably slow across all modules, not isolated to search

### UNKNOWNS (Critical):
- **Measured latency:** What is p50, p95, p99 search response time? What SLA are users expecting?
- **Load profile:** Current request rate, concurrent users, and headroom at peak?
- **Root cause:** Is it slow I/O (database queries), CPU-bound compute, network serialization, or lock contention?
- **Scaling mode:** Will 10x growth be uniform across modules, or will specific modules (e.g., billing, orders) see different scaling pressure?
- **Load forecast accuracy:** Is the 10x projection based on validated product/market assumptions, or is it a planning placeholder?

### CONFLICTING EVIDENCE:
- Modular design *within a monolith* suggests the team has already thought about boundaries. Extracting to microservices does not automatically improve latency if the bottleneck is internal to the orders module (e.g., query performance, data schema).

### CLAIMS (Requiring Verification):
- "Other screens seem fine" — does this mean we have measured baselines for non-search endpoints?
- "Microservices should solve both the slow endpoint and the scaling problem" — this conflates two different problems. Latency and throughput scaling may require different solutions.

---

## Why This Matters: Architecture Risk

The proposed change is **high-risk and irreversible** without evidence:

- **Microservices introduces operational complexity:** service discovery, distributed tracing, eventual consistency, deployment coordination, failure modes across network boundaries.
- **It solves a different problem:** microservices excel at independent scaling and deployment. They do *not* automatically reduce latency of a single endpoint—especially if that endpoint's slowness is caused by a query, algorithm, or data modeling choice *within* the orders module.
- **Scope creep:** splitting all three modules at once multiplies risk and gives no quick win to validate the approach.
- **No rollback:** once deployed to production under load, a failed architecture change is expensive to undo.

---

## Phased Recommendation

### Phase 1: Diagnosis (1–2 weeks)

Gather evidence to answer: *Is the bottleneck inside the orders module, at the module boundary, or in shared infrastructure?*

**Immediate steps:**

1. **Profile the slow endpoint in production or under realistic load:**
   - Measure end-to-end latency (p50, p95, p99).
   - Break down time spent in database, serialization, application logic.
   - Compare with non-slow endpoints (e.g., notifications endpoint).

2. **Inspect the search implementation:**
   - Review the `orders.search()` query. Are there missing indices? Inefficient SQL patterns? N+1 queries?
   - Check whether filtering logic is pushing computation to the application layer instead of the database.

3. **Measure current capacity:**
   - What is the current request rate to the search endpoint?
   - What is the database connection pool utilization?
   - Are there any error logs or timeouts?

4. **Validate the 10x growth assumption:**
   - Which modules will scale? Will order *queries* increase 10x, order *writes* 10x, or both?
   - Is there a load forecast tied to product milestones, or is this a rough planning number?

### Decision Point After Phase 1

Once you have profiles, ask:

- **If the bottleneck is a query or index issue:** Optimize the query. Cost: weeks. Risk: low. Impact: search latency improves immediately.
- **If the bottleneck is database connection saturation:** Add connection pooling, read replicas, or caching. Cost: weeks. Risk: low-medium. Impact: scales search and other read endpoints.
- **If the bottleneck is within the orders module's application logic:** Refactor the search algorithm or data structure. Cost: varies. Risk: low if tests are good. Impact: immediate.
- **If the bottleneck is at a module boundary (e.g., notification service calls from search):** Remove the call, cache the result, or make it async. Cost: days. Risk: low. Impact: immediate.

**None of these require microservices.** If Phase 1 reveals that the search endpoint calls notification or billing services synchronously, you have evidence for extracting at least the orders service. Until then, you are redesigning for an architectural problem you have not proven.

### Phase 2: Architecture Decision (If Needed)

If Phase 1 shows that:
- The bottleneck cannot be solved with query optimization or caching, *and*
- The load forecast is now validated (e.g., backed by a signed contract or product roadmap), *and*
- Splitting the orders module from billing/notifications would measurably reduce latency or unblock independent scaling,

then proceed with a **documented decision record** that names:
- The measured constraint (e.g., "orders module generates 8,000 queries/sec; database connection pool is exhausted at 5,000 queries/sec").
- Why the current design cannot meet it (e.g., "connection pool cannot be scaled further without architectural change").
- Why the chosen option (orders microservice) is better than alternatives (e.g., database sharding, caching, async queries).
- What evidence would trigger revisiting the decision (e.g., "if 10x growth doesn't materialize, revert to monolith").

---

## Implementation Steps (If Committed to Phase 2)

Assuming Phase 1 confirms a need:

1. **Extract orders service first, in isolation:**
   - Do not split billing and notifications yet. Orders is the bottleneck.
   - Keep billing and notifications in the monolith until they show independent scaling pressure.

2. **Establish service boundaries at the data level:**
   - Ensure orders owns all order-related tables. Billing and notifications read order data via API (not shared database).
   - This is the highest-value change. It unblocks independent scaling and deployment.

3. **Plan for rollout risk:**
   - Canary the orders service with 5–10% of traffic. Measure latency, errors, and customer impact.
   - Do not proceed until the new service beats the monolith on the measured metric (e.g., p95 latency).

4. **Defer notification and billing services:**
   - Wait for evidence of their own scaling bottleneck before extracting them.
   - They may never need to be separated.

---

## Summary

| Aspect | Current State | Recommendation |
|--------|---------------|-----------------|
| **Commit to migration?** | No | Gather 2 weeks of evidence first |
| **Immediate action** | None | Run profiles on the slow endpoint |
| **If search latency is a query issue** | — | Optimize query; stay monolith |
| **If search latency is module-induced** | — | Extract orders service; keep others |
| **If growth forecast is unvalidated** | — | Do not use it to justify architectural change |
| **Decision record** | None | Create one before Phase 2, naming constraints and unknowns |

The smallest evidence-supported change is to *diagnose the actual bottleneck*, not to *redesign the entire architecture*. Once you know where time is spent, the path forward becomes clear—and often cheaper than you expected.
