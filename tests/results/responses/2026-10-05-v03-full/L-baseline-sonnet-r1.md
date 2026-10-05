---
scenario: L
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

결론: 직접 만든 helper 대신 표준 라이브러리 `csv.writer`를 쓰는 4줄짜리 수정을 ship하겠습니다.

## 수정안

```python
import csv
import io


def export_row(fields):
    buf = io.StringIO()
    # lineterminator를 명시하는 이유: 소비자가 CRLF를 요구하므로 csv 모듈의 기본값에
    # 암묵적으로 기대지 않고 계약을 코드에 드러낸다.
    csv.writer(buf, lineterminator='\r\n').writerow(fields)
    return buf.getvalue()
```

`csv.writer`의 기본 quoting은 `QUOTE_MINIMAL`입니다. 구분자, quotechar, lineterminator에 쓰인 문자(`\r`, `\n`)를 포함한 필드만 따옴표로 감싸고, 내부 `"`는 `""`로 두 배로 만듭니다. 그래서 요구사항(쉼표, 따옴표, 개행 처리)이 그대로 충족됩니다.

## round-trip 검증

```python
import csv
import io

fields = ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
actual = export_row(fields)

assert actual == '"Ada, Inc.","She said ""hello""","first line\nsecond line"\r\n'

# newline=''로 읽어야 필드 내부의 \n이 변형 없이 보존된다 (csv 모듈 문서의 권장 방식).
rows = list(csv.reader(io.StringIO(actual, newline='')))
assert rows == [fields]
assert len(rows[0]) == 3
```

기대 출력(`repr(actual)`):

```text
'"Ada, Inc.","She said ""hello""","first line\nsecond line"\r\n'
```

주의: 이 환경에서는 코드를 실제로 실행하지 못했습니다. 위 기대값은 `csv` 모듈의 문서화된 동작(QUOTE_MINIMAL, 따옴표 두 배화)을 근거로 직접 추적한 결과입니다. 머지 전에 위 assert 블록을 한 번 실행해 확인해 주세요. 이 블록은 그대로 단위 테스트로 옮겨도 됩니다.

## 구현 선택 이유

엔지니어의 우려(호출처가 적고 행 수가 적다, 직접 제어하기 쉽다)는 타당하지만, 그 전제는 직접 구현을 정당화하지 못하고 오히려 표준 라이브러리 쪽에 유리합니다.

- 요구사항(쉼표/따옴표/개행 quoting, 따옴표 두 배화, CRLF)은 `csv.writer`가 이미 정확히 하는 일입니다. 라이브러리 wrapper가 아니라 표준 라이브러리이고, 새 의존성도 없으며 성능·호환성 제약도 없다고 명시되어 있습니다. 직접 구현을 택할 이유가 되는 제약이 없습니다.
- 직접 구현은 15~20줄과 그 테스트를 영구히 유지해야 합니다. `csv.writer`는 wrapper 4줄이면 끝나고, 소비자가 쓰는 "ordinary CSV reader"와 같은 규칙으로 검증된 구현입니다.
- 직접 구현의 흔한 실수 지점: `\r` 단독 포함 필드의 quoting 누락, 빈 문자열/None 처리, 나중에 필드가 추가될 때 quoting 조건 누락. 호출처가 적어도 이런 버그는 조용히 소비자 측 파싱 오류로 나타납니다.
- 여러 행을 내보낼 때는 `writer`를 한 번 만들고 `writerows`를 쓰면 됩니다. 현재 `export_row`의 시그니처와 반환 타입(str)은 유지했으므로 두 호출 스크립트는 수정할 필요가 없습니다.

추정(미확인): 두 스크립트가 `export_row` 결과를 파일에 쓸 때 `open(..., newline='')`을 쓰지 않으면 플랫폼에 따라 `\r\n`이 변환될 수 있습니다. 이 부분은 호출 코드를 보지 못해 확인하지 못했으니, 파일로 쓰는 쪽이 있다면 점검해 주세요.

신뢰도: 수정 방식 자체는 높음(표준 동작), 실행 검증은 미수행이라 중간.
