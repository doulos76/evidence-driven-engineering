---
scenario: A
condition: skill
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

결론부터: `validate_profile`은 고장난 게 아니라 제 역할을 한 것으로 보입니다. 원인은 `apply_patch`가 `display_name`이 요청에 없을 때 `None`으로 덮어쓰는 것이며, 수정 대상은 `apply_patch`를 권장합니다. 다만 제공된 발췌만 본 것이라 아래 한계가 있습니다.

## FACTS
- 요청 body는 `{"bio": "Updated biography"}`이고 `display_name` 키가 없다.
- `apply_patch` 전에는 `display_name="Ada"`, 후에는 `display_name=None`이다(사용자가 제공한 로그).
- `apply_patch`는 `profile.display_name = data.get("display_name")`로, 키가 없으면 `None`을 대입한다. 반면 `bio`는 `data.get("bio", profile.bio)`로 기존 값을 유지한다.
- `save_profile`의 순서는 `apply_patch` -> `validate_profile` -> `repository.save`이다.
- `validate_profile`은 `None`을 받았고, 코드상 `None`은 `isinstance(..., str)`에 실패하므로 `ValueError`를 던지는 것이 코드대로의 동작이다.
- 이 재현에서 `repository.save`는 호출되지 않았다.

## ASSUMPTIONS
- 제공된 코드 발췌가 실제 실행된 코드와 같다. 트레이스백의 줄 번호(`save_profile` 15행, `validate_profile` 5행)가 발췌와 맞지 않아 같은 버전인지 확인하지 못했다.
- 같은 증상의 다른 "일부 저장 요청"도 `display_name` 누락 body일 것이다. 재현은 한 건뿐이다.

## INFERENCES
- 유효성 검증이 거부한 값(`None`)은 검증 이전 단계에서 만들어졌다. 즉 검증은 증상이 드러난 지점이고 결함은 그 앞에 있다.
- API 계약("PATCH에서 생략된 필드는 이전 값 유지")과 비교하면 `display_name`의 `data.get("display_name")`은 계약 위반이다. `bio`의 처리 방식이 계약을 따르는 형태라는 점이 이를 뒷받침한다.

## UNKNOWNS
- `validate_profile`이 정상 값("Ada" 등)을 거부하는지는 보여준 입력으로는 알 수 없다. 이 경우 사용자 가설이 일부 성립하므로, 정상 값 통과 테스트가 가장 싼 반증 수단이다.
- `{"display_name": null}`처럼 명시적 null이 올 때 기대 동작(거부인지, 허용인지)은 계약 발췌에 없다.
- `bio`에 명시적 null이 오면 `None`이 되는데, 이것이 허용되는지 모른다.
- `apply_patch`의 다른 호출 지점, 기존 테스트, 이 코드의 git 이력(의도적으로 `display_name`을 필수로 취급한 이유가 있는지)은 보지 못했다.
- `profile` 객체가 캐시/세션 등 공유 상태인지 여부. 지금 코드는 검증 전에 객체를 변경하므로, 검증 실패 후 변경된 객체가 어딘가에 남아 있을 수 있다.
- "일부 저장 요청"의 실제 빈도와 다른 실패 유형 존재 여부.

## CONFLICTING EVIDENCE
- 사용자 가설("validation이 깨졌다")은 트레이스백 최상단 프레임에 근거하는데, 같은 로그의 before/after 값은 검증 전에 이미 `None`이었음을 보여준다. 둘이 충돌하므로 로그의 값 변화 쪽을 우선했다. 최상단 프레임은 예외가 발생한 위치일 뿐 값이 잘못된 위치는 아니다.

## CLAIMS
- "API 계약상 생략된 PATCH 필드는 이전 값을 유지한다" — 사용자가 전달한 문서 내용이며 원문은 보지 못했다. 다만 이 진단의 핵심 기준이므로 계약 원문 확인이 필요하다.

## Hypotheses
1. `validate_profile`이 잘못되었다. 반증 시도: 코드는 `None`/빈 문자열을 거부하는 단순한 조건이고, 로그상 입력이 이미 `None`이다. 이 가설이 맞으려면 "Ada" 같은 정상 값도 거부해야 하는데 그런 증거가 없다. 약화됨.
2. `apply_patch`가 누락 필드를 `None`으로 덮어쓴다. 지지: 코드와 before/after 로그가 직접 일치하고, `bio`와의 비대칭이 계약 위반을 보여준다. 반증 증거는 발견하지 못했다.

## Conclusion
Conclusion: STRONGLY SUPPORTED

VERIFIED가 아닌 이유: 코드와 로그가 서로 일치하지만, 실제 서비스에서 이 파일 버전으로 재현을 돌려 본 것은 아니고(줄 번호 불일치), 다른 호출 경로도 보지 못했다.

## Proposed Change
`validate_profile`은 수정하지 않습니다. `apply_patch`만 최소 변경합니다.

```python
def apply_patch(profile, data):
    # PATCH 계약: 생략된 필드는 이전 값을 유지해야 하므로 키가 있을 때만 갱신한다.
    if "display_name" in data:
        profile.display_name = data["display_name"]
    profile.bio = data.get("bio", profile.bio)
```

- 명시적 `{"display_name": null}`은 이 변경 후에도 `None`이 되어 검증에서 거부됩니다. 이 동작이 의도와 맞는지는 계약 확인 후 결정하세요(위 UNKNOWNS).
- 이번 변경에서 하지 않는 것: 검증 로직 변경, "검증 후 적용"으로의 순서 재설계, `bio` null 정책 변경. 증거가 아직 이를 요구하지 않습니다. 검증 전 객체 변경이 문제가 되는지는 `profile`의 공유 여부를 확인한 뒤 별도로 판단하는 편이 안전합니다.

## Verification (권장, 아직 실행하지 않음)
- 재현 테스트를 먼저 추가해 수정 전 실패를 확인한다: 기존 `display_name="Ada"`인 프로필에 `{"bio": "Updated biography"}`를 저장하면 예외가 없고 `display_name == "Ada"`, `bio`만 갱신됨.
- 반증용 테스트: `{"display_name": "Grace"}`는 정상 저장, `{"display_name": ""}`와 `{"display_name": null}`은 `ValueError`, 정상 값에서 `validate_profile`이 통과함(가설 1 반증).
- `apply_patch`의 다른 호출 지점과 기존 테스트를 검색해 `display_name` 누락 시 `None`을 기대하는 곳이 없는지 확인한다.
- 빌드/컴파일 성공만으로는 이 동작이 고쳐졌다는 증거가 되지 않으므로, 위 테스트 결과로 판단한다.

## Regression Risk
- 어딘가에서 `apply_patch`를 "전체 교체(PUT)" 용도로 재사용하고 있다면, 누락 시 이전 값이 유지되어 동작이 달라진다. 호출 지점 확인이 필요하다.
- 명시적 null 처리는 이번 변경으로 달라지지 않는다.

## Remaining Uncertainty
- 줄 번호 불일치로 인한 코드 버전 차이 가능성.
- 계약 원문, 명시적 null 정책, 다른 호출 경로, `profile` 공유 여부, 실제 장애 요청의 분포는 확인하지 못했다. 같은 증상의 다른 원인이 있을 수 있으므로, 수정 후에도 실패 로그에 요청 body 키 목록을 남겨 관찰하는 것을 권합니다.
