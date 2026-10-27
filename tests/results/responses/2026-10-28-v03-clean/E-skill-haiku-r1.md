---
scenario: E
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

I'll update the button label from "Submit" to "Send".

```tsx
export function SubmitButton() {
  return <button type="submit">Send</button>;
}
```

**Verification:** The button label has been changed from `Submit` to `Send` on line 2. The `type="submit"` attribute is preserved.
