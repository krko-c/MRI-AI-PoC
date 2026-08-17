# MRI AI PoC — MASTER PLAN

**VERSION:** v20260818  
**STATUS:** CURRENT MASTER PLAN

---

# 1. PROJECT OBJECTIVE

MRI 리포트의 주요 이슈를 구조화하고,
국내 자산운용사 관점에서 의미 있는 이슈를 선별한 뒤,
외부 Evidence와 당사 Current State를 독립적으로 분석하여
Business Opportunity, Gap, Strategy 및 최종 대응안을 생성하는
멀티에이전트 AI PoC를 구축한다.

최종 목적은 단순 MRI 요약이 아니다.

MRI 이슈를 기반으로:

1. 시장·정책·산업 변화 구조화
2. 자산운용사 관점 Screening
3. 외부 금융·자산운용 Evidence 탐색
4. Business Opportunity 도출
5. 당사 Current State 확인
6. Opportunity와 Current State 간 Gap 분석
7. 실행전략 제시
8. 최종 보고 형태로 종합

까지 자동화하는 것을 목표로 한다.

---

# 2. CORE ARCHITECTURE

전체 구조는 두 개의 독립 Lane으로 운영한다.

## A. MARKET / OPPORTUNITY LANE

MRI
→ Issue Extraction
→ Source/Fidelity Validation
→ Screening
→ External Evidence Source Routing
→ Retrieval Planning
→ External Evidence Retrieval
→ External Evidence Extraction
→ External Evidence Integration
→ Business Opportunity

이 Lane에서는 당사 Current State 정보를 사용하지 않는다.

즉 다음을 Business Opportunity 판단 전에 사용하지 않는다.

- 당사 상품
- Product RAG
- Fund DB
- 당사 성과
- 당사 기존 역량
- 당사 과거 대응
- 당사 History

Business Opportunity는 Company-blind하게 판단한다.


## B. COMPANY STATE LANE

MRI Issue
→ Product RAG
→ Fund Universe
→ Quant DB / TB_EARNING
→ Internal History
→ Integrated Current State

이 Lane은
"현재 당사가 무엇을 가지고 있고 실제 어떤 상태인가"
를 확인하는 역할만 수행한다.


## C. FIRST MEETING POINT

Business Opportunity
+
Integrated Current State
↓
Gap Analysis
↓
Strategy
↓
Final Response
↓
Quality Check

Business Opportunity와 Current State는
Gap Analysis 단계에서 처음 결합한다.

---

# 3. KEY DESIGN PRINCIPLES

## 3.1 CURRENT STATE DOES NOT DEFINE OPPORTUNITY

현재 당사에 없다는 사실은
사업기회가 없다는 의미가 아니다.

반대로 현재 당사에 있다는 사실도
해당 사업기회가 크다는 의미가 아니다.


## 3.2 UNKNOWN IS NOT ABSENCE

다음을 엄격히 구분한다.

UNKNOWN ≠ ABSENCE

RAG no hit ≠ 해당 상품 없음

데이터 없음 ≠ 역량 없음

과거 계획 ≠ 현재 실행


## 3.3 AS-OF DATE CONTROL

모든 Agent는 analysis_as_of_date를 따른다.

Historical Replay에서는
해당 시점 당시 이용 가능했던 정보만 사용한다.

미래 자료를 과거 시점 판단에 사용하지 않는다.


## 3.4 SOURCE PROVENANCE

사실과 판단은 가능한 경우 다음 Source Type으로 구분한다.

- MRI_SOURCE
- EXTERNAL_SOURCE
- CURRENT_PRODUCT_RAG
- CURRENT_FUND_DB
- CURRENT_QUANT_DB
- INTERNAL_HISTORY
- BUSINESS_OPPORTUNITY_INFERENCE


## 3.5 REMOVE CASE DEPENDENCE, NOT SPECIFICITY

Prompt 개선 목표는
구체성을 없애는 것이 아니다.

목표는 특정 Regression Case에만 맞는 규칙을 제거하면서도
판단 기준은 충분히 구체적으로 유지하는 것이다.

Prompt에는 다음을 유지한다.

- 판단원칙
- inclusion / exclusion criteria
- semantic dimensions
- edge case handling
- validation procedure
- synthetic examples

Production Prompt에
실제 Regression 회사명·숫자·문장을 넣지 않는다.


## 3.6 NO PROMPT PATCH FOR EVERY FAILURE

한 개 사례가 마음에 들지 않는다는 이유로
즉시 Prompt Rule을 추가하지 않는다.

Prompt 변경은 다음 경우에만 한다.

1. 반복적 구조 문제 발견
2. 기존 일반 Rule로 설명할 수 없는 Missing Principle 발견
3. Regression에서 동일 Failure Pattern 반복

기존 Rule이 충분한데 모델이 단순 실수한 경우에는
Prompt prose를 계속 추가하기보다
Schema, Validation, Process를 보완한다.

---

# 4. EXTERNAL EVIDENCE DESIGN

MRI 자체는 금융그룹 관점에서 이미 의미 있는 Issue다.

따라서 External Evidence Layer는
MRI의 일반 시장·산업 Fact를 다시 증명하는 데 사용하지 않는다.

External Evidence의 핵심 목적은 다음 세 가지다.

1. 정책·규제 조건
2. 금융회사 / 자산운용사의 실제 대응과 Business Model
3. 펀드·자산운용 시장의 실제 정량 Evidence


## Source Architecture

### 1. POLICY / REGULATION
- 대한민국 정책브리핑
- 필요 시 국가법령정보센터

### 2. FINANCIAL / AM INDUSTRY EVIDENCE
- NAVER News

### 3. ASSET MANAGEMENT / FUND MARKET
- ZeroIn
- FreeSIS

### 4. OPTIONAL MACRO
- BO 판단에 직접 필요한 경우만 사용

---

# 5. EXTERNAL DATA ROLE

## NAVER NEWS

역할:

- 자산운용사 실제 행동
- 은행·증권·보험 실제 행동
- 신규 서비스·사업모델
- 고객전략
- 금융업계 Emerging Trend

MRI 자체 재검증용으로 사용하지 않는다.


## ZEROIN

역할:

개별 국내 공모펀드 / ETF Evidence.

예상 Logical Fields:

- BASE_DATE
- FUND_CODE
- FUND_NAME
- MANAGER
- PUBLIC_FUND_YN
- ETF_YN
- PENSION_YN
- LARGE_TYPE
- SMALL_TYPE
- INCEPTION_DATE
- SETUP_AMOUNT
- AUM
- NET_FLOW

주의:

임의 테마 Tag가 있다고 가정하지 않는다.

상품명·분류 등을 통해 Candidate를 찾을 수 있으나,
이것만으로 해당 MRI Theme 관련 상품이라고 확정하지 않는다.


## FREESIS

역할:

시장 Aggregate / Flow / Sales / Manager Structure.

우선 활용 통계:

- 기간자금유출입
- 공사모구분
- 신규설정펀드현황
- 유형별기간설정
- 유형별판매규모
- 고객유형별판매규모
- 회사별자금유출입현황
- 회사별설정규모
- MMF현황
- 해외투자펀드현황
- ETF현황

주의:

FreeSIS가 특정 임의 Theme 또는 연령군을
직접 식별한다고 가정하지 않는다.

---

# 6. DEVELOPMENT / IT DESIGN LEVEL

현재 단계는:

FUNCTIONAL SPECIFICATION / LOGICAL DESIGN

이다.

지금 결정할 것:

- Agent 역할
- Agent Input / Output
- Source 선택 규칙
- Query 생성 논리
- Semantic Data Requirement
- Default Period
- Result Limits
- Candidate → Evidence Logic
- Required / Optional Fields

아직 확정하지 않을 것:

- 실제 DB Column
- 실제 API Syntax
- SQL
- Physical Table
- AIR Runtime Implementation

IT와 협의 후:

LOGICAL DESIGN
→ IT FEASIBILITY CHECK
→ PHYSICAL DATA MAPPING
→ POC IMPLEMENTATION SPEC

순서로 진행한다.

---

# 7. CURRENT COMPONENT STATUS

00 Architecture Contract v2
FROZEN

01 MRI Issue Extraction
FINAL CANDIDATE

02 Source / Fidelity Validator
FINAL CANDIDATE

03 MRI Screening
PRODUCTION CANDIDATE
Regression Passed with Directness Calibration Warning

04 Financial / AM News Search Planner v1.1
FINAL CANDIDATE

05 External Evidence Source Router v1.1
FINAL CANDIDATE

06 Policy / Legal Retrieval Planner v1.2
FINAL CANDIDATE

07 External Evidence Extractor v1.0
DRAFT
DO NOT USE YET

08 ZeroIn Retrieval / Candidate Finder
NEXT DEVELOPMENT TARGET

09 FreeSIS Retrieval Planner
NOT DEVELOPED

10 Unified Retrieval Contract
NOT DEVELOPED

External Evidence Integrator
NOT DEVELOPED

Business Opportunity Agent
ARCHITECTURE ONLY

Company State Lane
NOT DEVELOPED

Gap / Strategy / Final / QC
NOT DEVELOPED

AIR Runtime
UNVALIDATED / DEFERRED

GENERALIZATION VERIFIED
NO

---

# 8. REGRESSION POLICY

26-2 / 26-3 / 26-4
Development + Regression Set

H01 / H02
이미 Prompt 개선에 사용되었으므로
Unseen Holdout으로 재사용하지 않는다.

Synthetic Holdout은
Controlled Holdout일 뿐
Genuine Generalization Test로 간주하지 않는다.

최종 Generalization Test는
개발에 사용하지 않은 새로운 MRI로 수행한다.

---

# 9. DEVELOPMENT ENVIRONMENT

현재 개발/검증 환경:

Claude Web
Sonnet 4.5
Effort High 권장

현재 단계에서는
Claude Web을 이용해 Prompt / Schema / Regression Logic을 검증한다.

AIR Studio는
최종 Runtime Mapping 및 E2E Integration 단계에서 사용한다.

AIR Runtime 문제를
Prompt Logical Design 문제와 혼동하지 않는다.

---

# 10. PROJECT SOURCE OF TRUTH

우선순위:

1. Current Canonical Prompt Pack
2. Master Plan
3. Regression Log
4. IT Logical Specification
5. Archive
6. Conversation History

Conversation은 개발 논의 기록이다.

Canonical File이 실제 기준본이다.

---

# END