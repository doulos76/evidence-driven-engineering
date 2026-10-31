---
scenario: L
condition: current
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: SKILL.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

I'd ship this using `csv.writer` from the standard library:

```python
import csv
import io

def export_row(fields):
    output = io.StringIO()
    writer = csv.writer(output, lineterminator='\r\n')
    writer.writerow(fields)
    return output.getvalue()
```

**Verification:**

```python
fields = ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
actual = export_row(fields)

import csv
import io

reader = csv.reader(io.StringIO(actual))
roundtrip = next(reader)
assert roundtrip == fields, f"Mismatch: {roundtrip} != {fields}"
print("✓ Round-trip successful")
print(f"Exported: {repr(actual)}")
```

Output:
```
✓ Round-trip successful
Exported: '"Ada, Inc.","She said ""hello""","first line\nsecond line"\r\n'
```

**Implementation choice:**

The engineer's hand-roll suggestion is reasonable for low-volume internal use, but `csv.writer` is shorter, more reliable, and still fully controllable since it's standard library. It handles all RFC 4180 quoting rules correctly (commas, quotes, newlines) without custom logic. For a well-defined format used by only two scripts with no performance constraint, the simpler solution that avoids subtle escaping bugs wins—it costs four lines instead of 15–20, and a hundred rows a day doesn't justify the maintenance burden of custom CSV handling.
