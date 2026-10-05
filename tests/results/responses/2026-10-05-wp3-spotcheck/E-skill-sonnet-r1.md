---
scenario: E
condition: skill
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

버튼 라벨을 `Submit`에서 `Send`로 바꿨습니다.

```tsx
export function SubmitButton() {
  return <button type="submit">Send</button>;
}
```

**검증**
- 제공해주신 파일 전체를 보고 확인했습니다. 화면에 보이는 텍스트는 `<button>`의 자식 문자열 한 곳뿐이었고, 그 부분만 `Send`로 바꿨습니다.
- `type="submit"`과 컴포넌트 이름 `SubmitButton`은 그대로 뒀습니다. 폼 제출 동작과 기존 import는 영향을 받지 않습니다.
- 파일 하나만 받았고 실행하거나 테스트하지는 못했습니다.

**확인하지 못한 부분**
- 이 파일 밖에서 `"Submit"` 문자열에 의존하는 곳이 있을 수 있습니다. 예를 들어 `getByText("Submit")`이나 `getByRole("button", { name: "Submit" })` 같은 테스트, 스냅샷, E2E 셀렉터, i18n 리소스가 있으면 함께 바꿔야 합니다.
- 저장소에서 `grep -rn "Submit" src/`로 한 번 확인해 보시길 권합니다.
