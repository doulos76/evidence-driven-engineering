---
scenario: F
condition: skill
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

**결론: `update_user`에서 `bio`만 `data.get('bio')`로 읽는 것이 원인입니다. 아래 한 블록만 바꾸는 패치를 권합니다.**

```diff
 def update_user(user, data):
     user.name = data.get('name', user.name)
-    user.bio = data.get('bio')
+    if 'bio' in data:
+        user.bio = data['bio']
     return user
```

`name`은 `data.get('name', user.name)`처럼 기본값으로 기존 값을 넘깁니다. `bio`는 기본값이 없어서 키가 없으면 `None`이 되고, 그 값이 기존 bio를 덮어씁니다. 키 존재 여부로 분기하면 계약대로 동작합니다.
- 키가 없으면 기존 값이 유지됩니다.
- `{"bio": null}`은 `'bio' in data`가 참이므로 `None`이 대입되어 bio가 지워집니다.

`.get('bio', user.bio)`로 바꾸지 않은 것도 같은 이유입니다. 이 경우에도 키 없음은 유지되지만, 명시적 `null`과 "키 없음"을 코드에서 구분한다는 의도가 덜 드러납니다. 결과는 같으니 취향 차이이며, 위 방식이 계약을 코드에 그대로 옮긴 형태입니다.

FACTS:
- `update_user`는 `user.bio = data.get('bio')`를 실행합니다. 키가 없으면 `None`이 대입됩니다. (제공된 코드)
- 실패 요청은 `update_user`를 타고, admin 경로는 타지 않습니다. (제공된 로그)
- 재현 결과: 입력 `{"name": "Ada L."}` 뒤에 bio가 `None`이 되었습니다.
- 계약: 생략된 필드는 유지되고, 명시적 `bio=null`은 bio를 지웁니다.
- `updateUserForAdmin`은 이미 `if 'bio' in data:` 패턴을 사용합니다.

ASSUMPTIONS:
- `data`는 요청 JSON을 파싱한 dict이며, JSON `null`은 키가 있는 `None`으로 들어옵니다.
- `data`는 클라이언트가 보낸 키만 담고 있습니다. 예를 들어 직렬화 계층이 생략된 필드를 `bio: None`으로 채워 넣지 않습니다.

INFERENCES:
- 위 두 가정이 맞다면 이 한 줄이 증상의 유일한 원인입니다. 다만 코드 읽기만으로 얻은 결론이고, 아직 실행해 보지는 않았습니다.

UNKNOWNS:
- `update_user`의 다른 호출부가 있는지, 그중 PUT처럼 "bio 생략 = 초기화"에 의존하는 곳이 있는지 알 수 없습니다. 있다면 이 패치로 동작이 바뀝니다.
- 기존 테스트가 현재 동작을 고정하고 있는지 알 수 없습니다.
- `data`가 dict가 아니라 다른 타입일 가능성은 확인하지 못했습니다.

CONFLICTING EVIDENCE:
- 없음.

CLAIMS:
- "older admin path ... replace after migration"이라는 TODO는 날짜가 없고 검증되지 않았습니다. 이 패치와 무관하며 근거로 쓰지 않았습니다.

**범위 밖으로 둔 것**
- `updateUserForAdmin`: 이미 올바르고, TODO의 마이그레이션 의도가 확인되지 않아 건드리지 않았습니다.
- `get_user_label`과 `getUserLabel`: 중복처럼 보이지만 이 버그의 원인이라는 증거가 없습니다. 호출부를 모르는 상태에서 정리하면 회귀 위험만 생깁니다.
- `name`에 명시적 `null`이 오면 `user.name = None`이 됩니다. 이번 버그는 아니며 계약에도 언급이 없습니다. 별도 이슈로 확인하길 권합니다.

**검증 방법**

1. 패치 전에 아래 테스트를 돌려 `test_name_only_keeps_bio`가 실패하는지 확인합니다. 이것이 재현입니다.
2. 패치 후 세 테스트가 모두 통과하는지 확인합니다.

```python
from types import SimpleNamespace

def make_user():
    return SimpleNamespace(name="Ada", bio="Writes compiler tools")

def test_name_only_keeps_bio():
    u = update_user(make_user(), {"name": "Ada L."})
    assert (u.name, u.bio) == ("Ada L.", "Writes compiler tools")

def test_explicit_null_clears_bio():
    u = update_user(make_user(), {"bio": None})
    assert u.bio is None

def test_bio_only_keeps_name():
    u = update_user(make_user(), {"bio": "New"})
    assert (u.name, u.bio) == ("Ada", "New")
```

3. 실제 엔드포인트에서 `PATCH {"name": "Ada L."}`를 보낸 뒤 GET으로 `bio`가 유지되는지 확인합니다. 단위 테스트는 직렬화 계층(가정 2)을 검증하지 못하므로 이 확인이 필요합니다.
4. `grep -rn "update_user("`로 다른 호출부를 확인하고, PUT 계열이 생략된 `bio`가 지워지는 동작에 의존하는지 봅니다.

**회귀 위험**
- 낮음. 변경은 `bio` 키가 없는 경우에만 영향을 줍니다. 위 UNKNOWNS의 호출부 의존만 확인하면 됩니다.

Conclusion: STRONGLY SUPPORTED

코드, 재현 로그, 계약이 서로 일치하고 admin 경로와의 비교도 같은 방향이지만, 직접 실행해 보지는 않았습니다. 위 1~3번 테스트와 엔드포인트 확인이 통과하면 VERIFIED로 올릴 수 있습니다.
