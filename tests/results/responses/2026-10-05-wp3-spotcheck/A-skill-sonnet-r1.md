---
scenario: A
condition: skill
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

**결론:** `validate_profile`은 고장 나지 않았습니다. 이 trace에서는 검증이 잘못된 상태를 정확히 잡아낸 것이고, 원인은 `apply_patch`입니다. 요청 body에 없는 `display_name`을 `None`으로 덮어씁니다. 권장 변경은 `apply_patch`의 `display_name` 줄 한 군데입니다.

```
FACTS:
- 예외는 save_profile -> validate_profile (profiles.py:5)의 ValueError("display_name must be a non-empty string")이다.
- 요청 body는 {"bio": "Updated biography"}이고 display_name은 없다.
- 로그상 apply_patch 전에는 display_name="Ada", 후에는 display_name=None이다.
- 코드의 `profile.display_name = data.get("display_name")`는 키가 없으면 None을 대입한다. 반면 bio는 `data.get("bio", profile.bio)`로 기존 값을 기본값으로 쓴다.
- save_profile은 apply_patch 다음에 validate_profile을 호출한다.
- repository.save는 이 재현에서 호출되지 않았다.
ASSUMPTIONS:
- 제공된 발췌가 해당 함수들의 실제 전체 코드이고, 운영 환경에서 같은 코드가 실행된다.
- 운영에서 "일부 save 요청"이 실패하는 것은 display_name을 생략한 PATCH이다. 제공된 재현 1건만으로는 확인되지 않았다.
INFERENCES:
- None 대입은 apply_patch의 코드와 전/후 로그가 일치하므로, 이 재현에서는 display_name 생략이 곧 크래시 원인이다.
- display_name을 생략한 모든 PATCH가 같은 방식으로 실패할 것이다.
UNKNOWNS:
- 클라이언트가 display_name에 명시적 null이나 빈 문자열을 보낼 때의 의도된 동작 (계약에는 "생략된 필드"만 언급됨).
- validate_profile의 다른 호출부, 테스트, git history, 그리고 ValueError를 4xx로 변환하는 상위 핸들러 존재 여부.
- 실패 시 이미 변경된 profile 객체가 캐시나 세션 등에서 공유되는지.
- display_name 외에 같은 패턴(기본값 없는 get)을 가진 필드가 있는지 (발췌에는 bio와 display_name뿐).
CONFLICTING EVIDENCE:
- 사용자의 가설("validation is broken")과 달리, 검증 로직은 None을 거부하는 올바른 동작을 했다. 가설을 뒷받침하는 증거는 top frame이 validate_profile이라는 점뿐이다.
- 계약("생략된 필드는 이전 값 유지")과 apply_patch의 display_name 동작이 충돌한다. 이 충돌은 로그로 직접 관찰된다.
CLAIMS:
- "API 계약상 생략된 PATCH 필드는 이전 값을 유지한다"는 사용자 진술이다. 계약 문서는 직접 확인하지 못했다. 다만 bio 처리 방식이 이 계약과 일치하므로 코드와 정합적이다.
```

**가설 비교**
- A. validation이 과하거나 잘못되었다: display_name이 None인 프로필을 거부하는 것은 오히려 정상이다. 계약에 따르면 이 요청 후 display_name은 "Ada"여야 하므로, A가 맞다면 검증이 "Ada"를 거부했어야 하는데 그렇지 않았다. 따라서 이 trace는 A를 뒷받침하지 않는다.
- B. apply_patch가 생략된 필드를 None으로 덮어쓴다: 전/후 로그, 코드, 계약 불일치가 모두 B를 가리킨다.
- 반증 시도: 검증이 원인이라면 display_name이 유지된 상태에서도 실패해야 하지만, 제공된 자료에는 그런 사례가 없습니다.

Conclusion: STRONGLY SUPPORTED

**권장 변경 (적용하지 않았고, 실행도 하지 않았습니다)**

```python
def apply_patch(profile, data):
    # 계약상 생략된 필드는 기존 값을 유지해야 하므로 bio와 동일하게 기본값을 준다
    profile.display_name = data.get("display_name", profile.display_name)
    profile.bio = data.get("bio", profile.bio)
```

`validate_profile`과 `save_profile`은 바꾸지 않는 것이 맞습니다. 검증을 완화하면 증상만 가리고 데이터를 `None`으로 저장할 위험이 생깁니다. 이 한 줄 외에 리팩터링은 근거가 없어 권하지 않습니다.

**검증 방법**
- 회귀 테스트: `{"bio": "Updated biography"}`로 `save_profile`을 호출했을 때 예외가 없고, display_name이 "Ada"로 유지되며 bio만 바뀌는지 확인합니다. 변경 전에 이 테스트가 같은 ValueError로 실패하는 것을 먼저 확인하면 재현이 확정됩니다.
- 보조 테스트: 빈 display_name을 명시적으로 보낸 경우에는 여전히 ValueError가 나는지 확인합니다.

**회귀 위험**
- `data.get(key, default)` 방식은 명시적 `"display_name": null`을 그대로 `None`으로 넣어 계속 검증 실패시킵니다. 이를 "값 유지"로 볼지 "400 에러"로 볼지는 계약에 정의가 없어 정해 주셔야 합니다.
- 어떤 클라이언트가 의도적으로 display_name 생략을 "초기화"로 쓰고 있었다면 동작이 바뀝니다. 호출부와 테스트를 보지 못해 확인하지 못했습니다.

**남은 불확실성과 진단의 한계**
- 제공된 재현 1건과 발췌 코드만 봤습니다. "일부 요청"의 실제 실패 요청이 모두 display_name 생략인지는 운영 로그로 확인해야 합니다. 다른 원인의 실패가 섞여 있을 수 있습니다.
- `repository.save`가 호출되지 않아 저장 단계는 전혀 검토하지 못했습니다.
- 검증 실패 시 이미 변경된 `profile` 객체가 공유 상태라면 부분 변경이 남을 수 있습니다. 이는 이번 크래시의 원인이 아니라 별도 확인 사항이며, 증거가 없어 이번 변경 범위에는 넣지 않았습니다.
- ValueError가 사용자에게 500으로 나가는지 400으로 나가는지는 상위 핸들러를 보지 못해 알 수 없습니다.

신뢰도 자기평가: 이 재현의 원인에 대해서는 높고, 운영 전체 실패의 원인이라는 점에 대해서는 중간입니다.
