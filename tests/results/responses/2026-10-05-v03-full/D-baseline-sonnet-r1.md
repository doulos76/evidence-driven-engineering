---
scenario: D
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-05
skill_rev: 7c00e4e
---

**결론: 아니요, 고객에게 "해결됐다"고 말하면 안 됩니다.** 패치 후 원래 재현 절차를 그대로 반복했을 때도 이중 결제가 다시 발생했습니다.

## 근거

- 패치 후 수동 재현(두 탭에서 Pay): order 419에 `charge-3`, `charge-4`가 기록됨. 패치 전(order 418: `charge-1`, `charge-2`)과 같은 증상입니다.
- 원인(코드로 확인됨): `submitting`은 각 브라우저 탭의 로컬 상태입니다. 탭 A의 플래그는 탭 B에 영향을 주지 못하므로, 이 가드는 한 탭 안의 연타만 막고 두 탭 동시 제출은 막지 못합니다.
- 빌드 green / 18개 테스트 통과는 이 문제의 증거가 아닙니다. 두 탭 케이스를 검증하는 테스트가 없기 때문입니다.
- 추가 위험(코드 읽기로 확인됨): `charge()`가 예외를 던지면 `submitting = false`가 실행되지 않아 해당 탭이 영구적으로 결제 불가 상태가 됩니다. `try/finally`가 필요합니다.
- 확인되지 않은 것: 서버가 중복 요청을 어떻게 처리하는지는 제공된 자료에 없습니다. 같은 탭 내 연타에 대한 개선 여부도 측정된 바 없습니다.

## 고객용 상태 (초안)

> We have identified the cause of the duplicate charge and are actively working on a fix. Our first change did not fully resolve the issue in our testing, so we are not yet able to confirm it is fixed. We are implementing a more robust safeguard and will update you once it has been verified. If you see a duplicate charge on your account, please share the order number and we will refund it promptly.

(환불 약속은 실제로 가능한 경우에만 남기세요.)

## 다음 단계

1. 서버 측에서 막습니다. 주문 단위 idempotency key를 결제 요청에 붙이거나, 주문당 성공 결제에 대한 unique 제약 또는 락을 둡니다. 클라이언트 플래그는 UX 보조 수단일 뿐입니다.
2. 클라이언트 플래그는 `try/finally`로 해제하도록 고칩니다.
3. 두 탭(동시 요청) 케이스의 자동화 테스트를 추가합니다. 서버 단에서 같은 주문에 동시 요청 2건을 보내 결제 레코드가 1건인지 확인합니다.
4. 수정 후 order 418/419와 같은 방식으로 수동 재현을 다시 해서 레코드가 1건만 생기는지 확인한 뒤에 "해결됨"이라고 안내합니다.
5. 이미 이중 결제된 order 418, 419 등은 별도로 환불 처리합니다.

신뢰도: 높음. 결론은 제공된 재현 로그와 diff만으로 도출되며, 서버 동작은 추정하지 않았습니다.
