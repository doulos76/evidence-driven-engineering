---
scenario: E
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

Updated SubmitButton component with label changed from "Submit" to "Send":

```tsx
export function SubmitButton() {
  return <button type="submit">Send</button>;
}
```

Verified: button label text changed from "Submit" to "Send", button type preserved.
