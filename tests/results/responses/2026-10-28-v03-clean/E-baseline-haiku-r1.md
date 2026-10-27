---
scenario: E
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

Here's the updated file with the button label changed from "Submit" to "Send":

```tsx
export function SubmitButton() {
  return <button type="submit">Send</button>;
}
```

**Verification:** The button text inside the JSX has been changed from `Submit` to `Send` on line 2. The `type="submit"` attribute remains unchanged.
