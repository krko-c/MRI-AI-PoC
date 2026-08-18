# MRI AI PoC Development Roadmap v20260818 r3

## 0. 변경 요약
- 전체 Logical Workflow 유지
- Logical Step과 AIR Agent 분리 관리
- BO 이후 Agent 수 사전 확정 금지
- AIR는 runtime topology 최소 검증 우선
- 데이터셋 요청은 BO / Evidence Question / Validation Router 논리 설계 이후
- 최종 요청부서/요청내용은 Strategy 이후 확정
- Generalization 미검증 유지

---

## Phase A. Front Pipeline AIR 최소 안정화

목적: `CURRENT_MRI → Extraction → Fidelity → Screening`이 AIR에서 stage ownership을 유지하며 동작하는지 확인.

### 이미 확인
- CURRENT_MRI KB 호출 가능
- 전체 이슈 #1~#7 추출 가능
- Agent → KB / Tool 가능
- Conditional 가능
- Export → Import → Run 가능
- 현재 AIR 환경에서 KB reference restore 가능

### 2026-08-18 발견
직렬 FLOW에서 후속 Agent가 앞 단계를 재수행하거나, 앞 Agent가 사용자 전체 요청을 스스로 끝내는 현상 발생.

### 현재 실험 후보
```text
Supervisor
  ├→ 01 Extraction
  ├→ 02 Fidelity
  └→ 03 Screening
```
Supervisor가 각 Stage를 순차 호출하고 결과를 검사한 뒤 다음 Stage 호출.

### 현재 상태
- `MRI_01_02_03_v4_SUPERVISOR_ORCHESTRATED.json` 생성 완료
- runtime test **PENDING**

### Exit Criteria
- Supervisor → 01 → Supervisor → 02 → Supervisor → 03 순차 호출
- 각 Agent stage ownership 유지
- 7개 이슈 count/order 유지
- Screening 5 Lens / no-total 규칙 준수

---

## Phase B. BO Hypothesis Logical Development

### 개발 순서
1. Input Contract
2. Output Schema
3. Hypothesis Chain
4. Critical Assumption
5. Evidence Question link
6. H01/H02 regression
7. MRI #4/#5 replay

### Exit Criteria
- MRI fact와 inference 분리
- 회사 내부현황 사용 없음
- 외부 fact를 검증된 것처럼 쓰지 않음
- 가설이 실제 검증 질문으로 전환됨

---

## Phase C. Evidence Question + Opportunity Validation Router

해야 할 일:
- Evidence Category taxonomy
- ZeroIn / FreeSIS / News / Policy routing rule
- timeframe / grain / filter rule
- data unavailable 처리
- `UNKNOWN != ABSENCE`

Exit Criteria:
- 실제 BO 3~5개에 대해 evidence question 명확
- 각 question의 data source 결정
- 불필요한 전체조회/중복조회 없음

---

## Phase D. Dataset Requirement Specification

데이터셋 요청 전에 아래를 데이터별 확정한다.

| 항목 | 설명 |
|---|---|
| Dataset Purpose | 왜 필요한가 |
| Agent / Logical Step | 어디서 사용하는가 |
| Query Intent | 어떤 질문에 답하는가 |
| Grain | 펀드별 / 유형별 / 일자별 / 기사별 |
| Required Fields | 필수 컬럼 |
| Optional Fields | 선택 컬럼 |
| As-of Date | 기준일 조회 |
| Historical Replay | 과거 시점 재현 |
| Filter | 공모/사모/ETF 등 |
| Evidence ID | 추적 가능한 key |
| UNKNOWN Rule | 0 / 없음 / 미확인 구분 |
| Tool Input | 조회 입력 |
| Tool Output | 반환 schema |

### ZeroIn 후보 필드
AS_OF_DATE, FUND_CODE, FUND_NAME, REPRESENTATIVE_CLASS_NAME, MANAGER, PUBLIC_FUND_YN, ETF_YN, PENSION_YN, LARGE_TYPE, SMALL_TYPE, INCEPTION_DATE, FAMILY_SETUP_AMOUNT, FAMILY_NAV, SETUP_CHANGE_1M/3M/6M/YTD, NAV_CHANGE_1M/3M/6M/YTD

### FreeSIS 후보 메뉴
기간자금유출입, 공사모, 신규설정펀드, 유형별기간설정, 유형별판매규모, 고객유형별판매규모, 회사별자금유출입, 회사별설정규모, MMF, 해외투자펀드, ETF

### News 최소 요구
CONTENT_ID, PUBLISHED_DATE, SOURCE_NAME, TITLE, SUMMARY, CONTENT_TEXT, URL, CATEGORY

### Policy / Legal 최소 요구
DOCUMENT_ID, PUBLISHED_DATE, EFFECTIVE_DATE, ISSUER, TITLE, DOCUMENT_TYPE, CONTENT_TEXT, STATUS, URL

---

## Phase E. IT Dataset / Tool Request

Phase B~D 완료 후 ZeroIn / FreeSIS / News / Policy를 한 번의 요청 묶음으로 제출.

각 dataset별:
- 목적
- 필드
- 조회단위
- 시간 기준
- sample query
- expected output
- AIR 호출 방법/API 또는 Tool interface

CURRENT_MRI page provenance가 계속 불가능하면 PDF page-text parser/page metadata를 별도 runtime dependency 후보로 둔다.

---

## Phase F. External Research / Evidence Integration
데이터 수령 후 BO별 evidence question 실행, evidence normalization, contradictory evidence 처리, Evidence Integration, BO 상태 갱신.

---

## Phase G. Company Current State
외부 BO 검증 후에만 실행.
당사 상품, 펀드 현황, 마케팅/사업, 과거 MRI 대응, 내부 검토 이력.

---

## Phase H. Gap / Strategy
```text
Validated Opportunity
VS
Company Current State
→ Gap
→ Strategy Hypothesis
```
필요 시 Strategy-specific external research 추가.

---

## Phase I. Final Department Routing / Final Response / QC

최종 Department Routing 출력:
- request_required
- department
- request_reason
- requested_current_state
- requested_plan
- specific_questions
- due-date / format metadata (사용자가 제공한 경우)

QC:
- MRI fact / inference / external evidence 구분
- as-of date / historical replay
- provenance
- unsupported named entities
- state/modality
- company-state leakage
- recommendation overreach

---

## 전체 우선순위

### 지금
1. AIR v4 orchestration 1회 검증
2. BO Hypothesis 설계

### 그 다음
3. Evidence Question
4. Validation Router
5. Dataset logical spec
6. IT 요청

### 데이터 수령 후
7. Evidence retrieval/integration
8. Company State
9. Gap / Strategy
10. Final Department Routing / Response / QC

---

## 개발 중단 조건
이미 존재하는 abstract rule을 모델이 실행하지 못하는 경우 Prompt prose를 계속 추가하지 않는다.

우선순위:
```text
Prompt prose 추가 X
Schema / process / orchestration / validation gate 수정 O
```

Production Prompt에는 실제 regression case의 고유명사/실제 수치를 예시로 박아 넣지 않는다.
