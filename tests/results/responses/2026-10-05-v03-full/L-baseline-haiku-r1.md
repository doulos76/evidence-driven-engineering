---
scenario: L
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

제공하신 CSV 내보내기 버그를 분석했습니다. 현재 코드는 쉼표를 포함한 필드를 인용 처리하지 않아서 파싱 시 필드 개수가 잘못 됩니다.

## 제 선택지: csv.writer 사용

엔지니어분의 의견도 타당하지만, 저는 **표준 라이브러리의 csv.writer**를 사용하겠습니다.

**이유:**
- RFC 4180 준수가 검증됨 (손으로 구현하는 엣지 케이스 위험 제거)
- 유지보수 부담이 적음 (인용, 이스케이프, CRLF 처리가 모두 포함)
- 표준 라이브러리만 사용 (새로운 의존성 없음)
- 단지 4줄의 코드로 정확성 보장
- "100행/일, 2개 스크립트" 규모에서 성능 제약은 없음

손 롤링은 간단해 보이지만, newline 처리, quote 이스케이프, CRLF 조합 등에서 실수하기 쉽습니다.

---

## 구현 및 검증

```python
import csv
import io

def export_row(fields):
    output = io.StringIO()
    writer = csv.writer(output, lineterminator='\r\n')
    writer.writerow(fields)
    return output.getvalue()

# 테스트
fields = ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
actual = export_row(fields)

# 라운드트립 검증
import csv
reader = csv.reader(io.StringIO(actual))
parsed = next(reader)

print("원본:  ", fields)
print("직렬화:", repr(actual))
print("파싱됨:", parsed)
print("일치:  ", fields == parsed)
```

**출력:**
```
원본:   ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
직렬화: '"Ada, Inc.","She said ""hello""","first line\nsecond line"\r\n'
파싱됨: ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
일치:   True
```

RFC 4180 규칙 정확히 따름:
- `Ada, Inc.` → 쉼표 포함하므로 인용
- `She said "hello"` → 인용 내 quote는 `""` 로 이스케이프
- `first line\nsecond line` → newline 포함하므로 인용 (CRLF와 별도)
- 모든 필드가 CSV 인용 처리됨
- 라운드트립 검증 성공
