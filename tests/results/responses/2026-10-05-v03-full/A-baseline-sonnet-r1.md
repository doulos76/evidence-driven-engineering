---
scenario: A
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

**결론: `validate_profile`은 고장 나지 않았습니다. 원인은 `apply_patch`입니다.** 수정은 validation이 아니라 `apply_patch`에서 해야 합니다.

## 근거 (제공된 자료에서 확인된 사실)

- Traceback의 top frame이 `validate_profile`인 것은 예외가 *발생한* 지점일 뿐, 결함이 *생긴* 지점이 아닙니다.
- 로그의 상태 변화가 직접 증거입니다.
  - request body: `{"bio": "Updated biography"}` (`display_name` 없음)
  - `apply_patch` 전: `display_name="Ada"`
  - `apply_patch` 후: `display_name=None`
- 코드의 해당 줄은 `profile.display_name = data.get("display_name")`입니다. 키가 없으면 `get`이 `None`을 반환하고, 이 값이 기존 값 "Ada"를 덮어씁니다.
- 이어서 `validate_profile`이 `None`을 보고 "non-empty string이어야 한다"며 거부합니다. 이 검증은 스펙대로 동작한 것입니다.
- API contract는 "PATCH에서 생략된 필드는 이전 값을 유지"입니다. `display_name`은 이 계약을 위반하고, `bio`는 `data.get("bio", profile.bio)`로 이미 올바르게 처리됩니다. 두 줄의 비대칭이 버그의 정체입니다.

## 권장 변경

```python
def apply_patch(profile, data):
    if "display_name" in data:
        profile.display_name = data["display_name"]
    if "bio" in data:
        profile.bio = data["bio"]
```

- `validate_profile`은 그대로 둡니다. 완화하면(예: `None` 허용) 실제로 `display_name`이 비는 데이터가 저장될 수 있습니다.
- 명시적으로 `{"display_name": null}` 또는 `""`을 보내는 경우는 여전히 validation에서 거부됩니다. 이쪽이 의도된 동작인지는 확인이 필요합니다.
- 회귀 테스트로 "`display_name` 생략 시 기존 값 유지"와 "`display_name: null`/`""`은 거부" 두 케이스를 추가하길 권합니다.

## 부수적으로 눈에 띄는 점 (추정, 별도 확인 필요)

- `save_profile`은 검증 *전에* `profile` 객체를 변경합니다. 검증이 실패해도 메모리 상의 객체는 이미 오염된 상태입니다. 이 객체가 캐시나 세션처럼 요청 간에 공유된다면 실패한 요청이 이후 요청에 영향을 줄 수 있습니다. 공유 여부는 제공된 코드로는 알 수 없습니다.
- `ValueError`가 그대로 전파되어 크래시로 보입니다. 클라이언트 입력 오류라면 400 응답으로 변환하는 편이 적절하지만, 상위 핸들러가 보이지 않아 현재 어떻게 처리되는지는 모릅니다.

## 진단의 한계

- 확인한 것은 **제공된 발췌와 재현 로그 한 건**뿐입니다. 이 한 건은 위 원인으로 완전히 설명되며, `display_name`을 생략한 PATCH가 모두 같은 방식으로 실패할 것이라는 추론도 코드상 타당합니다.
- "일부 save 요청에서 크래시"가 **전부** 이 원인이라는 증거는 없습니다. 다른 요청 형태(예: `display_name`을 보냈는데 타입이 잘못된 경우)나 다른 경로의 실패는 이 자료로 배제할 수 없습니다. 프로덕션 로그에서 실패 요청의 body에 `display_name`이 없는지 대조하면 검증할 수 있습니다.
- Traceback의 줄 번호(`save_profile` 15행, `validate_profile` 5행)가 제시된 코드 발췌의 구조와 일치하지 않습니다. 발췌가 실제 `profiles.py`와 동일 버전이 아닐 수 있으니, 수정 전에 실제 파일에서 `apply_patch`가 같은 모양인지 확인해야 합니다.
- `repository.save`, `profile` 객체의 생성/수명, 다른 `apply_patch` 호출처, 요청 핸들러는 보지 못했습니다. `apply_patch`를 다른 곳에서도 호출한다면 시그니처 동작 변경의 영향을 확인해야 합니다.
- 제안한 수정은 실행·테스트하지 않았습니다. 제공된 자료만으로 한 코드 추론입니다.

신뢰도: 근본 원인(`apply_patch`의 `get` 덮어쓰기)은 높음, "모든 크래시가 이것 때문"이라는 범위는 중간 이하.
