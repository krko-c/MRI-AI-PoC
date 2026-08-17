# MRI AI PoC — MASTER PLAN

**VERSION:** v20260818_r2

**STATUS:** CURRENT MASTER PLAN

**ARCHITECTURE DECISION:** ADR-001 ACCEPTED

---

# 1. PROJECT OBJECTIVE

MRI 리포트의 주요 이슈를 구조화하고 국내 자산운용사 관점에서 의미 있는 이슈를 선별한 뒤, Company-blind Business Opportunity Hypothesis를 생성한다. 각 가설의 핵심 가정을 Evidence Question 기반 외부조사로 검증하고, 검증된 Opportunity와 당사 Current State를 독립적으로 분석하여 Gap, Strategy 및 최종 대응안을 생성하는 멀티에이전트 AI PoC를 구축한다.

최종 목적은 단순 MRI 요약이나 MRI 사실의 반복 검증이 아니다.

1. 시장·정책·산업 변화 구조화
2. 자산운용사 관점 Screening
3. Company-blind Business Opportunity Hypothesis 생성
4. 핵심 가정과 Evidence Question 생성
5. Targeted External Research를 통한 Opportunity 검증
6. 당사 Current State 확인
7. Opportunity와 Current State 간 Gap 분석
8. Strategy Hypothesis 및 필요시 Strategy-specific Research
9. 최종 전략과 보고 형태 종합

---

# 2. CORE ARCHITECTURE

## A. MRI UNDERSTANDING

`MRI → Issue Extraction → Source/Fidelity Validation → Screening`

MRI 원문 충실성, Issue Boundary, 실행상태 및 자산운용사 관련성을 확정한다.

## B. BUSINESS OPPORTUNITY HYPOTHESIS

`Screened MRI Issue → Business Opportunity Hypothesis Generation`

BO Hypothesis는 다음을 포함한다.

- Company-blind Opportunity hypothesis
- 왜 국내 자산운용사 Opportunity가 될 수 있는지
- Opportunity scope
- 핵심 가정
- Evidence Questions
- 필요한 Evidence Category
- 아직 externally validated되지 않았다는 상태

입력은 MRI Issue, Screening Result, 일반적인 국내 자산운용업 지식으로 제한한다. Product RAG, Fund DB, Quant DB, Internal History 등 Company 자료는 사용하지 않는다.

## C. OPPORTUNITY VALIDATION

`BO Hypothesis → Evidence Question Generation → Opportunity Validation Router`

`→ Targeted News / Policy / Legal / ZeroIn / FreeSIS / 기타 공식 통계`

`→ Evidence Normalization → Evidence Integration`

`→ Validated / Weak / Rejected / Insufficient Business Opportunity`

Evidence Question에 필요한 Source만 선택하며 모든 Source를 자동 호출하지 않는다.

## D. COMPANY STATE LANE

Validated Business Opportunity와 독립적으로 Company Current State를 확인한다.

`MRI Issue → Product RAG → Fund Universe → Quant DB / TB_EARNING`

`→ Internal History → Integrated Current State`

이 Lane은 현재 당사가 무엇을 가지고 있고 실제 어떤 상태인지 확인하는 역할만 수행한다.

## E. DECISION AND STRATEGY

`Validated Business Opportunity + Integrated Current State → Gap Analysis`

`→ Strategy Hypothesis → 필요시 Strategy-specific Research`

`→ Final Strategy → Final Response → Quality Check`

Business Opportunity와 Current State는 Gap Analysis에서 처음 결합한다.

---

# 3. HYPOTHESIS-DRIVEN EXTERNAL RESEARCH

## 3.1 ARCHITECTURE CHANGE

OLD:

MRI Issue 중심의 선행 External Evidence 수집

NEW:

BO Hypothesis를 먼저 생성하고, 각 BO의 핵심 가정을 검증하기 위한 Evidence Question 기반 Targeted Research 수행

예외적으로 MRI Issue 자체가 fund/product market과 직접 대응되는 경우에는 Issue-level direct market evidence retrieval을 선택적으로 허용한다.

## 3.2 OPPORTUNITY VALIDATION RESEARCH

주된 목적은 MRI Issue 자체를 재입증하는 것이 아니라 BO Hypothesis의 핵심 가정을 검증하는 것이다.

가능한 Source:

- Naver News: 금융회사 실제 행동, 사업모델, 고객전략, 경쟁사 실행
- Policy / Legal: 정책·규제 조건, 적용대상, 실행 가능성
- ZeroIn: 실제 공모펀드/ETF 상품시장 Evidence
- FreeSIS: Aggregate 설정·판매·유출입·운용사 구조
- 기타 공식 통계: Evidence Question에 직접 필요한 경우

## 3.3 ISSUE-DIRECT EXCEPTION

MRI Issue 자체에 직접적인 펀드·ETF·자금흐름·투자시장 표현이 있는 경우에만 `ISSUE_DIRECT` Mode로 시장 Evidence를 선택적으로 조회할 수 있다. Retrieval 단계에서 inferred need나 product/solution을 새로 만들지 않는다.

## 3.4 STRATEGY-SPECIFIC RESEARCH

Gap과 Strategy Hypothesis 생성 후 실행방식에 추가 검증이 필요할 때 수행한다. 경쟁사 실행사례, 판매채널 구조, 제도적 가능성, Partnership 방식 등을 검증할 수 있으며 Opportunity Validation Research와 목적 및 provenance를 구분한다.

---

# 4. PRESERVED DESIGN PRINCIPLES

## 4.1 CURRENT STATE DOES NOT DEFINE OPPORTUNITY

현재 당사에 없다는 사실은 사업기회가 없다는 의미가 아니며, 현재 당사에 있다는 사실도 해당 사업기회가 크다는 의미가 아니다.

## 4.2 COMPANY-BLIND OPPORTUNITY

BO Hypothesis 생성과 Opportunity 외부검증이 끝날 때까지 Company State 자료를 사용하지 않는다.

## 4.3 UNKNOWN IS NOT ABSENCE

`UNKNOWN ≠ ABSENCE`를 유지한다. RAG no hit는 상품 부재가 아니며, 데이터 없음은 역량 없음이 아니고, 과거 계획은 현재 실행이 아니다.

## 4.4 AS-OF DATE CONTROL

모든 Agent는 `analysis_as_of_date`를 따른다. Historical Replay에서는 해당 시점 당시 이용 가능했던 정보만 사용한다.

## 4.5 SOURCE PROVENANCE

사실과 판단은 가능한 경우 다음 Source Type으로 구분한다.

- MRI_SOURCE
- EXTERNAL_SOURCE
- CURRENT_PRODUCT_RAG
- CURRENT_FUND_DB
- CURRENT_QUANT_DB
- INTERNAL_HISTORY
- BUSINESS_OPPORTUNITY_INFERENCE

## 4.6 PROMPT DEVELOPMENT DISCIPLINE

Case dependence를 제거하되 판단 기준의 구체성은 유지한다. 반복적 구조 문제나 Missing Principle이 확인될 때만 Prompt를 변경하고, 개별 실행 실수마다 Prompt prose를 추가하지 않는다. Production Prompt에는 실제 Regression 사례가 아닌 Synthetic Example을 사용한다.

---

# 5. SOURCE ROLES

## 5.1 NAVER NEWS

Opportunity Evidence Question 또는 Strategy-specific Question에 필요한 금융회사 실제 행동, 신규 서비스·사업모델, 고객전략, 경쟁활동을 확인한다. MRI 자체 재검증용으로 사용하지 않는다.

## 5.2 POLICY / LEGAL

Opportunity 또는 Strategy의 정책·법적 전제, 적용대상, 허용·제한 조건을 확인한다. 정책 발표와 법적 효력 발생을 구분한다.

## 5.3 ZEROIN

Primary Mode는 `OPPORTUNITY_VALIDATION`이다. BO Hypothesis와 관련된 실제 공모펀드/ETF 시장 Evidence를 확인한다.

주요 Evidence:

- 관련 상품 존재 여부
- 상품 수 및 운용사 수
- 대표클래스 기준 패밀리 설정액과 NAV
- 1M / 3M / 6M / YTD 패밀리 설정액·NAV 증감
- 신규 상품 존재

모펀드는 upstream에서 제외한다. Fund Name Match만으로 Theme을 확정하지 않으며, `POSSIBLY_RELEVANT`는 확정 Evidence로 사용하지 않는다.

## 5.4 FREESIS

Opportunity Evidence Question에 산업 전체의 설정, 판매, 유출입, 운용사 구조 등 Aggregate Market Evidence가 필요한 경우 호출한다. 특정 임의 Theme 또는 고객군을 직접 식별한다고 가정하지 않는다.

---

# 6. DEVELOPMENT / IT DESIGN LEVEL

현재 단계는 `FUNCTIONAL SPECIFICATION / LOGICAL DESIGN`이다.

현재 결정할 사항:

- Agent 역할과 Input / Output
- BO Hypothesis와 Evidence Question Schema
- Evidence Question → Source 선택 규칙
- Source purpose contract
- Semantic Data Requirement
- Candidate → Evidence Logic
- BO Validation Decision
- Required / Optional Fields

아직 확정하지 않을 사항:

- 실제 DB Column 및 API Syntax
- SQL과 Physical Table
- 최종 AIR Runtime Implementation

Logical Design → IT Feasibility Check → Physical Data Mapping → PoC Implementation Spec 순서로 진행한다.

---

# 7. CURRENT COMPONENT STATUS

- 00 Architecture Contract v2: BASELINE PRINCIPLES PRESERVED / WORKFLOW SUPERSEDED IN PART BY ADR-001
- 01 MRI Issue Extraction: FINAL CANDIDATE
- 02 Source / Fidelity Validator: FINAL CANDIDATE
- 03 MRI Screening: PRODUCTION CANDIDATE, directness calibration warning
- Business Opportunity Hypothesis Agent: NEXT DEVELOPMENT TARGET
- 04 Financial / AM News Search Planner: EXISTING BASELINE / ARCHITECTURE REVISION PENDING
- 05 External Evidence Source Router: EXISTING BASELINE / ARCHITECTURE REVISION PENDING
- 06 Policy / Legal Retrieval Planner: EXISTING BASELINE / ARCHITECTURE REVISION PENDING
- 07 External Evidence Extractor: DRAFT / ARCHITECTURE REVISION PENDING
- 08 ZeroIn Retrieval / Candidate Finder: LOGIC DEVELOPED AND REGRESSION-TESTED / ROLE REPOSITIONING TO OPPORTUNITY_VALIDATION
- 09 FreeSIS Retrieval Planner: NOT DEVELOPED
- External Evidence Integrator: NOT DEVELOPED
- Company State Lane: NOT DEVELOPED
- Gap / Strategy / Final / QC: NOT DEVELOPED
- AIR Runtime: UNVALIDATED / DEFERRED
- Generalization verified: NO

Architecture Contract v2의 `Current State does not define Opportunity`, Company State / Opportunity separation, `UNKNOWN ≠ ABSENCE`, `analysis_as_of_date` 등 핵심원칙은 유지한다. 다만 기존 External Research의 순서와 역할은 ADR-001에 의해 일부 대체되었다.

현재 Canonical Prompt Pack `v20260818`은 저장된 baseline으로 유지한다. ADR-001 영향 Component 재설계가 완료된 후 새 Canonical Pack으로 일괄 승격한다.

---

# 8. REGRESSION POLICY

26-2 / 26-3 / 26-4는 Development + Regression Set이다. H01 / H02는 Prompt 개선에 사용되었으므로 Unseen Holdout으로 재사용하지 않는다. Synthetic Holdout은 Controlled Holdout이며 Genuine Generalization Test로 간주하지 않는다. 최종 Generalization Test는 개발에 사용하지 않은 새로운 MRI로 수행한다.

ZeroIn ZR-01~03 결과는 Retrieval logic 재사용과 Primary Mode 재배치의 근거로 유지한다.

---

# 9. DEVELOPMENT ENVIRONMENT AND RUNTIME

현재 Prompt, Schema, Regression Logic은 logical design 환경에서 검증한다. AIR Studio는 Component 재설계와 IT Mapping 이후 최종 Runtime Mapping 및 E2E Integration 단계에서 사용한다.

최종 구현은 AIR Node Mapping, Tool / KB connection, Supervisor / routing, Input/output mapping을 포함한 하나의 AIR Studio import JSON으로 구성한다.

AIR Runtime 문제와 Prompt Logical Design 문제를 혼동하지 않는다.

---

# 10. PROJECT SOURCE OF TRUTH

우선순위:

1. Current Canonical Prompt Pack
2. Latest Master Plan and accepted Architecture Decisions
3. Regression Log
4. IT Logical Specification
5. Archive
6. Conversation History

Canonical Prompt Pack `v20260818`은 실행 baseline으로 보존되지만 ADR-001 영향 Component 04~08은 Architecture Revision Pending이다. 새 Architecture 구현 기준은 accepted ADR과 이 Master Plan의 상태 표시를 함께 따른다.

---

# 11. IMMEDIATE NEXT DEVELOPMENT

Business Opportunity Hypothesis Agent를 설계한다.

각 MRI Issue에 대해 Company 자료를 사용하지 않고 다음을 생성한다.

1. Business Opportunity Hypothesis
2. 왜 국내 자산운용사 Opportunity가 될 수 있는지
3. Opportunity Scope
4. 핵심 가정
5. 검증이 필요한 Evidence Question
6. 필요한 Evidence Category

---

# END
