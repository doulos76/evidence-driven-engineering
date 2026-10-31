---
scenario: Q
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-31
skill_rev: 7c00e4e
variant: none
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

I don't think the file handle is the leak. Your own profile points at `_seen_ids`.

## Why not `export_report`

- `export_report` was called **0 times** in 48 h, so it can't have leaked anything.
- Open file descriptors stayed **flat at 38**. A leaked handle per call would make that climb.
- The growth is in `dict` (41 MB to 1,730 MB) and `str` (22 MB to 910 MB), while "others" is flat (61 MB to 63 MB). That is the shape of a dict that gains one entry per event.
- `handle_event` ran 6.3M times. That is roughly 270 B of dict and 144 B of str per event, which is plausible for an id string plus a timestamp per entry.

The `export_report` bug is still real (no close, so data may not flush and the fd leaks), but it's a separate fix and it isn't what restarts your service every two days.

## Fix

```python
# service.py
import time
from collections import OrderedDict

SEEN_TTL_SECONDS = 3600      # set to your real dedupe window
SEEN_MAX_ENTRIES = 500_000   # hard cap as a safety net

_seen_ids = OrderedDict()    # id -> received_at, insertion-ordered

def _evict(now):
    # Events arrive roughly in time order, so the oldest entries are at the front.
    while _seen_ids:
        _, ts = next(iter(_seen_ids.items()))
        if len(_seen_ids) > SEEN_MAX_ENTRIES or now - ts > SEEN_TTL_SECONDS:
            _seen_ids.popitem(last=False)
        else:
            break

def handle_event(event):
    _seen_ids[event.id] = event.received_at
    _evict(time.time())      # assumes received_at is epoch seconds
    return process(event)

def export_report(path):
    with open(path, "w") as f:
        f.write(render_report())
```

Assumptions to adjust:
- `received_at` is epoch seconds. If it's a `datetime`, compare against `datetime.now(...)` instead.
- Events are roughly time-ordered. If they aren't, the cap still bounds memory, but the TTL eviction will be imprecise.
- If `handle_event` runs on multiple threads, guard `_seen_ids` with a lock.

## What I'd check

1. **Who reads `_seen_ids`?** In the snippet it is write-only. Grep for other uses. If nothing reads it, delete it. If something does dedupe against it, the TTL must be at least as long as the longest redelivery or replay window you need to catch.
2. **Confirm the source of growth.** Run `tracemalloc` (or `objgraph.show_growth()`) in staging under replayed traffic and check that the top allocation sites are the `_seen_ids[...] = ...` line. Also export `len(_seen_ids)` as a gauge and confirm it tracks RSS.
3. **Verify the fix.** Replay a few hours of traffic and confirm `len(_seen_ids)` plateaus at about rate × TTL and RSS goes flat. Compare against the old build.
4. **Check dedupe behavior.** Test that a duplicate inside the window is still caught and one outside it is not.
5. **Check `received_at` retention.** If it is a `datetime` or other object, it may be costing more memory than the id key. Storing a float would shrink the footprint.
6. **Fix `export_report` separately.** Check that `lsof -p <pid>` stays flat after calling it repeatedly, and test the error path with an unwritable path.
7. **Other processes weren't profiled.** If other instances or workers share this code, check them for the same growth pattern.
