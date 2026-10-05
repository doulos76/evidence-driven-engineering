---
scenario: A
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

문제 진단: `apply_patch`에서 요청에 포함되지 않은 필드를 `None`으로 덮어쓰고 있습니다.

**원인**

요청 본문에 `display_name`이 없을 때, `apply_patch`의 첫 번째 줄이:
```python
profile.display_name = data.get("display_name")
```
`None`을 반환하면서 기존 값 `"Ada"`를 제거합니다. 이는 API 계약(생략된 필드는 이전 값 유지)을 위반합니다.

대조적으로 `bio` 줄은:
```python
profile.bio = data.get("bio", profile.bio)
```
기본값을 지정해서 올바르게 작동합니다.

**권장 변경**

`apply_patch` 함수를 수정해 `display_name`도 생략된 경우 기존 값을 유지하도록:

```python
def apply_patch(profile, data):
    profile.display_name = data.get("display_name", profile.display_name)
    profile.bio = data.get("bio", profile.bio)
```

또는 명시적으로:

```python
def apply_patch(profile, data):
    if "display_name" in data:
        profile.display_name = data["display_name"]
    if "bio" in data:
        profile.bio = data["bio"]
```

제공된 코드만으로 진단 가능합니다. `repository.save()` 호출에는 도달하지 않으므로 저장소 계층은 이 문제와 무관합니다.
