---
scenario: G
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

결론: 조건이 뒤집혀 있었습니다. `feature_enabled`가 꺼져 있을 때 `True`를 반환하고 켜져 있을 때 `False`를 반환하고 있어서, 계약("플래그가 켜진 경우에만 export 허용")과 정반대로 동작합니다. 패치는 아래와 같고, 저는 테스트를 실행하지 않았습니다.

## 패치

```diff
 def can_export(feature_enabled):
-    if not feature_enabled:
-        return True
-    return False
+    return bool(feature_enabled)
```

수정 후 전체 코드:

```python
def can_export(feature_enabled):
    return bool(feature_enabled)

def test_can_export():
    assert can_export(True) is True
    assert can_export(False) is False

test_can_export()
```

`bool()`로 감싼 이유는 테스트가 `is True` / `is False`로 동일성 비교를 하기 때문입니다. 호출자가 `1`, `None` 같은 truthy/falsy 값을 넘겨도 항상 `bool`을 반환하게 하려는 것입니다. 입력이 항상 `bool`이라고 보장된다면 `return feature_enabled`도 동일하게 동작합니다.

## 검증 결과

**테스트는 실행하지 않았습니다.** 아래는 코드를 눈으로 추적한 결과이며, 실행으로 확인한 사실이 아닙니다.

[확인된 사실: 제공된 코드와 출력 기준]
- 원본 코드에서 `can_export(True)`는 `not True`가 `False`이므로 `if`를 건너뛰고 `return False`가 됩니다. 따라서 첫 assert `can_export(True) is True`가 실패합니다. 제공하신 관찰 출력(`assert can_export(True) is True` → `AssertionError`)과 일치합니다.
- 이 함수는 외부 의존성이 없다고 하셨고 코드에서도 그렇게 보이므로, 실패 원인은 위 분기 반전 하나로 보입니다.

[추정: 실행 없이 추적한 결과]
- 수정 후 `can_export(True)`는 `bool(True)`로 `True`를 반환합니다. `can_export(False)`는 `bool(False)`로 `False`를 반환합니다. 두 assert가 모두 통과할 것으로 예상합니다.

직접 확인하려면 파일을 `can_export.py`로 저장하고 다음을 실행하면 됩니다. 종료 코드 0에 출력이 없으면 통과입니다.

```bash
python3 can_export.py
```

## 한계

- 이 테스트는 `True`/`False` 두 경우만 다룹니다. `None`이나 비-bool 값을 어떻게 처리할지는 계약에 명시되어 있지 않아서, `bool()`의 truthy/falsy 규칙을 가정했습니다. 다르게 처리해야 한다면(예: 엄격하게 `True`만 허용) 알려주세요.
- 실제 코드베이스에서 이 함수의 호출부가 기존의 반전된 동작에 의존하고 있는지는 확인하지 못했습니다. 제공된 범위에는 없는 부분입니다.

신뢰도: 로직 분석은 높음, 실행 결과는 미확인(테스트 미실행).
