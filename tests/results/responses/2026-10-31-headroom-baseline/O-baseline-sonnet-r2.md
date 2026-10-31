---
scenario: O
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-31
skill_rev: 7c00e4e
variant: none
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

## Root cause

The race is real. `get()` does an unlocked check-then-act on `self._data`, so two threads can both see `None` and both call `_load()`. The lock inside `_load` only serializes the two disk reads. It doesn't stop the second load, and the second thread's result overwrites the first's. Any caller that already holds a reference to, or has mutated, the first dict is now looking at an orphan.

That matches runs 8812 and 8830 (two threads in `_load`, one waiting on `_lock`).

It does not explain run 8851. There was one thread in `_load`, no waiter, and the assertion failed in the test body. So I'd call this the likely cause of the flake, not a confirmed one. Two other gaps:

- All three failures were on node-pool-b, but you haven't looked at which pool the 15 passing runs used. If pool-a passes just as rarely as pool-b, the "2 cores" story is weaker.
- Nothing has been run with a changed cache, so there's no evidence yet that fixing this removes the failures.

## Patch

```python
class SessionCache:
    def __init__(self):
        self._data = None
        self._lock = threading.Lock()

    def get(self, key):
        data = self._data
        if data is None:
            with self._lock:
                if self._data is None:          # re-check under the lock
                    self._data = self._load()
                data = self._data
        return data.get(key)

    def _load(self):
        return read_sessions_from_disk()        # no lock here; caller holds it
```

Two things to check before applying it:

- If anything else calls `_load()` directly, it now runs without the lock.
- If the class has other methods that mutate `self._data`, they need the same lock. I only saw `get`.

## What I'd do before merging

1. **Reproduce locally.** Write a stress test that starts N threads behind a `threading.Barrier`, all calling `get()` on a fresh cache, and asserts `_load` ran exactly once. It should fail on the old code and pass on the new. Restricting CPUs (e.g. `taskset -c 0,1`, or a 2-CPU container) makes it closer to node-pool-b.
2. **Look at run 8851.** A failure with no concurrent `_load` means either a second bug or a different mechanism. Read the actual assertion message. If it fails the same way as the other two, the single-thread dump may just have been captured at a different moment.
3. **Check the passing runs by pool.** Confirm failures really cluster on node-pool-b and aren't just a sample of three.
4. **Run the patched test on node-pool-b repeatedly**, say 50 to 100 times. At a 1-in-5 failure rate, 20 clean runs is about a 1% chance by luck, so that's the minimum for any confidence.

If the stress test reproduces the double-load and the patched CI runs are clean, merge. If 8851's failure turns out to have a different signature, merge the fix anyway since the race is a genuine bug, but keep the flake ticket open rather than calling it solved.
