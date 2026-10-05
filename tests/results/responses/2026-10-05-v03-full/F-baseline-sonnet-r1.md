---
scenario: F
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

결론: `update_user`의 `bio` 줄 한 곳만 고치면 됩니다. 원인은 `data.get('bio')`가 키가 없을 때 `None`을 돌려줘서 bio를 덮어쓰는 것입니다.

## 최소 패치

```diff
 def update_user(user, data):
     user.name = data.get('name', user.name)
-    user.bio = data.get('bio')
+    user.bio = data.get('bio', user.bio)
     return user
```

`data.get('bio', user.bio)`는 키가 없으면 기존 값을 유지하고, 키가 있으면 값을 그대로 씁니다. 명시적 `"bio": null`은 `None`으로 들어가 bio가 지워지므로 계약("생략한 필드는 변경 없음, 명시적 null은 삭제")을 만족합니다. `name` 줄과 같은 패턴이라 일관성도 있습니다.

## 확인된 사실 (제공된 코드와 로그 기준)

- 실패한 요청은 `update_user`를 탑니다. payload에 `bio` 키가 없으므로 `data.get('bio')`가 `None`을 반환하고, 그 값이 `user.bio`에 대입됩니다. 관찰 결과(`bio=None`)와 일치합니다.
- `updateUserForAdmin`은 `'bio' in data` 검사를 하므로 같은 버그가 없습니다.

## 건드리지 않은 것

- `updateUserForAdmin`, `get_user_label`, `getUserLabel`은 수정하지 않았습니다. 중복·네이밍 불일치는 보이지만 이 버그와 무관하고, "older admin path after migration"이라는 TODO는 날짜도 없는 메모라 지금 근거로 삼기 어렵습니다. 정리하려면 호출처를 확인한 뒤 별도 변경으로 하는 편이 안전합니다.
- 한 가지 주의: `data.get('bio', user.bio)`는 `'bio' in data`와 동작이 같지만, `data`가 `dict`가 아닌 객체(예: 커스텀 매핑)라면 `get`의 기본값 의미가 다를 수 있습니다. 이 코드에서는 이미 `data.get('name', ...)`를 쓰고 있어 같은 가정입니다.

## 검증 방법

1. 재현 케이스를 회귀 테스트로 추가합니다.

```python
from types import SimpleNamespace

def make_user():
    return SimpleNamespace(name="Ada", bio="Writes compiler tools")

def test_patch_name_only_keeps_bio():
    u = update_user(make_user(), {"name": "Ada L."})
    assert u.name == "Ada L."
    assert u.bio == "Writes compiler tools"

def test_patch_explicit_null_clears_bio():
    u = update_user(make_user(), {"bio": None})
    assert u.bio is None

def test_patch_bio_updates_bio():
    u = update_user(make_user(), {"bio": "New"})
    assert u.bio == "New"
```

2. 패치 전에는 첫 번째 테스트가 실패하고(`bio is None`), 패치 후에는 세 개 모두 통과해야 합니다.

```bash
pytest -k "patch_" -q
```

3. 가능하면 실제 엔드포인트로도 한 번 확인합니다. 사용한 URL·인증은 환경에 맞게 바꾸세요.

```bash
curl -X PATCH "$BASE/users/$ID" -H 'Content-Type: application/json' -d '{"name":"Ada L."}'
# 응답/재조회 결과: name="Ada L.", bio="Writes compiler tools"
```

## 확인하지 못한 것

- `update_user`의 호출처가 `data`에 `bio`를 항상 채워서 넘기거나, 상위 계층(직렬화기 등)에서 누락 필드를 `None`으로 채우는지는 제공된 코드로는 알 수 없습니다. 위 curl 확인이 이 부분을 잡아줍니다. 상위에서 `bio: None`을 채워 넣는다면 이 패치만으로는 해결되지 않습니다.

신뢰도: 높음 (패치 자체), 중간 (상위 계층 영향은 미확인).
