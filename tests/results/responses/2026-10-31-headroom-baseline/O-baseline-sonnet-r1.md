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

## Root cause (probable, not confirmed)

`get()` has a check-then-act race. The `_data is None` check happens outside the lock, and the lock only wraps the disk read inside `_load`. Two threads that both see `None` each run `_load` (the second just waits on the lock), and each then assigns `self._data`. The second assignment replaces the first dict. If anything wrote to or held a reference to the first dict in between, that state is lost. That would explain a failure in a session-restore test. It also fits the thread dumps in runs 8812 and 8830, and the 2-core runners make unlucky interleavings more likely than on your 8-core machine.

The race is real, but the evidence doesn't yet show it causes this flake:

- **Run 8851 doesn't fit.** One thread in `_load`, no waiter, and the assertion failed in the test body. That is not the two-thread signature, so it may be a different failure.
- **Only the failing runs were inspected.** The 15 passing runs weren't, so you don't know whether passing runs also show two threads in `_load`. If they do, the dump isn't distinguishing anything.
- **All three failures are on node-pool-b.** That is consistent with the 2-core theory, but also with anything else specific to that pool, such as disk speed, a stale session dir, or a different image.
- **Nothing has been tried with a changed cache.** The theory is untested.

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
        return read_sessions_from_disk()        # lock now held by caller
```

The lock moves out of `_load` because `threading.Lock` isn't reentrant, and keeping it in both places would deadlock. If other code reads `_data` or `_load` directly, check those call sites. The local `data` variable avoids re-reading `self._data` after the check.

## Before merging

1. **Look at run 8851 on its own.** Find out why the test body failed with no second thread present. If the cause differs from the other two, there may be a second bug.
2. **Compare against passing runs.** Check which pool they ran on, and whether you can get the same thread dumps or logs from them.
3. **Reproduce deterministically.** Add a short `sleep` or a `threading.Barrier` inside `_load` and call `get()` from two threads. It should fail on the old code and pass on the new. Also try running the test pinned to 2 CPUs locally (for example in a container with `--cpus=2`).
4. **Soak the patch on node-pool-b.** At a 1-in-5 failure rate, 20 clean runs would happen by chance only about 1% of the time (0.8²⁰), so 20 to 30 consecutive passes is meaningful evidence.
5. **Check for writers.** Search for anything that mutates `_data` after load. If something does, it also needs to be thread-safe.

The patch is correct on its own merits and low-risk, so merging it today is reasonable. But I wouldn't close the flaky-test ticket until step 4 passes, and I wouldn't say "fixed" in the PR description before then.
