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

**Recommendation: Do not commit to a microservices migration on this information. Measure first.**

The proposal conflates two separate concerns — a localized performance complaint and anticipated growth capacity — and assumes architecture is the root cause without evidence. This is backward: you measure to *discover* whether architecture is your constraint, not assume it before measuring.

## What We Actually Know

- One endpoint reports slow; others are fine (localized problem)
- No profile, latency data, or trace of the endpoint
- No load test, capacity forecast, or evidence the current architecture fails at 10x
- No measured constraint that module boundaries are creating

## The Risk of Committing Now

A microservices migration is:
- **Irreversible** — distributed system complexity, eventual consistency tradeoffs, operational overhead
- **Expensive** — months of refactoring, testing, deployment orchestration, monitoring
- **Confidence-destroying** — you'll ship a slower, more fragile system if the actual constraint was something else (a slow query, missing index, N+1, lock contention)

If the order search is slow because of a query plan issue or missing index, splitting it into a microservice makes it worse, not better.

## Measure Before Deciding

Propose a short measurement sprint (1–2 weeks):

1. **Profile the endpoint** — CPU, memory, database queries, lock contention, cache behavior
2. **Load-test the current architecture** — what request rate and concurrency cause degradation? How far below 10x are you?
3. **Identify the constraint** — Is it database throughput, query efficiency, CPU, memory, or cross-module call overhead?
4. **Test the hypothesis** — If you suspect module boundaries cause slowness, instrument the internal calls and measure their latency vs. total request time

## Decision Framework (After Measurement)

Once you have data:

- **If the bottleneck is database throughput:** Consider read replicas, caching, or query optimization within the monolith first. Splitting into microservices requires separate databases, which breaks shared data semantics and adds consistency overhead — only do this if you've proven the benefit outweighs the cost.
- **If the bottleneck is compute or cache locality:** Vertical scaling, caching, or targeted refactoring may be cheaper than a full migration.
- **If the bottleneck is truly module boundaries:** Then microservices becomes a reasonable option. Plan the split *for the modules that are actually constraining you*, not all three.
- **If the current architecture scales fine:** Don't migrate. Revisit in 12 months when you have real 10x load.

## Implementation Plan (If You Commit to Measuring)

```
Sprint 1: Establish Facts
  - Run a profile on the order search endpoint
  - Load-test the current monolith (ramp to 10x current load)
  - Measure database query times, connection pool saturation, cache hit rates
  - Document latency distribution and identify the bottleneck
  
Outcome Decision Gate:
  - If no measurable constraint: ship the endpoint optimization, monitor
  - If constraint is external (database, network): optimize there first
  - If constraint is module boundaries: proceed to Option A or B below

Option A (If Only One Module Needs to Scale):
  - Extract the constrained module into a sidecar service
  - Keep the others monolithic (lower operational risk)
  - Rollout: sidecar in shadow mode → canary → full cutover

Option B (If Multiple Modules Constrain Each Other):
  - Extract the top bottleneck first (measure to identify it)
  - Keep others monolithic until they also show constraint
  - Rollout incrementally: highest-impact module → others as needed
```

## What to Tell the Product Lead

"Order search is slow, and we want to grow 10x. Microservices *might* help, but only if module boundaries are actually the constraint. We don't know that yet. A 1–2 week profile and load test will tell us whether to optimize the current design, add caching, fix queries, or split into services. Committing to a full migration without that data risks shipping a slower, more fragile system. Let's measure first—that's what will actually unblock us."
