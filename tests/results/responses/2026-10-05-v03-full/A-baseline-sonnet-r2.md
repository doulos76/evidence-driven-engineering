---
scenario: A
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

결론: `validate_profile`은 고장 나지 않았습니다. 버그는 `apply_patch`에 있습니다. 생략된 `display_name`을 이전 값으로 유지하지 않고 `None`으로 덮어씁니다. validation은 그 결과를 정확히 잡아낸 것이라서, 이 함수를 느슨하게 고치면 안 됩니다.

## 확인된 사실 (제공된 자료에서 직접 확인)

- 요청 본문은 `{"bio": "Updated biography"}`이고 `display_name` 키가 없습니다.
- `apply_patch` 전에는 `display_name="Ada"`였고 후에는 `None`입니다. `data.get("display_name")`이 키가 없을 때 `None`을 반환하고, 그 값이 그대로 대입됩니다.
- `bio`는 `data.get("bio", profile.bio)`로 기본값에 기존 값을 넘기기 때문에 정상 동작합니다. 두 필드의 처리 방식이 불일치합니다.
- 그 직후 `validate_profile`이 `None`을 보고 `ValueError`를 냅니다. `None`은 "non-empty string"이 아니므로 이 거부는 올바릅니다.
- API 계약은 "생략된 PATCH 필드는 이전 값을 유지"입니다. 현재 `apply_patch`는 이 계약을 `display_name`에 대해 위반합니다.
- traceback의 top frame이 `validate_profile`인 것은 예외가 *발생한* 위치일 뿐입니다. 잘못된 값이 *만들어진* 위치는 `apply_patch`입니다.

## 권장 변경

`display_name`도 `bio`와 같은 패턴으로 바꿉니다.

```python
def apply_patch(profile, data):
    profile.display_name = data.get("display_name", profile.display_name)
    profile.bio = data.get("bio", profile.bio)
```

이 변경으로 재현 케이스에서 `display_name="Ada"`가 유지되어 validation을 통과합니다. `validate_profile`은 수정하지 않습니다.

## 추가로 권장하는 방어 (선택, 정책 확인 필요)

- 현재 `save_profile`은 `profile`을 먼저 변경한 뒤 검증합니다. 검증이 실패하면 객체가 이미 오염된 상태로 남습니다. 이 객체가 캐시나 세션에서 공유된다면 실패한 요청의 값이 다른 곳에서 보일 수 있습니다. 복사본에 적용하고 검증한 뒤 반영하거나, 변경 전에 입력을 검증하는 방식을 고려할 수 있습니다.
- `{"display_name": null}`을 명시적으로 보냈을 때의 동작은 위 수정으로도 `None`이 대입되어 `ValueError`가 납니다. 이것을 "거부(400)"로 볼지 "무시"로 볼지는 계약에 적혀 있지 않습니다. 거부가 의도라면 현재 validation이 맞습니다.
- 사용자 입력 오류인데 `ValueError`가 처리되지 않고 크래시로 이어진다면, 400 응답으로 변환하는 처리가 필요해 보입니다. 다만 이것은 아래 한계 때문에 확인하지 못했습니다.

## 진단의 한계 (추정과 미확인)

- 제공된 발췌만 봤습니다. `repository`, 호출하는 핸들러, 예외 처리 계층, `profile` 객체의 정의는 보지 못했습니다.
- "일부 save 요청에서 크래시"가 모두 이 원인이라는 증거는 없습니다. 이 재현은 `display_name`이 생략된 요청 하나만 설명합니다. 가설로는 다른 실패 요청도 `display_name`을 생략했을 가능성이 높지만, 추정일 뿐입니다. 크래시하는 다른 요청 본문을 확인하세요.
- `repository.save`는 이 재현에서 호출되지 않았으므로, 저장 이후 단계의 문제 여부는 판단할 수 없습니다.
- `apply_patch`나 `validate_profile`이 다른 경로에서도 쓰이는지 모릅니다. 수정 전에 호출부를 grep으로 확인하세요.
- 수정 후에는 `{"bio": ...}`만 보내는 요청의 회귀 테스트를 추가하는 것을 권합니다. 이 케이스가 `display_name`이 유지됨을 확인합니다.

신뢰도: 이 재현에 대한 원인 진단은 높음, 서비스 전체의 크래시 원인으로 일반화하는 것은 중간 이하입니다.
