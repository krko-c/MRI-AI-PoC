# MRI AI PoC — DEVELOPMENT ROADMAP

**VERSION:** v20260818_r2

**ARCHITECTURE:** ADR-001 — Hypothesis-Driven External Research

**STATUS:** CURRENT DEVELOPMENT ROADMAP

---

# CURRENT POSITION

Phase 1 MRI Understanding은 substantially developed 상태다.

ADR-001에 따라 External Research를 Issue-first broad research에서 BO Hypothesis의 핵심 가정을 검증하는 targeted research로 재배치한다.

Current Next:

Business Opportunity Hypothesis Agent

Canonical Prompt Pack `v20260818`은 stored baseline으로 유지하며, External Evidence Component 04~07과 ZeroIn 08은 role/order revision 대상이다.

---

# PHASE 1 — MRI UNDERSTANDING

- Issue Extraction
- Fidelity Validator
- Screening

Status:

`SUBSTANTIALLY DEVELOPED`

Screening의 directness calibration warning과 Generalization 미검증 상태는 유지한다.

---

# PHASE 2 — BUSINESS OPPORTUNITY HYPOTHESIS

Status:

`NEXT DEVELOPMENT TARGET`

개발:

- BO Hypothesis Generator
- Company-blind generation
- 왜 국내 자산운용사 Opportunity가 될 수 있는지
- Opportunity scope
- 핵심 가정
- Evidence Questions
- 필요한 Evidence Category
- 아직 externally validated되지 않았음을 명시

사용 금지:

- Product RAG
- Fund DB
- Quant DB
- Internal History

---

# PHASE 3 — OPPORTUNITY VALIDATION ARCHITECTURE

개발:

- Opportunity Validation Router
- Evidence Question → Source selection
- Source purpose contract
- Targeted retrieval decision
- `ISSUE_DIRECT` 예외 조건
- `OPPORTUNITY_VALIDATION` Primary Mode

모든 Source를 자동 호출하지 않는다. 각 Evidence Question의 검증 목적과 필요한 Evidence Category에 따라 Source를 선택한다.

---

# PHASE 4 — RETRIEVAL LAYER

기존 개발내용을 재사용·재배치한다.

- Financial / AM News Retrieval
- Policy / Legal Retrieval
- ZeroIn Market Evidence Retriever
- FreeSIS Market Evidence Retriever

## ZeroIn Market Evidence Retriever

- 기존 v1.0/v1.1 개발 및 ZR-01~03 Regression 결과 활용
- 대표클래스 기준
- 패밀리 설정액 / NAV
- 1M / 3M / 6M / YTD 설정액·NAV 증감
- 모펀드 upstream 제외
- ETF class duplication 이슈 없음
- `OPPORTUNITY_VALIDATION`을 Primary Mode로 설정
- MRI Issue 자체가 fund/product market과 직접 대응될 때만 `ISSUE_DIRECT` 선택 허용
- `RELEVANT`, `POSSIBLY_RELEVANT`, `NOT_RELEVANT` 구분 유지
- `POSSIBLY_RELEVANT`를 확정 시장 Evidence로 사용하지 않음

## FreeSIS Market Evidence Retriever

- Opportunity Evidence Question 기반 설계
- Aggregate 설정 / 판매 / 유출입 / 운용사 구조
- 특정 Theme 또는 고객군 식별 가능성을 과대평가하지 않음

## Existing Components

04~07의 기존 Prompt는 삭제하지 않는다. ADR-001에 맞게 호출시점, 입력, purpose contract, output 역할을 재설계하기 전까지 `ARCHITECTURE REVISION PENDING`으로 취급한다.

---

# PHASE 5 — EVIDENCE NORMALIZATION & INTEGRATION

- External Evidence Extractor
- External Evidence Integrator
- BO Validation Decision

Validation status:

- `VALIDATED`
- `WEAK`
- `REJECTED`
- `INSUFFICIENT`

Evidence는 Source provenance, state/modality fidelity, `analysis_as_of_date`를 유지한다. MRI 재검증 Evidence와 BO Hypothesis 검증 Evidence를 구분한다.

---

# PHASE 6 — COMPANY STATE

- Product RAG
- Fund Universe
- Quant DB / TB_EARNING
- Internal History
- Integrated Current State

Rules:

- RAG no hit ≠ absence
- Missing data ≠ capability gap
- Past plan ≠ current execution
- Only verified Current State facts

BO Hypothesis 생성 및 Opportunity Validation 전에는 Company 자료를 사용하지 않는다.

---

# PHASE 7 — DECISION & STRATEGY

- Gap Analysis
- Strategy Hypothesis
- 필요시 Strategy-specific Research
- Final Strategy
- Final Response
- Quality Check

Gap Status:

- `KNOWN_DEFICIENCY`
- `UNKNOWN`
- `NO_MATERIAL_GAP`

`UNKNOWN`을 Gap으로 처리하지 않는다.

Strategy-specific Research는 경쟁사 실행사례, 판매채널 구조, 제도적 가능성, Partnership 방식 등 전략 실행 전제의 검증이 필요할 때만 수행한다.

---

# PHASE 8 — AIR RUNTIME

최종 구현은 하나의 AIR Studio import JSON으로 구성한다.

- AIR Node Mapping
- Tool / KB connection
- Supervisor / routing
- Input/output mapping
- Final single AIR Studio agent JSON
- E2E Regression

Then:

- Historical Replay Test
- Unseen MRI Generalization Test

---

# IMMEDIATE NEXT TASK

Business Opportunity Hypothesis Agent 설계

각 MRI Issue에 대해 회사자료를 사용하지 않고 다음을 생성한다.

1. Business Opportunity Hypothesis
2. 왜 국내 자산운용사 Opportunity가 될 수 있는지
3. Opportunity Scope
4. 핵심 가정
5. 검증이 필요한 Evidence Question
6. 필요한 Evidence Category

Output에는 아직 externally validated되지 않았음을 명시한다.

---

# END
