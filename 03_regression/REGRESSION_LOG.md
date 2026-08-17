# MRI AI PoC — REGRESSION LOG

## 01 MRI Issue Extraction

- H01: Mixed-state aggregation 문제
- H02: 목표/예정/완료/검토 상태 왜곡 반복
- Patch: Mixed-State Aggregation
  - 목표 ≠ 예정
  - 검토 ≠ 추진
  - 계획 ≠ 시행 예정
  - 구축 완료 ≠ 서비스 출시
  - 부지 확보 ≠ 착공
- Current Status: FINAL CANDIDATE

## 02 Source / Fidelity Validator

- H01에서 mixed-state distortion 미탐지
- `MIXED_STATE_DISTORTION` 검증 추가
- Current Status: FINAL CANDIDATE

## 03 MRI Screening

- Source Entailment patch
- General AM knowledge는 connection mechanism 설명에만 사용
- Score 2는 추가 factual assumption 없이 direct/almost direct일 때만 사용
- 총점 사용하지 않음
- Deterministic rule:
  - max 2 → OPPORTUNITY
  - max 1 → MONITOR
  - all 0 → EXCLUDE
- Current Status: PRODUCTION CANDIDATE — REGRESSION PASSED WITH DIRECTNESS CALIBRATION WARNING
- Residual: 일부 Regression에서 Score 2 directness가 다소 공격적인 경향이 남아 있음
- 동일 20-case Regression을 반복 실행하며 Prompt를 추가 Patch하지 않음

## 04 Financial / AM News Search Planner

- Tokenized: Query 과다
- Corporate Cash: RP/신탁/핀테크 solution leakage
- ESS: PF/사모펀드/대체투자/인프라펀드 leakage
- v1.1에서 discovery-oriented query로 수정
- Default 5~6, max 8
- Current Status: FINAL CANDIDATE

## 05 External Evidence Source Router

- v1.0: purpose leakage, structured-source overclaim
- v1.1: PURPOSE FIDELITY, STRUCTURED SOURCE FIDELITY
- ESS spot check PASS
- Senior spot check PASS
- Current Status: FINAL CANDIDATE

## 06 Policy / Legal Retrieval Planner

- v1.0: agency over-inference, policy concept broadening
- v1.1: concept/agency 개선, specific law names leaked via search_concepts
- v1.2: NO LEGAL TARGET LEAKAGE
- PL-V12-01 PASS
- Current Status: FINAL CANDIDATE

## 07 External Evidence Extractor

- VERSION: v1.0
- STATUS: DRAFT / DEFERRED
- 아직 Regression 수행 금지
- 선행 완료 필요:
  - ZeroIn Retrieval / Candidate Finder
  - FreeSIS Retrieval Planner
  - Unified Retrieval Contract
- 위 Retrieval Layer 완료 후 Draft 재검토 → Regression → Final Candidate 승격 여부 판단

## Generalization Policy

- 26-2 / 26-3 / 26-4: Development + Regression Set
- H01 / H02는 Prompt 개선에 사용되었으므로 Unseen Holdout으로 재사용하지 않는다.
- Synthetic Holdout은 Controlled Holdout이며 Genuine Generalization Test로 간주하지 않는다.
- 최종 Generalization Test는 개발에 사용하지 않은 새로운 MRI로 수행한다.

## 08 ZeroIn Retrieval / Candidate Finder

### Data Design Confirmed

- representative class name available
- family setup amount available
- family NAV available
- family setup / NAV change available for 1M / 3M / 6M / YTD
- master funds will be excluded upstream
- ETF has no class duplication issue

### ZR-01

Result:
PASS WITH MINOR CALIBRATION

Issue:
Unsupported issue-specific geography introduced once.

Action:
MRI ISSUE FIDELITY rule added.

### ZR-02

Result:
FAIL

Issue:
Demographic MRI issue was transformed into inferred needs and products: retirement income / income / TDF / dividend.

Impact:
Confirmed relevant market was over-expanded.

Action:
ISSUE CONCEPT BOUNDARY added.

### ZR-03

Result:
PASS WITH MINOR EXECUTION WARNING

Core relevance:
PASS

Confirmed aggregation:
PASS

Issue:
MMF was generated as a BROAD concept despite the existing concept-boundary rule.

Impact:
No confirmed-market contamination. MMF remained POSSIBLY_RELEVANT.

Action:
Do not add an MMF-specific Prompt patch. Use structured concept provenance / validation gate in future revision.

### Architecture Finding

Regression demonstrated that ZeroIn has limited value as a mandatory Issue-level retrieval source.

Primary role changed to:

OPPORTUNITY_VALIDATION market evidence retrieval.

This finding led to ADR-001: Hypothesis-Driven External Research Architecture.
