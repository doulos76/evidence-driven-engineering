---
scenario: A
condition: skill
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

결론부터: `validate_profile`은 고장 나지 않았고, 이 재현에서는 정상적으로 잘못된 입력을 거부했습니다. 원인은 `apply_patch`가 요청에 없는 `display_name`을 `None`으로 덮어쓰는 것입니다. 이는 "생략된 PATCH 필드는 이전 값을 유지한다"는 API 계약 위반입니다. 추천 변경은 `apply_patch`의 한 줄입니다. 다만 아래 한계가 있습니다.

```
FACTS:
- traceback의 최상단 프레임은 validate_profile(profiles.py:5)이고, 예외는 ValueError("display_name must be a non-empty string")이다.
- 요청 본문은 {"bio": "Updated biography"} 이고 display_name 키가 없다.
- apply_patch 전에는 display_name="Ada", 후에는 display_name=None 이다 (제공된 로그).
- apply_patch는 `profile.display_name = data.get("display_name")` 이다. 기본값 인자가 없어 키가 없으면 None이 된다.
- 같은 함수의 bio는 `data.get("bio", profile.bio)` 로 기존 값을 유지한다. 두 필드의 처리가 비대칭이다.
- validate_profile은 display_name이 str이 아니거나 빈 문자열이면 예외를 던진다. None은 str이 아니므로 예외가 나는 것이 코드상 정상 동작이다.
- save_profile은 apply_patch -> validate_profile -> repository.save 순서다. 이 재현에서 repository.save에는 도달하지 않았다.
ASSUMPTIONS:
- 제공된 발췌가 실제 배포 코드와 동일하다.
- 이 요청이 사용자가 말한 "일부 save 요청 crash"의 대표 사례다. 재현은 한 건뿐이다.
INFERENCES:
- 크래시는 validate_profile의 버그가 아니라 앞단 apply_patch가 만든 잘못된 상태 때문에 발생한다. (로그의 before/after 값과 코드가 일치한다.)
- display_name을 생략하는 모든 PATCH 요청이 같은 경로로 실패할 것이다. 코드를 읽고 추론한 것이며 실행으로 확인하지는 않았다.
UNKNOWNS:
- 실제로 실패하는 다른 요청들이 모두 "display_name 생략" 유형인지 알 수 없다.
- 클라이언트가 `"display_name": null`을 명시적으로 보낼 때 기대 동작(값 지우기 허용인지, 거부인지)이 계약에 명시돼 있는지 모른다.
- Profile 객체의 다른 필드, 그리고 apply_patch가 다른 호출 지점에서도 쓰이는지 모른다.
- ValueError가 호출자에서 어떻게 처리되는지(500 크래시인지 400 응답인지) 모른다.
- Profile 객체가 캐시나 세션처럼 공유되는지 모른다. 그렇다면 검증 실패 후에도 변경된 상태가 남을 수 있다.
CONFLICTING EVIDENCE:
- 사용자의 가설("validation이 깨졌다")과 상충한다. 검증 로직은 명세대로 동작했고, 입력값(None)이 문제였다. 검증을 완화하면 증상만 가리고 display_name=None이 저장될 수 있다.
CLAIMS:
- "API 계약상 생략된 PATCH 필드는 이전 값을 유지한다"는 사용자의 진술이다. 계약 문서 자체는 보지 못했다. 다만 bio의 처리 방식과 일치하므로 신뢰할 근거는 있다.
- "validate_profile 검증이 깨졌다"는 사용자의 가설이다. 위 증거로는 지지되지 않는다.
```

## 가설과 증거

| 가설 | 지지 증거 | 반증/부족한 증거 |
|---|---|---|
| H1. `apply_patch`가 생략된 필드를 `None`으로 덮어쓴다 | before/after 로그, `data.get("display_name")`의 기본값 없음, bio와의 비대칭 | 실제 실행은 하지 않았다 |
| H2. `validate_profile`이 잘못되어 유효한 값을 거부한다 | traceback의 top frame뿐이다 | 입력이 `None`이므로 거부가 맞다. 로그상 "Ada"에서 거부된 사례는 없다 |

top frame은 예외가 발생한 위치일 뿐 결함이 있는 위치를 뜻하지 않습니다. H2를 깨뜨리려면 "validate가 `None`을 통과시켜야 하는가?"를 물으면 되는데, 계약상 display_name은 필수 문자열로 보이므로 아닙니다. H1은 로그 값 하나하나가 코드와 맞아떨어집니다.

Conclusion: STRONGLY SUPPORTED

(코드와 로그가 서로 일치하고 대안 H2가 약화되었지만, 직접 실행해서 재현하지는 않았으므로 VERIFIED는 아닙니다.)

## 권장 변경

```python
def apply_patch(profile, data):
    profile.display_name = data.get("display_name", profile.display_name)
    profile.bio = data.get("bio", profile.bio)
```

`validate_profile`은 그대로 둡니다. 변경 이유는 두 가지입니다. 생략된 필드를 보존하라는 계약을 bio와 같은 패턴으로 맞춥니다. 검증은 그대로 두어 명시적 빈 값 입력은 계속 막습니다.

## 검증 방법

1. 먼저 회귀 테스트를 추가합니다. `display_name="Ada"` 프로필에 `{"bio": "Updated biography"}`로 `save_profile`을 호출합니다. 현재 코드에서는 `ValueError`로 실패하고, 수정 후에는 `display_name == "Ada"`, `bio == "Updated biography"`이며 `repository.save`가 호출되어야 합니다.
2. 주변 경로도 함께 테스트합니다. `{}`(빈 본문), `{"display_name": ""}`, `{"display_name": "Grace"}`를 넣습니다.
3. 빌드나 기존 테스트 통과만으로는 이 버그가 고쳐졌다는 증거가 되지 않습니다. 위 재현 테스트가 통과해야 합니다.

## 회귀 위험과 남은 불확실성

- 명시적 `"display_name": null`: 수정 후에도 `None`이 대입되어 검증에서 거부됩니다(실패하는 쪽으로 안전). 이것이 의도한 동작인지는 계약 확인이 필요합니다. 값 삭제를 허용해야 한다면 별도 결정이 필요합니다.
- 이 변경이 보고된 모든 크래시를 설명하는지는 확인하지 못했습니다. 로그에서 다른 유형의 실패(예: display_name을 보냈는데 거부된 경우)가 있는지 확인하세요.
- 수정과 별개로, 지금 구조는 검증 전에 객체를 변경합니다. 실패 시 변경된 객체가 공유·캐시된다면 부분 적용 상태가 남을 수 있습니다. 증거가 없으므로 이번 수정에는 넣지 않았고, Profile 객체의 수명을 확인한 뒤 판단할 사항입니다.
- 서비스의 나머지 부분은 보지 못했고, 위 내용은 제공된 발췌에 한정된 진단입니다.
