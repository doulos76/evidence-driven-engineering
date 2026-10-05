---
scenario: G
condition: skill
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

결론: 분기 조건의 반환값이 뒤집혀 있습니다. 두 반환값을 맞바꾸면 됩니다. 아래 검증은 제가 테스트를 실행한 결과가 아니라, 코드를 손으로 추적한 결과입니다.

FACTS:
- 계약: feature flag가 켜져 있을 때만 export를 허용한다 (사용자 제공).
- 현재 구현은 `feature_enabled`가 falsy이면 `True`, 그 외에는 `False`를 반환한다. 코드에서 직접 읽은 내용입니다.
- 제공된 테스트 출력에서는 `assert can_export(True) is True`에서 `AssertionError`가 발생했다.
- 네트워크, 파일시스템, 설정 등 외부 의존성은 없다 (사용자 제공).

ASSUMPTIONS:
- 호출자는 `True`/`False`만 넘긴다고 가정합니다. 이 함수의 호출처는 제가 보지 못했습니다.
- 계약의 "enabled"는 truthy/falsy 판정이라고 가정합니다. `None`이나 `0`이 들어올 때의 기대값은 계약에 명시되어 있지 않습니다.

INFERENCES:
- 관찰된 실패는 구현이 뒤집혀 있다는 사실과 일치합니다. `can_export(True)`는 `False`를 반환하므로 첫 assert에서 실패하는 것이 맞습니다.
- 테스트는 첫 실패에서 중단되므로 출력에는 두 번째 assert가 보이지 않습니다. 하지만 현재 구현에서는 `can_export(False)`도 `True`를 반환하므로, 첫 assert를 고쳐도 둘째 assert에서 또 실패했을 것입니다. 즉 실패 지점은 하나가 아니라 구현 전체가 반전된 것입니다.

UNKNOWNS:
- 호출처가 현재의 반전된 동작에 기대고 있는지는 알 수 없습니다. 예를 들어 호출 쪽에서 결과를 다시 부정하는 보정 코드가 있을 수 있습니다.
- truthy/falsy 입력(`None`, `0`, 문자열 등)에 대한 계약상 기대 동작은 알 수 없습니다.

CONFLICTING EVIDENCE:
- 없음. 계약, 구현, 테스트, 실패 출력이 모두 "구현이 반전됨"이라는 설명과 일치합니다. 테스트의 기대값은 계약과도 일치하므로 테스트를 고칠 이유는 없습니다.

CLAIMS:
- "계약은 flag가 켜졌을 때만 허용"은 사용자가 준 설명입니다. 제가 별도 문서로 확인한 것은 아닙니다. 다만 테스트 기대값과 일치하므로 서로 교차 확인은 됩니다.

Hypotheses:
1. 구현의 반환값이 뒤집혀 있다. 코드와 실패 출력이 모두 지지합니다.
2. 테스트가 잘못되었다. 테스트는 계약과 일치하므로 반증됩니다.
3. 호출 측에서 입력이나 결과를 반전해서 쓰는 관례가 있다. 단일 함수만 보고는 확인할 수 없고, 이 경우에도 계약을 어기는 쪽은 이 함수입니다.

Conclusion: STRONGLY SUPPORTED

(손 추적과 실패 출력이 일치하고 대안 가설은 약해졌지만, 제가 직접 실행하지는 않았으므로 VERIFIED는 아닙니다.)

## Patch

최소 변경으로 기존 구조와 `bool` 반환을 유지합니다.

```diff
 def can_export(feature_enabled):
     if not feature_enabled:
-        return True
-    return False
+        return False
+    return True
```

적용 후:

```python
def can_export(feature_enabled):
    if not feature_enabled:
        return False
    return True
```

`return feature_enabled`로 줄이지 않은 이유는, 입력이 `None`이나 `1` 같은 값일 때 `bool`이 아닌 값이 새어 나가 `is True` 류 비교가 깨질 수 있기 때문입니다. 단순화는 요청 범위 밖이라 하지 않았습니다.

## Verification

실행하지 않았습니다. 이 환경에서 테스트를 돌리지 않았으므로 "통과했다"고 주장하지 않습니다. 수동 추적 결과는 다음과 같습니다.

| 호출 | 수정 전 | 수정 후 | 테스트 기대값 |
|---|---|---|---|
| `can_export(True)` | `False` | `True` | `True` |
| `can_export(False)` | `True` | `False` | `False` |

수정 후에는 두 assert 모두 충족되어야 합니다. 직접 확인하려면 다음을 실행하세요 (`export_flag.py`는 예시 파일명이며, 실제 파일명으로 바꾸세요).

```bash
python export_flag.py && echo "OK"
```

assert 실패 없이 종료되면 이 테스트에 한해 통과입니다.

## Regression Risk

- 이 함수는 반환값이 완전히 반대로 바뀝니다. 호출처가 현재의 잘못된 동작에 맞춰 보정하고 있다면(결과를 다시 부정하는 코드 등) 그쪽이 오히려 깨집니다. 머지 전에 호출처를 검색해 확인하세요.
- 현재 구현이 배포된 상태라면, 지금까지 flag가 꺼진 사용자가 export를 할 수 있었고 켜진 사용자가 막혀 있었을 수 있습니다. 이 부분은 보안/권한과 관련될 수 있으니 영향 범위를 별도로 확인하는 것이 좋습니다.

## Remaining Uncertainty

- 테스트가 `True`/`False` 두 값만 다루므로, `None`이나 truthy 값에 대한 동작은 검증되지 않습니다. 계약이 이를 정의한다면 케이스를 추가하세요.
- 테스트 실행은 하지 않았습니다. 위 추적은 코드 읽기에 근거한 것입니다.
