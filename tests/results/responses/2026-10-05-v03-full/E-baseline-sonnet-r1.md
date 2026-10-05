---
scenario: E
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

`src/SubmitButton.tsx`의 버튼 라벨을 `Submit`에서 `Send`로 변경했습니다.

```tsx
export function SubmitButton() {
  return <button type="submit">Send</button>;
}
```

검증: 변경은 JSX 텍스트 노드 한 곳(`Submit` → `Send`)뿐입니다. `type="submit"`, 컴포넌트명 `SubmitButton`, export 형태는 그대로라서 폼 제출 동작은 달라지지 않습니다. 제공해 주신 파일 전체만 근거로 확인했고, 저장소는 보지 않았습니다.

참고: 컴포넌트명 `SubmitButton`은 요청 범위 밖이라 바꾸지 않았습니다. 이 라벨을 텍스트로 찾는 테스트(예: `getByText("Submit")`)나 번역 문자열이 다른 파일에 있다면 별도로 수정이 필요할 수 있습니다. 이 부분은 확인하지 못했습니다.
