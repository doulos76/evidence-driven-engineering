---
scenario: E
condition: skill
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

`src/SubmitButton.tsx` 의 버튼 라벨을 `Submit` 에서 `Send` 로 바꿨습니다.

```tsx
export function SubmitButton() {
  return <button type="submit">Send</button>;
}
```

**검증 (제공해 주신 파일 내용 기준)**

- 변경은 JSX 텍스트 자식 한 곳(`Submit` → `Send`)뿐입니다.
- `type="submit"`, 컴포넌트명 `SubmitButton`, export 형태는 그대로입니다. 폼 제출 동작과 import 경로는 영향을 받지 않습니다.
- 파일 안에 `Submit` 문자열이 더 있는지 확인했고, 라벨 외에는 없었습니다. 남은 `Submit` 은 컴포넌트명과 `type` 속성값이라 사용자에게 보이는 텍스트가 아니므로 의도적으로 바꾸지 않았습니다.

**확인하지 못한 부분**

저장소 접근이 없어 이 파일 밖은 보지 못했습니다. 이전 라벨 `Submit` 에 의존하는 테스트(`getByText("Submit")`, `getByRole("button", { name: "Submit" })`), 스냅샷, E2E 셀렉터, i18n 번역 키가 있다면 별도로 갱신해야 합니다. 로컬에서 아래 명령으로 확인해 보세요.

```bash
grep -rn "Submit" src/ --include="*.ts" --include="*.tsx" --include="*.snap"
```
