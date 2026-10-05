---
scenario: A
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## 진단

**근본 원인:** `apply_patch` 함수의 필드 처리 불일치

요청에서 `display_name`을 생략하면, `data.get("display_name")`은 기본값이 없으므로 `None`을 반환합니다. 반면 `bio`는 `data.get("bio", profile.bio)`로 기본값을 지정해 이전 값을 유지합니다. 

이 불일치 때문에 omitted 필드가 보존되어야 한다는 API 계약을 위반하고, `display_name=None`이 되어 검증을 실패합니다.

## 권장 변경

```python
def apply_patch(profile, data):
    profile.display_name = data.get("display_name", profile.display_name)  # 기본값 추가
    profile.bio = data.get("bio", profile.bio)
```

`display_name`에 `profile.display_name`을 기본값으로 지정하면, 요청에 없을 때 이전 값이 유지됩니다. 이렇게 하면 두 필드 모두 동일한 retention 로직을 따르게 되어 API 계약을 충족합니다.
