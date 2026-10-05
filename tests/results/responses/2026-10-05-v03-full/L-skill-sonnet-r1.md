---
scenario: L
condition: skill
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

## 결론

hand-roll 대신 표준 라이브러리 `csv.writer`를 쓰는 것을 권합니다. 이유는 제공된 제약 조건(경로 2곳, 하루 100행 미만, 일반 CSV reader, 모든 필드가 str)에서 두 선택지가 동등하게 동작하고, 직접 만든 helper는 추가로 유지할 코드가 되기 때문입니다.

## FACTS / ASSUMPTIONS / UNKNOWNS

FACTS (요청에 명시된 내용)
- 현재 구현은 `','.join(fields)`라서 필드 안의 `,`, `"`, `\n`을 처리하지 못합니다.
- 소비자는 CRLF 레코드를 쓰는 일반 CSV reader이고, 커스텀 dialect는 없습니다.
- Python 3 표준 `csv`, `io`가 가능하고, 필드는 모두 str이며, `csv.writer`를 배제하는 측정된 제약은 없습니다.

ASSUMPTIONS
- 소비자의 "일반 CSV reader"가 RFC 4180 스타일 quoting(따옴표 감싸기, `""` 이스케이프, quoted 필드 안의 개행 허용)을 지원한다고 가정합니다. 요청에 명시된 사실은 아니므로 아래 UNKNOWNS에 둡니다.

UNKNOWNS
- 소비자가 BOM이나 헤더 행을 기대하는지는 알 수 없습니다. 현재 요구에는 없으므로 추가하지 않았습니다.
- 이 응답에서는 코드를 실행하지 않았습니다. 아래 round-trip 출력은 실행 결과가 아니라 예상입니다.

## 선택지 비교

| | 직접 구현 (15~20줄) | `csv.writer` |
|---|---|---|
| 요구 충족 | 가능 | 가능 (기본값이 `lineterminator='\r\n'`, `QUOTE_MINIMAL`) |
| 유지보수 | 직접 테스트하고 관리해야 함 | 표준 라이브러리가 관리 |
| 엣지 케이스 | 빠뜨릴 위험 (`\r` 단독 등) | 라이브러리가 처리 |
| 의존성 | 없음 | 없음 (stdlib) |

직접 구현의 장점으로 제시된 "통제하기 쉽다"는 점은, `csv.writer`를 배제할 성능이나 호환성 제약이 없는 이상 근거가 약합니다. 호출 경로가 2곳뿐이라는 점도 어느 쪽이든 큰 차이를 만들지 않습니다. 둘 다 가능하다면 직접 짠 quoting 로직이라는 새 유지보수 대상을 만들지 않는 쪽이 낫다고 판단했습니다.

## 적용할 수정

```python
import csv
import io


def export_row(fields):
    buf = io.StringIO()
    # lineterminator를 명시하는 이유: 기본값에 암묵적으로 기대지 않고
    # 소비자 계약(CRLF)을 코드에 드러내기 위해서다.
    writer = csv.writer(buf, lineterminator='\r\n')
    writer.writerow(fields)
    return buf.getvalue()
```

호출 시그니처(`export_row(fields) -> str`)와 반환 형식(CRLF로 끝나는 한 레코드)은 그대로 유지하므로 두 스크립트의 호출부는 수정하지 않아도 됩니다.

## Round-trip 검증

```python
import csv
import io

fields = ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
actual = export_row(fields)

# 예상 출력:
# '"Ada, Inc.","She said ""hello""","first line\nsecond line"\r\n'
print(repr(actual))

# newline=''을 쓰는 이유: 기본 설정이면 quoted 필드 안의 개행이 변환되어
# round-trip 비교가 왜곡될 수 있다.
rows = list(csv.reader(io.StringIO(actual, newline='')))
assert len(rows) == 1, rows
assert rows[0] == fields, rows[0]
assert actual.endswith('\r\n')
print("round-trip OK:", rows[0])
```

실행 방법은 위 코드를 `check.py`로 저장한 뒤 `python3 check.py`입니다. `AssertionError` 없이 `round-trip OK`가 출력되면 통과입니다.

## Conclusion: INFERRED

- `csv.writer`의 기본 동작(`QUOTE_MINIMAL`이 구분자, 따옴표, 줄바꿈 문자를 포함한 필드를 quoting하고 내부 따옴표를 두 번 쓰는 동작)에 대한 설명은 제 지식에 기반한 것입니다. 이 환경에서 실제로 실행해 확인하지는 않았습니다.
- 제출 전에 위 스크립트를 한 번 실행해 주세요. 통과하면 이 판단은 VERIFIED가 됩니다.

## 회귀 위험과 남은 불확실성

- 입력이 str이 아니면 `','.join`은 `TypeError`를 냈지만, `csv.writer`는 `None`을 빈 문자열로, 숫자는 `str()`로 변환해 조용히 통과시킵니다. 요청에 "모든 필드는 문자열"이라고 되어 있어 영향은 없지만, 이 동작 차이는 알아두셔야 합니다.
- 기존 출력과 달라지는 부분은 quoting이 필요한 필드뿐입니다. 쉼표, 따옴표, 개행이 없는 필드는 이전과 같은 바이트로 출력됩니다. 소비자 쪽에서 이 변화가 문제없는지는 실제 소비자로 한 번 확인하는 것이 안전합니다.
- 소비자가 RFC 4180을 따르는 reader라는 가정(ASSUMPTIONS)이 틀리면 이 수정은 효과가 없습니다. 실제 소비자 파서에 샘플 한 건을 흘려보는 것이 가장 싼 검증입니다.
