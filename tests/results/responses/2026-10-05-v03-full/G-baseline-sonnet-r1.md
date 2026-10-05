---
scenario: G
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

결론: 조건이 뒤집혀 있습니다. `not feature_enabled`일 때 `True`를 반환하고 있어서, 계약("플래그가 켜진 경우에만 export 허용")과 정반대로 동작합니다. 관찰된 `can_export(True) is True` 실패와 일치합니다.

## 패치

```diff
 def can_export(feature_enabled):
-    if not feature_enabled:
-        return True
-    return False
+    return feature_enabled is True
```

`feature_enabled is True`로 쓴 이유: 테스트가 `is True` / `is False`로 비교하므로 반환값이 항상 `bool`이어야 합니다. `return feature_enabled`만 쓰면 `1`이나 `"yes"` 같은 truthy 값이 그대로 반환되어 `is` 비교가 깨질 수 있습니다. 다만 truthy 값(`1` 등)을 "켜짐"으로 볼지는 계약에 명시되어 있지 않습니다. 이 패치는 엄격하게 `True`만 허용합니다. truthy도 허용해야 한다면 `return bool(feature_enabled)`로 바꾸세요. 이 부분은 제가 정한 가정입니다.

## 검증 결과

- 코드는 실행하지 않았습니다. 테스트를 돌렸다고 가정하지 않습니다. 아래는 코드를 읽고 추적한 결과입니다.
- 기존 코드 추적 (확인된 사실): `can_export(True)`는 `not True`가 False라서 `return False`로 가고, 그래서 `assert ... is True`가 실패합니다. 제공하신 관찰 출력(AssertionError)과 일치합니다. 원인 가설이 증상을 설명한다는 점은 확인됐습니다.
- 패치 후 추적 (추론, 미실행):
  - `can_export(True)`는 `True is True`라서 `True`가 되어 첫 assert를 통과합니다.
  - `can_export(False)`는 `False is True`라서 `False`가 되어 두 번째 assert를 통과합니다.
- 범위: 제공하신 설명대로 외부 의존성이 없는 순수 함수라서, 위 추적이 이 테스트 두 케이스에 대해서는 충분히 근거가 됩니다. 다만 `None`이나 truthy 값 입력 같은 케이스는 테스트에 없고 검증하지 않았습니다.

직접 확인하려면 아래 명령을 실행하세요. 테스트 파일 마지막 줄에서 `test_can_export()`가 호출되므로, 통과하면 아무 출력 없이 종료됩니다.

```bash
python3 your_file.py && echo OK
```

신뢰도: 원인과 패치 자체는 높음, 실행 검증은 없음(코드 추적만).
