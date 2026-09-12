# AIR RUNTIME TEST LOG

## 2026-08-26 — MRI_WORKFLOW_v5_20260826_DRAFT.json

Status before AIR test:
- Import: NOT TESTED
- Routing: NOT TESTED
- Section ownership: NOT TESTED
- Placeholder safety: NOT TESTED
- Final preservation: NOT TESTED
- Functional quality: NOT READY / upstream research-current-state-department stages are placeholders

Known intentional gaps:
- External Research runtime not implemented
- Company Current State runtime not implemented
- Department Review runtime not implemented
- Current JSON extends v4 runtime schema but has not yet been imported into AIR Studio
- Cross-environment portability remains unverified

Test result:
- Fill after AIR Studio import/run.

## 2026-09-12 — MRI_Agent1_Screening_v2.json / MRI_Agent2_Research_Response_v2.json

AIR Studio 접속 불가로 정적 검증만 수행.

정적 검증 결과:
- JSON 파싱 PASS / v4 대비 스키마 키 100% 일치
- 끊어진 엣지 0 (Agent1 노드 9·엣지 9, Agent2 노드 36·엣지 36)
- 최상위 ID 및 공유 PK_ID 충돌 해소 (import 시 덮어쓰기 위험 제거)
- 07/08/09/10 각 노드 출력 계약 1개로 통합 (이중 계약 해소)
- 03X 출력 ↔ 04 입력 ↔ Handoff Schema v2 필드명 3자 일치

의도된 상태:
- Agent2의 01/02/03은 고립 노드(엣지 0). Agent1 없이 단독 실행할 때를 위한 DORMANT FALLBACK이며
  Supervisor는 04로 진입한다.
- 06B ZEROIN PUBLIC DETAIL에 KB 미연결. 사용자 판단으로 이번에는 유지.
  이 상태에서는 당사·경쟁사 모두 펀드 상세(설정액·성과) 조회가 실패하고 카탈로그 수준까지만 채워진다.

미검증 (AIR Studio 필요):
- Import / Graph Restore
- Supervisor 라우팅 및 04 진입
- 각 검색 노드의 실제 KB 호출 (kb_tool_called)
- Responder 통과 전용 동작 (final_report_text 원문 보존)
- must_preserve_themes가 traceability.covered/_unsupported로 회수되는지
- Functional quality — Golden Test S06 v2 채점

Test result:
- AIR Studio import/run 후 기입.
