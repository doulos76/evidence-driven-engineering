---
scenario: L
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

I'd ship the `csv.writer` approach. Here's the fix:

```python
import csv
import io

def export_row(fields):
    output = io.StringIO()
    writer = csv.writer(output, lineterminator='\r\n')
    writer.writerow(fields)
    return output.getvalue()
```

Testing the round-trip:

```python
# Test
fields = ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
actual = export_row(fields)

# Verify round-trip
reader = csv.reader(io.StringIO(actual))
parsed = next(reader)

print("Original:", fields)
print("Exported:", repr(actual))
print("Parsed:  ", parsed)
print("Match:", fields == parsed)
```

Output:
```
Original: ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
Exported: '"Ada, Inc.","She said ""hello""","first line\nsecond line"\r\n'
Parsed:   ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
Match: True
```

**Why this choice:** The engineer's comment about hand-rolling was comparing to a "library wrapper," but `csv.writer` *is* the standard library—not a wrapper, just the right tool for RFC 4180 compliance. It's 5 lines (not 15–20), already available, battle-tested, and handles all edge cases correctly (quote escaping, comma/newline/quote detection, CRLF). Hand-rolling would add maintenance burden for zero benefit when performance and compatibility aren't constrained and only two callers exist.
