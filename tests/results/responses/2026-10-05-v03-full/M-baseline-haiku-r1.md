---
scenario: M
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Recommendation: Do Not Commit to Microservices Migration Now

**Status:** Not ready to proceed. Commit to a profiling phase first.

This decision lacks the evidence required to justify a microservices migration:

- **No root cause identified.** The complaint is "order search feels slow," but we have no latency distribution, tracing, or profiling data. Slowness could stem from the search query itself, database load, external API calls within the orders module, or infrastructure limits—each requires different fixes.
- **No bottleneck isolated to module boundaries.** Microservices solve cross-service coordination costs and independent scaling. If the problem is a poorly optimized query or N+1 queries within the orders module, separating it into a service won't help and adds network latency instead.
- **10x growth is a scaling problem, not necessarily a services problem.** A monolith can scale 10x if the bottleneck is removed (e.g., add caching, optimize queries, scale the database). Splitting services prematurely adds complexity—deployment coupling, data consistency issues, debugging difficulty—without confirming this will move you toward the goal.
- **No deployment independence requirement.** You stated there's no external need to deploy modules independently. Microservices' primary value is independent scaling and deployment; without this requirement, you're trading simplicity for operational overhead.

## Recommended Plan (Next 2 Weeks)

### Phase 1: Profile and Measure (Required)

1. **Install production observability** (1–2 days)
   - Add application profiling (flame graphs) to the order search handler.
   - Log database query timing and connection pool metrics.
   - Instrument the entire request path: entry, module calls, database, serialization.

2. **Capture production traffic** (3–5 days of traffic, parallel with step 1)
   - Measure p50, p95, p99 latency of order search requests.
   - Break down latency by component: database query, orders.search() logic, JSON serialization, network I/O.
   - Identify request rate and concurrent users today (baseline for scaling math).

3. **Analyze and hypothesize** (1 day, after data is captured)
   - Is latency dominated by database queries, module logic, or I/O?
   - Does latency scale linearly with result count or cursor position?
   - Are there resource bottlenecks (CPU saturation, memory, connection pool exhaustion)?

### Phase 2: Options Analysis (1 day, after Phase 1)

Based on findings, compare:
- **Option A (Monolith optimizations):** Add caching, query optimization, database indexing, or read replicas.
  - Effort: days–weeks. Risk: low. Scaling capacity: 3–5x typical.
- **Option B (Selective services):** Extract only the measured bottleneck (e.g., if it's billing lookups in orders, move billing to a service).
  - Effort: weeks. Risk: medium. Scaling: targeted to that service.
- **Option C (Full microservices):** Split all three modules.
  - Effort: months. Risk: high (deployment, consistency, debugging complexity). Scaling: independent, but adds latency.

### Acceptance Criteria for Committing to Migration

Do not commit to microservices until you have:
1. ✓ Measured that a single module or process boundary is the confirmed bottleneck.
2. ✓ Quantified the scaling cost (e.g., "database load will hit 80% capacity at 3x growth").
3. ✓ Validated that modular optimizations (caching, indexing) won't reach 10x scaling needs.
4. ✓ Designed service boundaries based on data, not assumed module boundaries (orders + billing might belong together if they're queried together).

## Revised Ticket Language

**Title:** Order search performance investigation—establish baseline and root cause

**Description:**

We've received reports that order search is slow, and we're planning for 10x growth. Before committing to a microservices migration, we need to:

1. Measure current latency (p50, p95, p99) and resource bottleneck (database, CPU, I/O).
2. Identify which component is the constraint.
3. Evaluate whether monolith optimizations or selective services would suffice.

**Outcome:** A decision document showing the bottleneck, the cost of 10x growth without changes, and the recommended architecture for that scale.

**Not** committing to full services split until evidence justifies it.

---

**Rationale for this approach:**

Microservices are a high-cost solution (debugging, deployment, data consistency, operational burden). They shine when you need independent scaling, independent deployment, or cross-organizational team boundaries. None of those apply yet. The cost of being wrong—splitting prematurely—is 2–3 months of integration rework, not the cost of waiting two weeks to measure. Measure first; decide second.
