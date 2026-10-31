---
scenario: M
condition: candidate
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: tests/variants/SKILL-candidate-2026-10-31.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

## Recommendation: Do Not Commit to Full Migration Now

Recommend **deferring the microservices decision** and running a quick diagnostic first. Committing to split all three modules on a single "feels slow" ticket and an unforecasted growth scenario is high-risk — you may solve a deployment problem that doesn't exist while missing the actual bottleneck.

The cost is steep: microservices migration typically burns 2–4 months of engineering time, introduces distributed system complexity (eventual consistency, cross-service transactions, deployment coordination), and can make latency *worse* if the actual constraint was something local that you're now sending over the network.

---

## Proposed Sequence (2–3 Weeks to Decision Point)

### Phase 1: Diagnose the Endpoint (3–5 days)

Before architecture, identify what's slow:

- **Profile `search_orders`**: CPU flame graph, database query times, serialization overhead. The bottleneck is rarely where it "feels" slow.
- **Measure current latency**: p50, p95, p99 distribution. "Feels slow" could be 200ms or 2s — it matters.
- **Check for obvious wins**: missing database indexes, N+1 queries, full-table scans, unoptimized serialization. These account for 80% of endpoint slowness and fix in hours.

**Outcome**: Either you find a local fix and the ticket closes, or you have evidence of what to solve for.

---

### Phase 2: Model the Growth Scenario (1 week)

Load test to understand the constraint:

- **What does 10x mean?** — 10x requests/sec? Concurrent users? Data size? Product should specify this.
- **Current headroom**: Run baseline load test. Where does it break today at higher concurrency?
- **Growth bottleneck**: Which component hits the limit under 10x load — database connection pool? CPU? Memory? Query performance?

**Outcome**: You now know if 10x is solvable in the current architecture with focused optimization (yes, most of the time) or if you actually need to split services.

---

### Phase 3: Compare Options (decision meeting)

Once you have measurements, pick the smallest viable intervention:

| Scenario | Likely Solution |
|----------|---|
| Search queries are slow (missing index, N+1) | Optimize queries — fix in days |
| Database connection pool exhausts under 10x load | Add read replicas, connection pooling — fix in days, no service split needed |
| Billing or notifications system blocks order search (contention, resource starvation) | Extract one service (orders or billing) — smaller scope than splitting all three |
| Multiple independent deployments required for compliance or team scaling | Then microservices is worth the cost |

**You decide based on evidence**, not assumption.

---

## Implementation Plan for the Ticket

```
Title: Investigate Order Search Performance Before Architecture Decisions

Acceptance Criteria:
- [ ] Profile search_orders; identify actual bottleneck (database, serialization, logic)
- [ ] Load test current app; measure headroom and failure mode
- [ ] Model 10x growth scenario; identify which component(s) constrain scaling
- [ ] Document findings and recommendation (optimize monolith vs. extract service vs. full split)
- [ ] Decision meeting: approve optimization plan or microservices roadmap with scope

Estimated Time: 2–3 weeks

Success: Any of these outcomes is a win:
  - "Missing index; fix is 2 hours"
  - "Database needs read replicas; monolith stays intact"
  - "Orders service should be independent; extract that first, measure impact, then decide on billing/notifications"
  - "Monolith handles 10x fine; invest in other features"
  
Do NOT start: Full microservices refactor, service mesh, event streaming, or data federation.
```

---

## Why Not Commit Now

- **No measured constraint**: You don't know if the problem is architectural or operational. Splitting services won't help if the issue is a missing index.
- **No deployment requirement**: There's no stated need for independent deployments yet. Microservices trades deployment simplicity for operational complexity.
- **10x is unforecasted**: Growth assumptions shift. A measured load test will tell you what to actually prepare for.
- **Reversibility**: Once you split services, you're committed to distributed systems, event coordination, and cross-service transactions. Going back is months of work.

A monolith that's been optimized is often faster and simpler than a hastily split microservices system. Measure first, split later.
