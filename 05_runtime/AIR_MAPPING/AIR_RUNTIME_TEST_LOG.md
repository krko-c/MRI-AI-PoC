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

## 2026-09-14 — Agent 1 기준 파일도 플랫폼 내보내기로 교체

`mri_stg_0_20260914_130516.json` 을 Agent 1 의 기준 파일로 채택.
프롬프트와 llm_model_setting 은 직전 레포 버전과 9개 노드 전부 동일했고,
차이는 **에어스튜디오가 관리하는 필드 3종**뿐이다. 내보내기에만 나타나므로
직접 만든 JSON 에는 없었다. 앞으로 노드를 추가·수정할 때 이 필드들을 지운 채
임포트하지 않는다.

| 필드 | 붙는 노드 | 이번 값 | 뜻 |
|---|---|---|---|
| `use_responser` | RESPONDER | `false` | 답변 노드 비활성화 상태. 화면 출력은 03X 가 만든다 |
| `recursion_limit` | AGENT | 01=20 · 02=15 · 03=15 · 03X=2 | 노드 1회 실행 중 허용되는 반복(도구 호출) 횟수 |
| `index_name` / `search_type` | KNOWLEDGBASE | `kb-6b0fd700` / `rag` | KB 조회 방식 |

**`search_type: "rag"` 는 추출 손실 진단을 확정한다.** KB 는 문서 전체가 아니라
질의에 맞는 청크만 돌려준다. `kb_return_diagnostic` 이 이슈별 회수율 25% 를
보고한 것과 일치하며, 01 에 이슈별 개별 호출 규칙을 넣은 근거가 여기 있다.

**`recursion_limit` 은 다음 실행에서 지켜볼 값이다.**
01 은 이제 구조 파악 1회 + 이슈별 7회 + 누락 항목 재조회 몇 회를 하도록 지시받는데,
이 반복이 20 을 넘으면 뒤쪽 이슈가 조회되지 않은 채 추출이 끝난다.
그 경우 프롬프트가 안 먹힌 것이 아니라 한도에 걸린 것이므로,
`self_check.kb_call_count` 가 20 부근에서 멈췄는지 먼저 확인한다.

## 2026-09-14 — 01 의 KB 조회 규칙을 되돌리고, 03X 변경만 남긴다

09-14 오전 실행은 끝까지 돌았다. 판정은 OPPORTUNITY 1 · MONITOR 3 · EXCLUDE 3,
요약표와 검토서가 화면에 나왔고, 슈퍼바이저 폭주도 답변 노드 재작성도 없었다.
결함은 두 가지뿐이었다 — `kb_call_count: 2` 로 인한 이슈별 회수율 부족,
그리고 핸드오프 JSON 이 S06 패키지 안에서 잘린 것.

그 다음 두 커밋이 첫 번째 결함을 고치려다 실행 자체를 깨뜨렸다.
호출 상한을 없앤 뒤 01 에서 플랫폼 체크섬 오류가 났고
(`expected 0x3a22496e, calculated 0x5dc5e9c6`), 8회로 묶은 뒤에도 원인은
확인되지 않았다. 오전 내내 한 번도 나지 않던 오류다.

**되돌린 것** — 01 프롬프트를 오전 실행본(`d6010a3`)으로 복원.
KB 호출은 다시 2회 상한, 이슈별 개별 조회 없음.
이슈별 회수율은 낮아지지만 02 가 원문 대조로 복원한다.
직전 실행에서 02 는 39개 항목을 되살렸고, 그것이 이 상한을 감당 가능하게 만드는 안전망이다.

**남긴 것** — 03X 의 출력 순서 변경(JSON 을 검토서보다 먼저)과
JSON 슬림화(lens reason · connection_logic · recommendation_reason · confidence 제거,
스키마 `2026-09-14.v5`). 이건 확인된 S06 잘림에 대한 수정이고, 체크섬 오류와 무관하다.
분량이 넘치면 검토서가 잘리고 연구 워크플로가 파싱해야 할 JSON 은 살아남는다.

**한 번에 하나씩.** 이번 실행에서 확인할 것은 JSON 이 `packager_self_check` 까지
도달하는지 하나다. 이슈별 조회는 그것이 확인된 뒤에 따로 시도한다.

### 추가 확인 — 8회 제한본도 같은 오류로 죽었다

되돌리기 직전 버전(호출 8회 상한 + 3~5낱말 질의 + 실패 시 건너뛰기)도
`Step 2: 이슈별 상세 조회` 를 시작하자마자 중단되었다.
체크섬 값은 두 실행 모두 **완전히 동일**하다 —
`expected 0x3a22496e, calculated 0x5dc5e9c6`.

이것이 뜻하는 바:

- 원인은 **호출 횟수가 아니다.** 상한 없는 버전과 8회 버전이 같은 자리에서 같은 값으로 죽었다.
- 원인은 **질의 길이도 아니다.** 3~5낱말로 묶은 뒤에도 동일하다.
- 값이 매번 같다는 건 **무작위 손상이 아니라 결정적**이라는 뜻이다.
  같은 객체를 같은 경로로 가져오다 같은 지점에서 실패한다.
- 실패 지점은 **구조 파악 1회 다음의 이슈별 조회 첫 호출**이다.
  오전 실행이 `kb_call_count: 2` 로 끝났다는 사실과 겹쳐 보면,
  2회까지는 통과하고 그 다음 성격의 조회에서 걸린다.

**결론: 이슈별 개별 조회는 프롬프트로 풀 수 있는 문제가 아니다.**
어떻게 묶어도 같은 오류가 난다. 회수율 개선은 플랫폼 쪽 KB 동작
(`search_type: rag` 의 청크 반환, 인덱스 재적재 여부)을 확인한 뒤에 다시 본다.
그때까지 01 은 오전 실행본 그대로 두고, 이슈별 세부 복원은 02 에 맡긴다.
