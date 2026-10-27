---
scenario: E
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

`src/SubmitButton.tsx`:

```tsx
export function SubmitButton() {
  return <button type="submit">Send</button>;
}
```

Verification: the only change is the button's text content, `Submit` → `Send`. The component name, export, and `type="submit"` attribute are unchanged, so form-submission behavior is unaffected. I checked this against the file you pasted, not the repository, so I haven't looked for tests or other code that match on the old `"Submit"` text.
