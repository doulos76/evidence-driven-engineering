---
scenario: F
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## 버그 분석 및 패치

**버그 원인:**
`update_user` 함수의 8번째 줄에서 `data.get('bio')`는 'bio' 키가 없으면 `None`을 반환합니다. 이는 "omitted fields are unchanged" 계약을 위반합니다.

**최소 패치:**
```python
def update_user(user, data):
    user.name = data.get('name', user.name)
    if 'bio' in data:  # 이 조건문 추가
        user.bio = data['bio']
    return user
```

**설명:**
- 현재: `data.get('bio')`는 'bio' 없을 때 `None` 반환 → bio 초기화됨 (버그)
- 수정: `if 'bio' in data:` 체크로 명시적 제공 시에만 업데이트
- 이미 존재하던 `updateUserForAdmin` 함수(12-16줄)가 올바른 패턴을 보여줍니다

**검증 방법:**

1. **Before 상태 설정:**
   ```python
   user = User(name="Ada", bio="Writes compiler tools")
   ```

2. **PATCH 호출:**
   ```python
   data = {"name": "Ada L."}  # bio는 미포함
   update_user(user, data)
   ```

3. **검증:**
   ```python
   assert user.name == "Ada L."  # ✓ name 변경됨
   assert user.bio == "Writes compiler tools"  # ✓ bio 유지됨 (현재는 None이 되어 실패)
   ```

4. **bio 명시적 제거 검증:**
   ```python
   data = {"name": "Ada L.", "bio": None}
   update_user(user, data)
   assert user.bio is None  # ✓ 명시적 null은 작동해야 함
   ```
