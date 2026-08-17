# MRI AI PoC — Architecture Decisions

## ADR-001 — Hypothesis-Driven External Research Architecture

Date: 2026-08-18
Status: ACCEPTED

### Context

기존 Architecture에서는 MRI Issue Extraction 및 Screening 이후 Issue-level External Evidence를 먼저 수집하고, 그 결과를 활용하여 Business Opportunity를 생성하는 구조를 검토하였다.

ZeroIn Retrieval / Candidate Finder를 개발하고 ZR-01, ZR-02, ZR-03 Regression을 수행하는 과정에서 다음 문제가 확인되었다.

1. MRI 자체가 이미 외부 환경 변화에 대한 분석자료이므로 모든 Issue에 대해 외부자료를 다시 선행 조사할 경우 MRI 내용을 재검증하는 작업이 발생할 수 있다.
2. 고령 1인가구, 기업 잉여자금 등과 같이 자산운용 상품과 직접 대응되지 않는 Issue에서는 BO가 생성되기 전에 ZeroIn/FreeSIS 검색을 수행하려면 모델이 먼저 상품 또는 금융솔루션을 추론해야 한다.
3. 이 경우 `Issue → inferred need → product/solution` 연결이 Retrieval 단계에서 발생하여 Business Opportunity Generation과 Retrieval의 역할이 혼합된다.
4. 실제로 필요한 외부조사는 Business Opportunity Hypothesis가 생성된 이후 해당 가설의 핵심 가정을 검증하는 방향으로 수행하는 것이 목적성과 효율성이 높다.

### Decision

External Research Architecture를 `Issue-first broad research`에서 `Hypothesis-driven targeted research`로 변경한다.

기본 흐름은 다음과 같다.

`MRI → Issue Extraction → Source/Fidelity Validation → Screening`

`→ Business Opportunity Hypothesis Generation → Evidence Question Generation`

`→ Opportunity Validation Router → Targeted External Research → Evidence Integration`

`→ Validated Business Opportunity → Company Current State → Gap Analysis`

`→ Strategy Hypothesis → 필요시 Strategy-specific Research → Final Strategy`

`→ Final Response → Quality Check`

### Business Opportunity Hypothesis

BO Hypothesis는 Company Current State를 보기 전에 생성한다.

입력:

- MRI Issue
- Screening Result
- 일반적인 국내 자산운용업 지식

다음 Company 자료는 사용하지 않는다.

- Product RAG
- Fund DB
- Quant DB
- Internal History

BO Hypothesis는 아직 확정된 Opportunity가 아니다.

각 BO Hypothesis는 함께 생성한다.

- Opportunity hypothesis
- 핵심 가정
- Evidence Question
- 필요한 Evidence Category

### Opportunity Validation Research

External Research의 주된 목적은 MRI Issue 자체를 다시 입증하는 것이 아니라 생성된 BO Hypothesis를 검증하는 것이다.

Evidence Question에 따라 필요한 Source만 호출한다.

가능한 Source:

- Naver News
- Policy / Legal
- ZeroIn
- FreeSIS
- 필요시 기타 공식 통계

모든 Source를 자동 호출하지 않는다.

### ZeroIn Role

ZeroIn의 주된 역할은 Business Opportunity Hypothesis와 관련된 실제 공모펀드/ETF 시장 Evidence를 확인하는 것이다.

확인 가능한 주요 Evidence:

- 관련 상품 존재 여부
- 상품 수
- 운용사 수
- 패밀리 설정액
- 패밀리 NAV
- 1M / 3M / 6M / YTD 패밀리 설정액 증감
- 1M / 3M / 6M / YTD 패밀리 NAV 증감
- 신규 상품 존재

ZeroIn은 필요시 Issue 단계에서도 사용할 수 있으나, MRI Issue 자체가 펀드/투자시장과 직접 대응되는 경우에 한한다.

ZeroIn Market Evidence Retriever는 장기적으로 동일한 Retrieval Engine을 재사용하되 호출 목적을 구분한다.

MODE A — `ISSUE_DIRECT`

- MRI Issue 자체가 직접적인 펀드/투자시장 표현을 가질 때만 사용
- 선택적 사용

MODE B — `OPPORTUNITY_VALIDATION`

- BO Hypothesis 생성 후 해당 Opportunity와 관련된 실제 펀드시장 Evidence를 검증
- ZeroIn의 주된 사용 Mode

### FreeSIS Role

FreeSIS도 모든 MRI Issue에 선행 호출하지 않는다.

Opportunity Validation 과정에서 산업 전체의 설정/판매/유출입/운용사 구조 등 Aggregate Market Evidence가 필요한 경우 호출한다.

### Strategy-specific Research

Validated Business Opportunity와 Company Current State를 결합하여 Gap 및 Strategy Hypothesis를 생성한 후에도 전략 실행방식 자체에 추가 검증이 필요한 경우 Strategy-specific Research를 수행할 수 있다.

예:

- 실제 경쟁사 실행사례
- 판매채널 구조
- 제도적 가능성
- 특정 Partnership 방식

Opportunity Validation Research와 목적을 구분한다.

### Preserved Architecture Principles

다음 기존 원칙은 유지한다.

- Current State does not define Business Opportunity.
- Company State와 Business Opportunity는 Gap Analysis 전까지 분리한다.
- UNKNOWN ≠ ABSENCE.
- `analysis_as_of_date`를 준수한다.
- Historical replay에서는 기준일 이후 정보를 사용하지 않는다.
- Company 자료는 BO 생성 및 BO 외부검증 전에 사용하지 않는다.
- External Evidence는 provenance를 유지한다.

### Impact

다음 Component의 역할 또는 순서를 재검토해야 한다.

- 04 Financial / AM News Search Planner
- 05 External Evidence Source Router
- 06 Policy / Legal Retrieval Planner
- 07 External Evidence Extractor
- 08 ZeroIn Retrieval / Candidate Finder
- 예정된 09 FreeSIS Retrieval Planner

기존 Prompt는 삭제하지 않는다.

현재 Canonical Prompt Pack은 새 Architecture에 맞춘 Component 재설계가 끝날 때까지 저장된 baseline으로 보존한다.

단, 04~07 External Evidence Layer와 08 ZeroIn의 현재 위치/호출목적은 `ARCHITECTURE REVISION PENDING` 상태로 취급한다.
