# Final MRI Response Format v1

_Date: 2026-09-12_
_Status: AGREED — supersedes `FINAL_MRI_RESPONSE_SCHEMA_v0.md` as the output format decision_

## Decision

최종 리포트는 **내부적으로 A–F 사고구조를 유지하되, 사람이 받는 문서는 기존 MRI의 현황/계획 양식으로 압축한다.**

`10 ISSUE FINAL MRI RESPONSE r7_DUAL_OUTPUT` 노드가 한 번의 실행으로 둘을 함께 반환한다.

```
내부 (추적·QC용)                     외부 (제출물)
final_report.A_core_judgment   ──→   □ 핵심 판단
final_report.B_current_status  ──→   □ (현황) 영역별
final_report.C_opportunities   ┐
final_report.D_recommended     ├──→  □ (계획) 우선 추진과제 / 전략적 확장 / 차별화 과제
final_report.E_action_plan     ┘
final_report.F_additional      ──→   □ 추가 확인사항 (조건부)
traceability                         (노출 안 함)
                                     = final_report_text
```

A–F 라벨, BO/RQ ID, portfolio bucket 이름, readiness enum, evidence ID는 `final_report_text`에 노출하지 않는다.
`final_report_text` 없이 A–F 객체만 반환하는 것은 계약 위반이다.

## 현황 — 체크리스트이지 고정 목차가 아님

산업·고객 / 정책·제도 / 금융업권·경쟁사 / 자산운용·펀드시장 / 당사 현황.
관련성이 있고 상위 근거가 있으면 반드시 쓰고, 관련이 없으면 뺀다. 분량 때문에 근거 있는 영역을 버리지 않는다.

영역별 최소 정보 chain은 node 10 프롬프트에 고정되어 있다.
원칙: **상위 Evidence에 존재하는 정보는 Final이 임의로 버리지 않는다.** 없는 수치를 찾아오라는 지시가 아니다.

## 계획 — 승격 조건

무엇을 + 누구에게 + 어떤 방식으로 + 어떤 상품/서비스로 + 어떤 채널을 통해 + 왜.
이를 갖추지 못한 전략은 (계획)으로 올리지 않는다. 09의 전략·action만 사용하고 09의 우선순위를 보존한다.

## Readiness → 어휘 매핑

| readiness | 허용 어휘 |
|---|---|
| READY | 추진 / 개발 / 확대 / 운영 / 연계 |
| CONDITIONAL | 추진 검토 / 상품화 검토 / Pilot 추진 / 협업방안 구체화 |
| MONITOR | 모니터링 / 재검토 |
| 판단 불가 | (계획)에 넣지 않고 추가 확인사항으로 이동 |

"검토"라는 단어 자체는 금지가 아니다. 금지되는 것은 대상·방식·목적이 없는 빈 검토다.

- BAD: `관련 ETF 출시 검토`
- GOOD: `주식보상 수혜 임직원을 대상으로 글로벌 분산형 상품을 기업 제휴채널에 공급하는 방안 검토`

이 완화는 Hard Fail Evaluator v2의 `HF09`와 Golden Test v2의 실패조건에 함께 반영되어 있다.

## Responder는 통과 전용

`final_report_text`가 이 양식대로 화면에 뜨려면 Responder가 그것을 다시 쓰지 않아야 한다.
두 워크플로의 Responder 프롬프트가 `"실행결과 출력"` 한 줄이던 상태에서는
JSON을 그대로 덤프하거나 본문을 요약해버릴 수 있었다 (v4에서 실제로 발생한 실패).

현재 규정:
- Agent 2 Responder — `final_report_text`를 한 글자도 바꾸지 않고 렌더(`\n`은 실제 줄바꿈,
  □/○/- 계층 유지) → 추적정보 → JSON 전문. 요약·문장 다듬기·블록 생략·내부 라벨 노출 금지.
- Agent 1 Responder — 스크리닝 목록 전건(EXCLUDE 포함) + handoff JSON 전문.
- 두 Responder 모두 `temperature 0`, `max_tokens 50000`.

## 당사(OWN_COMPANY) 현황의 출처

□ (현황) 당사 현황을 채우려면 05 검색계획이 당사 조회 태스크를 만들어야 한다.
당사 표기가 소스마다 다르므로 05에 소스별 매핑을 하드룰로 고정했다.

| 소스 | 표기 |
|---|---|
| mri_zeroin_public / public2 / etf | NH-Amundi운용 |
| mri_freesis | 엔에이치아문디자산운용 (협회 표기) |
| mri_news | 두 표기 + NH아문디 / NH-Amundi / NH아문디자산운용 |

ZeroIn 태스크에 협회 표기를, FreeSIS 태스크에 ZeroIn 표기를 쓰는 것을 금지한다.
당사 태스크는 `company_scope="OWN_COMPANY"`로 표시하고 경쟁사 쿼리와 분리한다.

연결된 소스가 없어 채울 수 없는 항목 — 과거 시도·중단 기획 / 파이프라인 / 채널 전략 /
부서 검토 이력 — 은 검색 태스크를 만들지 않고 `unresearchable_company_items`에 기록한다.
07이 이를 `data_gaps`로 승계하고 `final_report_domain_coverage`에
"내부 문서 소스 미연결" 사유를 남긴다. **빈 배열을 "당사는 해당 활동 없음"으로 읽지 않는다.**

## 관련 파일

- `05_runtime/AIR_MAPPING/MRI_Agent2_Research_Response_v2.json` — node 10 구현
- `06_project_docs/contracts/MRI_Handoff_Schema_v2.json` — Agent1 → Agent2 계약
- `06_project_docs/contracts/MRI_Hard_Fail_Evaluator_v2.json` — HF01–HF13
- `03_regression/regression_cases/MRI_Golden_Test_S06_v2.json` — S06 골든 케이스
