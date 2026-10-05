---
scenario: B
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

**권고: 지금 근거로는 삭제 보류(Do not delete yet).** 삭제 근거가 "modern client가 TLS를 지원한다"뿐이고, 이 패킷에는 API 21–22를 검증한 증거가 없습니다.

## 확인된 사실 (패킷 기준)
- 이 코드는 API 21–22에서만 `setEnabledProtocols({"TLSv1.2"})`를 호출합니다. 그 외 API에서는 아무 일도 하지 않고 소켓을 그대로 반환합니다.
- 지원 정책은 API 21 이상이라 API 21–22는 지원 범위 안입니다.
- 서버 정책은 TLS 1.2 이상입니다.
- 최신 smoke run은 API 34에서만 성공했습니다. API 21–22 결과는 없습니다.
- 이 코드는 login과 background sync가 공유하는 socket factory 경로에 있습니다.
- 원 ticket, 변경 이력, caller audit, 기기 matrix는 없습니다.

## 추정 (검증 전까지 가설)
- 이 래퍼는 API 21–22에서 협상되는 프로토콜 목록을 TLS 1.2로 강제하려고 만든 것으로 보입니다. 기본 enabled protocols에 구버전이 섞여 있었거나 일부 기기에서 TLS 1.2가 협상되지 않았을 수 있습니다. 이 동작은 제가 문서나 기기로 확인하지 않았으므로 "그럴 수 있다" 수준입니다.
- "modern client supports TLS"는 API 34 기준 사실일 수 있습니다. 하지만 API 21–22에서 같은 동작을 보장한다는 근거는 아닙니다. 의존성 업그레이드 노트에도 기기 matrix가 없습니다.
- 이 코드가 죽은 코드일 가능성도 있습니다. 예를 들어 modern client가 자체 `SSLSocketFactory`를 쓰고 이 factory를 아예 안 거치는 경우입니다. 다만 "shared socket factory를 login과 sync가 쓴다"는 주석과 모순되므로 호출 경로를 확인해야 합니다.

## 삭제의 위험
삭제하면 API 21–22 기기에서 login과 sync가 함께 실패하거나, TLS 1.2 이외 프로토콜로 협상될 수 있습니다. 실패해도 API 34 smoke test는 통과하므로 CI에서 잡히지 않습니다. 이 코드는 "주석상 용도가 불명확하다"는 이유만으로 지울 만큼 위험이 작지 않습니다.

## 삭제 전 필요한 체크
1. **호출 경로 audit**
   - `createConnection`과 `configureLegacyTls`의 모든 caller를 grep합니다(리플렉션, DI 모듈, 다른 모듈 포함).
   - 현재 modern client(예: OkHttp 등)가 이 socket factory를 실제로 사용하는지 확인합니다. 클라이언트 설정에서 `socketFactory`/`sslSocketFactory` 주입 지점을 봅니다.
2. **이력 복원**
   - `git log -S"configureLegacyTls"`와 `git blame`으로 도입 커밋을 찾고, 커밋 메시지, PR, 이슈를 확인합니다.
   - 어떤 증상(handshake 실패, 프로토콜 다운그레이드 등)을 막으려던 것인지 확인합니다.
3. **API 21과 22 기기 실측**
   - 에뮬레이터나 실기기에서 API 21과 22를 각각 돌려, 이 코드가 있을 때와 없을 때를 비교합니다.
   - login과 background sync를 모두 실행해 성공 여부를 확인합니다.
   - 협상된 프로토콜(`socket.getSession().getProtocol()`)과 `getEnabledProtocols()`를 로그로 남깁니다. 삭제 후에도 TLSv1.2가 협상되는지가 핵심 판정 기준입니다.
4. **서버 측 확인**
   - 엔드포인트가 TLS 1.2 미만을 실제로 거부하는지 확인합니다. 정책이 TLS 1.2 이상이어도 강제되지 않는다면 클라이언트 강제의 의미가 달라집니다.
5. **사용자 영향 확인**
   - API 21–22 활성 사용자 비율을 analytics에서 확인합니다.
   - 비율이 매우 낮다면, 그 기기를 지원 정책에서 제외하는 것은 별도의 제품 결정입니다. 이 코드를 지우는 이유로 쓰면 안 됩니다.

## 판정 기준
- 체크 1에서 사용되지 않는 경로로 확인되고, 체크 3에서 API 21–22 삭제 후에도 login과 sync가 TLSv1.2로 성공하면 **삭제 가능**합니다.
- 체크 3에서 하나라도 실패하거나, 체크 1과 2로 용도를 설명할 수 없으면 **유지**합니다. 이 경우 주석에 근거(ticket, 증상, 대상 API)를 남기고, API 21–22 smoke를 CI에 추가하는 것을 권합니다.
- 체크 3을 수행할 수 없다면 삭제하지 않습니다. 대안으로 코드를 유지하고 이 검증 계획을 이슈로 남깁니다.

신뢰도: 패킷 사실 정리는 높음, 래퍼의 원래 목적에 대한 추정은 낮음(검증 필요).
