---
scenario: M
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

# Recommendation: Do Not Commit to Microservices Migration

**Do not proceed with the proposed split.** The decision lacks the evidence needed to justify the migration's cost and complexity.

## Evidence-First Analysis

**FACTS:**
- One endpoint (order search) is reported as slow by users
- Other screens perform acceptably
- Current monolith works and passes tests
- No profiling, latency distribution, or trace data for the slow endpoint
- No load forecast or measured capacity headroom
- No external requirement for module independence

**UNKNOWNS (material):**
- Where is the slowness? (search algorithm, database query, serialization, external calls, or module boundaries?)
- What are the current P50/P95/P99 latencies and throughput?
- What is actual capacity headroom today?
- Will 10x growth materialize, and when?
- Will the current bottleneck remain a bottleneck under 10x load, or does it decouple?

**CONFLICTING EVIDENCE:**
- Slowness is localized to one endpoint, not systemic across modules
- Other screens are fine, suggesting the problem is likely algorithmic or database-level, not architectural
- Proposal assumes microservices solves scaling, but monoliths scaled to billions of requests per day; scaling and slowness are different problems

**THE CORE ISSUE:**
The proposal conflates three separate problems—slowness now, anticipated growth, and module coupling—and assumes one solution (microservices) solves all three. There's no evidence the slowness is caused by module boundaries or that splitting will fix it.

---

## Next Steps for Planning Ticket

### Phase 1: Diagnosis (1–2 weeks; ~5 engineering days)

**Minimal evidence to gather before any architectural decision:**

1. **Profile the order search endpoint**
   - Reproduce the slow behavior in staging with production-like data volume
   - Capture: endpoint latency, database query time, JSON serialization time, network time
   - Identify which component dominates (e.g., "70% database, 20% serialization, 10% application logic")

2. **Measure current capacity**
   - Current request rate on order search (req/sec)
   - Current P50/P95/P99 latency
   - Capacity headroom (CPU, memory, database connections, disk I/O)
   - Current concurrent user count

3. **Validate the 10x growth assumption**
   - Get actual forecast data from marketing (timeline, magnitude, breakdown by feature)
   - Model capacity needs under that load (e.g., "10x = 50→500 req/sec")

**Outcome:** Root cause (e.g., "unindexed search query" or "N+1 in order serialization"), not architectural problem.

---

### Phase 2: Fix the Root Cause (Timeline depends on Phase 1 diagnosis)

**Most slowness is not architectural.** Common fixes:
- Add database index on search filters
- Optimize the query (pagination, projection, connection pooling)
- Batch or cache expensive lookups
- Reduce payload size

**Re-measure after fix.** Does the endpoint meet acceptable latency at current load? If yes, you've solved the immediate problem for ~10–50x less effort than a microservices migration.

---

### Phase 3: Capacity Planning (After Phase 2)

With actual measurements:
- Compare projected load (10x) against measured capacity headroom after fix
- If headroom is still insufficient, then propose scaling strategies (horizontal monolith, read replicas, caching, query optimization)
- Only if the monolith cannot be scaled further *and* module coupling is measured to be a blocker, revisit microservices as an option

---

## Why Not Microservices Yet?

| Claim | Evidence | Status |
|-------|----------|--------|
| "Module boundaries are slowing search" | None; other modules are fine | Unverified |
| "Microservices will scale to 10x" | None; scaling depends on the actual bottleneck | Unverified |
| "We need independent deployment" | No stated requirement | Unverified |
| "The endpoint is slow" | User report, no measurement | Verified but cause unknown |

Microservices are high-complexity (data consistency, deployment, monitoring, latency). They solve verified deployment or scaling constraints, not vague performance fears.

---

## Risk If You Skip Diagnosis

- **Spend 2–3 months migrating, then discover:** The search was slow because of a missing index. You've now added network latency and eventual consistency across services.
- **Build the wrong boundaries:** Without tracing real request paths and data flows, you may split services in ways that require frequent cross-service calls (defeating the purpose).
- **Discover the 10x never came:** Microservices complexity has become a permanent sunk cost.

---

## What to Write in the Ticket

```
Title: Order Search Performance — Diagnosis Before Architecture

Goal: Understand why order search is slow and measure capacity headroom.

Phase 1 (1–2 weeks):
  [ ] Profile order search endpoint (isolate bottleneck)
  [ ] Measure current load and latency distribution (P50/P95/P99)
  [ ] Measure capacity headroom (CPU, memory, DB connections)
  [ ] Get validated 10x growth forecast from marketing (timeline, magnitude)

Decision gate: If Phase 1 shows a fixable bottleneck (query, cache, index),
  fix it and re-measure. Do not commit to microservices until capacity
  planning shows the fix is insufficient for projected load.

Phase 2 (if needed):
  Optimize root cause. Re-measure. If headroom remains insufficient,
  model monolith scaling options before considering module split.
```

**Do not assign microservices work until Phase 1 is complete.**
