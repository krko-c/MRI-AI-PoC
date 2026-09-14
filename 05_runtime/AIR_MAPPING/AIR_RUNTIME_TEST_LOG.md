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

## 2026-09-14 — Agent 2 기준 파일을 플랫폼 내보내기로 교체

`mri_stg_20260914_090243.json` (AIR Studio 내보내기) 를 Agent 2 의 기준 파일로 채택.
앞으로 Agent 2 수정은 이 파일을 출발점으로 한다.

**직전 레포 버전 대비 변경**
- `kb-2831d472` 노드 추가, `06B ZEROIN PUBLIC DETAIL → kb-2831d472` 엣지 추가 (사용자 작업)
- 노드 37 / 엣지 37, 고립노드 없음, 중복 엣지 없음, Agent 1 과 PK 충돌 0
- 전 노드의 프롬프트와 max_tokens 는 직전 레포 버전과 동일 (16000 / 50000 두 값만 존재)

**형식 차이 — 이후 편집 시 반드시 유지**
JoinMaps 스키마가 다르다. 플랫폼 내보내기는 엣지에 `PK_ID` 가 없고
`MAPPINGVALUE` / `SubDesc` 를 갖는다. 직전 레포 버전은 v1 에서 파생된 형태라
엣지에 `PK_ID` 가 있었다. 왕복이 검증된 쪽은 플랫폼 내보내기 형식이므로
엣지를 추가·수정할 때 `PK_ID` 를 새로 만들어 넣지 않는다.

| | 플랫폼 내보내기(현행) | 직전 레포 버전 |
|---|---|---|
| JoinMap 키 | FK_START_MAP_ID, FK_END_MAP_ID, edge_type, MAPPINGVALUE, DisplayName, SubDesc, condition_key | FK_START_MAP_ID, FK_END_MAP_ID, edge_type, DisplayName, condition_key, PK_ID |

**해소된 기존 제약**
06B 미연결 상태가 해소되어 `mri_zeroin_public2` (펀드 상세, 설정액 2시점) 의
의존 검색 경로가 열렸다. 이전 수동 실행의 "06B KB 미연결" 단서는 더 이상 적용되지 않는다.

**남은 미연결**
`mri_zeroin_etf` (06C 의 kb-f01bb5d9) 는 연결되어 있으나 수동 실행 환경에서는
디렉터리가 없어 RETRIEVAL_ERROR 로 처리되었다. 플랫폼에서의 동작은 실행으로 확인 필요.
06P / 06R1 / 06R2 / 06R3 / 06S / 06T / 06X 는 계획·수집·판정 노드이므로 KB 미연결이 정상이다.
