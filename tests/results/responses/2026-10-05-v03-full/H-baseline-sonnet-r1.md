---
scenario: H
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

## 결론

**현재 정보로는 새 background export job에서 `snapshot()`을 호출하는 것을 승인할 수 없습니다. 보류(hold)를 권고합니다.** "안전하다"는 증거도 "위험하다"는 증거도 packet에 없으므로 어느 쪽도 단정하지 않습니다. 다만 호출을 허용하려면 안전하다는 근거가 필요하고, 지금 있는 유일한 직접 증거(docstring)는 반대 방향입니다. 그래서 기본값은 "호출하지 않거나, serialize 확인 전까지 main thread로 넘기는 것"입니다.

두 동료의 주장은 각각 부분적으로만 맞습니다.

## 증거 평가

**[확인된 사실: packet 내용]**
- `snapshot()` docstring: "Main-thread only. Do not use from a worker thread."
- call site #1은 main thread, call site #2는 background thread에서 `snapshot()`을 호출하며 1년 전에 배포됨.
- 운영 노트: 지난 1년간 call site #2에서 보고된 실패 없음.
- cache consistency audit 없음. `serialize()` 소스, docstring 이력, model의 thread-safety 문서 모두 packet에 없음.

**동료 A: "docstring이 결론을 낸다"**
- docstring은 작성자가 남긴 명시적 제약이라 무시할 수 없는 증거입니다.
- 그러나 docstring은 "왜" 제약인지(실제 thread 불안전, UI 객체 접근, 과거의 방어적 표기 등), 언제 작성됐는지, 지금도 유효한지를 말해주지 않습니다. 그래서 "절대 불가"를 증명하지는 못합니다.
- 반대로 이 제약을 어기는 호출이 이미 존재한다는 것은 docstring이 이미 어겨지고 있거나 낡았을 가능성을 보여줍니다. 어느 쪽인지는 알 수 없습니다.

**동료 B: "1년간 worker가 돌았으니 안전하다"**
- "보고된 실패 없음"은 "실패가 없었음"과 다릅니다. 모니터링·알림이 이 실패를 잡도록 되어 있었는지 확인된 바가 없습니다.
- thread 관련 결함은 간헐적이고, 조용히 잘못된 데이터를 만드는 형태(torn read, 일관되지 않은 snapshot)일 수 있습니다. 예외가 나지 않으면 "실패 없음"으로 집계됩니다. 이 때문에 **cache consistency audit이 없다는 점이 특히 중요합니다.** 잘못된 값이 cache에 들어갔더라도 아무도 모르고 있을 수 있습니다.
- call site #2의 부하·타이밍이 새 job과 같다는 보장이 없습니다. `export_batch`는 여러 model을 연속으로 직렬화하므로 model이 동시에 변경되는 시간 창이 더 깁니다. 그래서 #2의 무사고 기록이 새 호출에 그대로 전이된다고 볼 수 없습니다.
- 1년 무사고는 약한 정황 증거입니다. 단, "이 호출 패턴이 최소한 크게 망가지지는 않았다"는 정도의 의미는 있어 완전히 무시할 것은 아닙니다.

**[추정/추론]**
- 설명 가능성은 여러 가지입니다: (a) serialize가 실제로 thread-safe이고 docstring이 낡음, (b) thread-unsafe이지만 경합 조건이 드물어 아직 안 터짐, (c) 터졌지만 감지되지 않음. 현재 증거로는 이 셋을 구분할 수 없습니다.
- 위험한 쪽의 비용이 비대칭적일 수 있습니다. 조용한 데이터 손상은 발견도 재현도 어렵습니다. 다만 이것도 serialize 구현을 봐야 확정됩니다.

## 권고

1. **지금 결정해야 한다면**: 새 worker에서 `snapshot()`을 직접 호출하지 않습니다. 선택지는 아래와 같습니다.
   - main thread에서 `snapshot()`을 실행해 결과(불변 값)를 worker에 넘기는 방식. docstring 계약을 지키므로 가장 보수적입니다.
   - 또는 확인이 끝날 때까지 export job 배포를 미룹니다.
2. call site #2는 **"안전함이 입증된 선례"가 아니라 "계약 위반 가능성이 있는 기존 호출"** 로 분류하고 별도 follow-up 대상으로 올립니다. 새 코드가 이를 선례로 복제하지 않게 합니다.
3. 아래 확인을 마치면 결정을 다시 엽니다.

## 다음 확인 (우선순위 순)

1. **`serialize()` 구현 읽기**: 공유 가변 상태, 전역/클래스 변수, lazy 초기화·내부 cache, UI 프레임워크 객체·thread-affine 자원(thread-local, run loop, DB 연결) 접근 여부를 봅니다. 이 결과가 가장 결정적입니다.
2. **docstring 이력 추적**: `git log -S "Main-thread only"` / `git blame`으로 문구가 언제, 어떤 커밋·이슈에서 왜 들어갔는지 확인합니다. call site #2 배포 전후 중 어느 쪽인지도 봅니다. 작성자에게 직접 묻는 것도 방법입니다.
3. **model의 변경 경로 확인**: export 도중 main thread(또는 다른 thread)가 model을 변경할 수 있는지, 어떤 락/직렬화로 보호되는지 확인합니다.
4. **call site #2 사후 검증**: 그 cache 내용을 샘플링해 같은 model을 main thread에서 만든 `snapshot()`과 비교합니다. 이것이 없는 audit을 대신하는 가장 값싼 증거입니다.
5. **"실패 없음"의 감도 확인**: 그 worker의 오류가 로깅·알림되는지, 예외가 삼켜지지 않는지, 데이터 불일치를 사용자가 신고할 경로가 있는지 확인합니다.
6. **재현 시도**: 별도 worker에서 `snapshot()`을 반복 호출하면서 main thread에서 model을 변경하는 stress test를 돌립니다. 가능하면 thread sanitizer 또는 thread-affinity assertion을 추가합니다. 실패 재현은 "위험" 증거가 되지만, 재현되지 않는다고 "안전"이 증명되지는 않습니다.
7. **임시 계측**: `snapshot()`에 호출 thread를 기록하는 로그/assert를 넣어 call site #2가 실제로 background에서 실행되는지, 호출 빈도는 어떤지 확인합니다.

## 결정 기준

- 1번에서 thread-safe임이 코드로 확인되고 3번에서 동시 변경이 없거나 보호됨 → docstring을 갱신(근거 포함)하고 호출을 허용.
- thread-unsafe로 확인되거나 판단 불가 → main thread 경유 또는 thread-safe 복사본/전용 API로 설계.

신뢰도: 증거 평가와 "보류" 권고는 높음. serialize의 실제 안전성에 대해서는 정보가 없어 판단하지 않았습니다.
