---
scenario: C
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

결론부터: 제공된 증거로는 "pool reduction이 root cause"라고 쓸 수 없습니다. 확정할 수 있는 건 "timeout이 02:00 export 시작 직후 약 16분간만 발생한다"까지입니다. Revert는 임시 완화책으로는 합리적이지만, 원인 확정 문구와는 분리해야 합니다.

## 증거 평가

**확인된 사실 (supplied evidence)**
- Monday 배포에서 pool max가 40에서 20으로 줄었고, Tuesday부터 "connection acquisition timed out"이 보고됨.
- 요청 부하는 24시간 95-105 rps로 평탄함.
- Timeout 184건은 전부 02:00-02:15에 몰려 있고, 나머지 시간대는 0건임.
- 02:00에 nightly accounting export가 시작되며, API와 같은 DB에 연결함.
- 해당 시간대의 DB active connection 수는 수집되지 않았음.

**이 증거가 가리키는 것**
- 부하가 평탄한데 낮에는 20개 pool로 timeout이 0건입니다. 따라서 "20개는 현재 부하에 무조건 부족하다"는 주장과 맞지 않습니다. 같은 부하가 하루 종일 같은 pool을 쓰는데 16분만 실패합니다.
- 실패 구간은 부하 변화가 아니라 export 시작 시각과 일치합니다. 이 상관관계는 pool 크기보다 훨씬 구체적입니다.

**엔지니어 논거에 대한 반박**
- "배포 직후라서 배포 탓"은 시간 순서일 뿐입니다. 첫 02:00 실행이 배포 후 처음이었다는 점도 같은 시간 순서로 설명됩니다.
- "export는 수개월째 존재했다"는 export가 원인이 아니라는 증거가 아닙니다. 예전에는 pool 40의 여유로 흡수됐을 수 있습니다. 데이터 양 증가나 같은 배포에 포함된 다른 변경이 영향을 줬을 가능성도 있습니다.

## 가능한 설명 (추정, 아직 검증 안 됨)

| 가설 | 내용 | 현재 증거와의 정합성 |
|---|---|---|
| H1. 상호작용 | export가 DB 연결/자원(connection slot, lock, I/O)을 점유해 API 쿼리가 느려지고, pool 20에서는 여유가 없어 timeout 발생. 40에서는 흡수됐음 | 부합. pool 감소는 기여 요인일 수 있음 |
| H2. export 단독 | export 자체의 변화(데이터 증가 등)나 DB 쪽 포화가 원인. pool 크기는 무관 | 부합 (배포와 우연히 겹침) |
| H3. pool 단독 | pool 20이 순수하게 부족 | 부합도 낮음. 평탄한 부하에서 낮 시간 0건과 모순 |

H1과 H2는 현 데이터로 구분할 수 없습니다. 이를 가르는 핵심 데이터가 바로 수집되지 않은 02:00 구간의 DB active connection 수입니다. 이 값이 없으므로 이 부분은 "모른다"고 적어야 합니다.

## 보고서에 쓸 결론 (초안)

> **Root cause: 미확정 (under investigation).**
> Timeout 184건은 전부 02:00-02:15에 발생했으며, 이는 같은 DB를 사용하는 nightly accounting export의 시작 시각과 일치한다. 같은 요청 부하(95-105 rps)에서 나머지 시간대는 0건이므로, API pool 20개가 일반 부하에 부족하다는 가설은 지지되지 않는다. Pool 40에서 20으로의 축소(Monday 배포)가 export 구간의 여유를 없애 증상을 드러냈을 가능성은 있으나, 해당 구간의 DB active connection 데이터가 없어 이를 확인하지 못했다. 현재 확정된 것은 timeout이 export 실행 구간과 상관된다는 점까지이다.

## 제안 조치

1. **완화 (즉시)**: pool을 40으로 revert하는 것은 괜찮습니다. 다만 보고서에는 "mitigation"으로 적고 root cause라고 쓰지 않습니다. 이후 timeout이 사라져도 H1과 H2 모두 같은 결과를 내므로, revert의 성공은 pool이 root cause라는 증거가 되지 못합니다.
2. **데이터 수집 (오늘 밤 02:00 전)**: 01:55-02:20 동안 DB의 active connection 수를 application/user별(API vs export)로 수집합니다. 예: pg_stat_activity 계열 쿼리나 DB 모니터링 지표의 1분 이하 간격 샘플링. 같은 구간의 pool metrics(active/pending/acquire time)와 export 쿼리의 실행 시간, lock 대기도 함께 봅니다. DB가 PostgreSQL이라는 건 제가 확인한 사실이 아니므로, 실제 DB에 맞게 바꿔야 합니다.
3. **구분 실험 (선택)**: 수집 후에도 H1과 H2가 갈리지 않으면 staging이나 하루 한정으로 (a) pool 20 + export 시간 이동, (b) pool 40 + export 유지를 비교합니다.
4. **확인 항목**: Monday 배포에 pool 외 다른 변경이 있었는지, 최근 export 소요 시간과 데이터 양 추이, pool이 인스턴스별인지 전체 기준인지(인스턴스 수 포함)를 확인합니다.
5. **보고서 갱신**: 위 데이터로 H1/H2 중 하나가 확인되면 그때 root cause를 확정하고 보고서를 갱신합니다.

엔지니어에게는 이렇게 전달하면 좋습니다. "Revert는 진행하되, 그것만으로는 원인을 확정할 수 없다. 오늘 밤 데이터를 먼저 잡자."

신뢰도: 중간. 증거 해석(낮 시간 0건과 02:00 일치)은 명확하지만, H1과 H2의 구분은 데이터 부재로 불가능함.
