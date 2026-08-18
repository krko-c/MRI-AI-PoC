# MRI AI PoC Master Plan v20260818 r3

## 0. 문서 목적

본 문서는 MRI AI PoC의 현재 논리 아키텍처, 개발 원칙, AIR Studio 물리 구현 원칙, 데이터 검증 구조를 하나의 기준선으로 정리한다.

r3의 핵심 변경은 **전체 논리 Flow를 변경하는 것이 아니라, Logical Step과 Physical Agent를 분리하여 관리하는 것**이다.
2026-08-18 AIR Studio 실험에서 Agent 간 handoff와 stage ownership이 별도 설계 이슈임이 확인되었으므로, 앞으로는 논리 단계 하나를 곧바로 Agent 하나로 간주하지 않는다.

> 상태 표기 원칙
> - Logical Design과 AIR Runtime 상태를 별도로 기록한다.
> - Runtime 미실행 구조를 PASS로 기록하지 않는다.
> - `GENERALIZATION VERIFIED`는 실제 미확인 상태에서 사용하지 않는다.

---

## 1. Source of Truth

프로젝트 내 충돌 시 아래 우선순위를 따른다.

1. Accepted ADR
2. 최신 Master Plan / Development Roadmap
3. Canonical Prompt Pack
4. Regression Log
5. IT Logical Spec
6. Runtime / AIR Mapping 기록
7. Archive
8. Conversation History

### ADR-001
현재 채택 아키텍처는 **Hypothesis-Driven External Research Architecture**이다.

핵심 원칙:
- 외부조사는 MRI 이슈를 다시 증명하기 위한 것이 아니라 **Business Opportunity 가설을 검증**하기 위한 것이 원칙이다.
- MRI 자체가 펀드/상품시장으로 직접 연결되는 경우에만 issue-level direct market retrieval을 예외적으로 허용한다.
- Company Current State는 Business Opportunity를 정의하지 않는다.
- Opportunity와 Company State를 분리한 후 Gap 단계에서 결합한다.
- `UNKNOWN != ABSENCE`
- 모든 분석은 `analysis_as_of_date`를 가진다.
- Historical replay 시 as-of 시점 이후 정보 사용 금지.
- BO 생성 및 BO 외부검증 단계에서 회사 내부 상품/현황 데이터 사용 금지.
- Provenance를 가능한 한 보존한다.

---

## 2. 전체 Logical Workflow

```text
CURRENT MRI
  ↓
Issue Extraction
  ↓
Source / Fidelity Validation
  ↓
MRI Screening
  ↓
Business Opportunity Hypothesis
  ↓
Evidence Question Generation
  ↓
Opportunity Validation Router
  ↓
Targeted External Research
  ├─ ZeroIn
  ├─ FreeSIS
  ├─ News
  └─ Policy / Legal
  ↓
Evidence Integration
  ↓
Validated Business Opportunity
  ↓
Company Current State
  ↓
Gap Analysis
  ↓
Strategy Hypothesis
  ↓
필요 시 Strategy-specific Research
  ↓
Final Strategy
  ↓
Final Department Routing / Request Design
  ↓
Final Response
  ↓
QC
```

### 요청부서 처리 위치

앞단 Screening에서는 `department_candidates` 수준의 후보를 낼 수 있다.
최종 요청부서, 요청사유, 요청자료, 질문항목은 원칙적으로 다음을 모두 본 뒤 확정한다.

```text
Validated BO
+ Company Current State
+ Gap / Strategy
→ Final Department Routing
```

급한 현업 대응 시에는 Screening 결과만으로 임시 부서 요청을 먼저 할 수 있으나, 이는 정상 최종 경로와 구분한다.

---

## 3. Logical Step ≠ Physical Agent

앞으로 `Logical Step 1개 = AIR Agent 1개`로 보지 않는다.

### 별도 Agent로 분리할 실익이 큰 경우
- 사용하는 데이터 원천 또는 권한이 다름
- 서로의 정보를 미리 보면 판단 편향이 생김
- 독립적인 품질 검증이 실제로 필요함
- 병렬/독립 조사 후 통합하는 것이 명확함

### 한 Agent 내부 STEP으로 합칠 수 있는 경우
- 동일 원천을 읽고 연속 추론하는 작업
- 단순히 사고 순서만 다름
- Agent handoff가 새로운 오류를 유발함
- 중간 출력의 외부 독립성이 필요하지 않음

따라서 현재 `Issue Extraction → Fidelity → Screening`은 **Logical 3-Step으로 유지**하되, 최종 Physical Agent 개수는 AIR 안정화 결과를 보고 확정한다.
같은 원칙을 `BO Hypothesis → Evidence Question → Validation Router`에도 적용한다.

---

## 4. Front Pipeline Logical Contract

### 4.1 Issue Extraction
- CURRENT_MRI 최상위 이슈 전수 추출
- 문서 순서와 제목/상태 표현 보존
- 사업성/상품성 판단 금지
- 페이지 메타데이터가 없으면 `page=null`, `source_pages=[]`

### 4.2 Source / Fidelity Validation
- Extraction 결과가 MRI 원문에 충실한지 검증
- 외부 현실세계의 사실 진위 검증이 아님
- 검증: source boundary, issue boundary, title fidelity, state/modality, mixed-state aggregation, recommendation leakage, provenance
- 원문 제목의 `대응/점검/진단/필요` 자체를 recommendation leakage로 판정하지 않음

### 4.3 MRI Screening
5개 Lens:
- product
- investment_theme
- customer
- channel
- group_collaboration

각 Lens 0/1/2, 총점 금지.

분류:
- 어느 Lens든 2 → `OPPORTUNITY`
- 2 없이 1 이상 → `MONITOR`
- 전부 0 → `EXCLUDE`
- Fidelity FAIL → `VALIDATION_BLOCKED`

### Score 2 Gate
```text
MRI-confirmed change
→ concrete asset-manager mechanism
→ practical use
```

`성장산업 → 관련 기업 존재 추정 → ETF 가능`은 원칙적으로 최대 1점이다.
실제 investable universe, 유동성, 상품경쟁, 시장성 등을 외부 검증해야 2점이 성립한다면 현재 단계는 1점으로 둔다.

---

## 5. Business Opportunity Architecture

### Input
- MRI Issue
- Screening Result
- `analysis_as_of_date`

허용: 일반적인 국내 자산운용 기능 지식

금지:
- Company Product RAG
- Internal Fund DB
- Internal History
- retrieved external evidence

### Output
- `opportunity_id`
- `hypothesis`
- `opportunity_scope`
- `asset_manager_role`
- `asset_manager_connection`
- `hypothesis_chain`
- `critical_assumptions`
- `evidence_questions`
- `validation_status = UNVALIDATED`

Traceability:
```text
BO_ID → ASSUMPTION_ID → EVIDENCE_QUESTION_ID
```

---

## 6. External Research Architecture

### Opportunity Validation Router
- BO Hypothesis, Critical Assumptions, Evidence Questions를 입력으로 받음
- 필요한 데이터 원천/기간/단위/evidence type만 선택
- 모든 데이터셋을 무조건 조회하지 않음

### Data Source Role

#### ZeroIn
- 펀드/대표클래스/family 수준 흐름
- setup amount / NAV 및 기간 변화
- NAV 증감 ≠ 순유입
- 설정액 증감이 자금 유출입 해석에 더 직접적

#### FreeSIS
- 시장 전체 유형별 흐름
- 운용사별 흐름
- 고객유형별 판매
- 공사모/ETF/MMF 등 시장 aggregate 보완

#### News
- 시장 반응, 고객행동, 경쟁사/산업동향, 최신 외부 변화
- 가능한 한 `CONTENT_TEXT` 확보

#### Policy / Legal
- 발표/발의/입법예고/의결/공포/시행/검토 상태 구분
- 정책 시행 시점과 상태 충실도 확보

---

## 7. Company State / Gap / Strategy

Company Current State는 외부 Opportunity 검증 후 본다.

```text
Validated Opportunity
VS
Company Current State
→ Gap
→ Strategy Hypothesis
```

Company State로 BO를 역정의하지 않는다.

---

## 8. AIR Physical Implementation Principles

### 확인된 Runtime
- Agent → Agent context transfer: 가능
- Agent → Knowledge Base: 가능
- Agent → Tool: 가능
- Conditional routing: 가능
- Export → Import → Run: 현재 AIR 환경에서 가능

### 제약
- Agent 간 전달은 immutable typed object가 아니라 rich LLM context transfer에 가까움
- exact JSON preservation 보장 안 됨
- stage ownership은 prompt만으로 완전 보장 안 됨
- CURRENT_MRI KB page provenance는 현재 `Unknown`
- Conditional은 whole-output Contains 기반
- Tool/KB는 reference 형태이므로 cross-environment standalone portability 미검증

### 현재 구현 후보
직렬 `01 → 02 → 03`보다 Supervisor 중심 순차 orchestration을 우선 검증한다.
단, **v4 Supervisor-orchestrated runtime은 아직 미실행**이므로 PASS가 아니다.

---

## 9. 현재 개발상태

| 영역 | 상태 |
|---|---|
| Architecture | 큰 구조 확정 |
| Issue Extraction | Logical design 성숙 |
| Fidelity Validation | Logical design 성숙 |
| Screening | Logical design 성숙, directness calibration 계속 |
| 01~03 AIR Physical Orchestration | In Progress |
| BO Hypothesis | Next logical development target |
| Evidence Question | 미개발 |
| Validation Router | 미개발 |
| ZeroIn logical spec | 상당 부분 준비 |
| FreeSIS logical spec | 초기 |
| News / Policy logical spec | 초기 |
| Company State | 미개발 |
| Gap / Strategy | 미개발 |
| Final Routing / QC | 미개발 |
| Generalization | NOT VERIFIED |

---

## 10. r3 Development Principle

```text
1. 01~03 AIR orchestration 최소 안정화
2. BO Hypothesis 논리 / Schema / Regression
3. Evidence Question 논리
4. Opportunity Validation Router 논리
5. 실제 Evidence Question 기준 데이터 요구사항 확정
6. ZeroIn / FreeSIS / News / Policy 묶음 IT 요청
7. 데이터 수령 후 Research/Evidence AIR 구현
8. Company State
9. Gap / Strategy
10. Final Department Routing / Final Response / QC
```

**AIR 노드를 먼저 늘리지 않는다.**
Logical design과 regression이 안정된 뒤 가장 단순한 Physical implementation으로 옮긴다.
