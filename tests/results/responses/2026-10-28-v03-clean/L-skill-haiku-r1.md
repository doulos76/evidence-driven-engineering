---
scenario: L
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

I'd ship the stdlib solution using `csv.writer`. It's simpler, more maintainable, and there's no evidence-based reason to hand-roll when the stdlib tool is available and does this exact job correctly.

The engineer's reasoning ("easier to control than a library wrapper") conflates `csv.writer` with a third-party library—it's not a wrapper, it's the standard tool for RFC 4180 CSV. Hand-rolling introduces subtle risks (quote escaping edge cases) that add maintenance burden for code that only two scripts use and processes <100 rows/day. Correctness and simplicity favor the battle-tested approach.

```python
import csv
import io

def export_row(fields):
    output = io.StringIO()
    writer = csv.writer(output, lineterminator='\r\n')
    writer.writerow(fields)
    return output.getvalue()

# Verify round-trip
fields = ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
actual = export_row(fields)

# Parse it back with a standard CSV reader
reader = csv.reader(io.StringIO(actual))
parsed = next(reader)

assert parsed == fields
print(repr(actual))
# "Ada, Inc.",\"She said \"\"hello\"\""first line\nsecond line"\r\n
```

This handles:
- Comma in "Ada, Inc." → quoted
- Quotes in "She said…" → escaped by doubling
- Newline in the third field → quoted
- CRLF line ending per spec

If they insist on hand-rolling for code clarity, that's defensible too—it's genuinely short—but csv.writer removes the correctness risk with no downside.
