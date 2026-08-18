# MRI AI PoC

MRI 리포트의 주요 이슈를 구조화하고, 국내 자산운용사 관점에서 Screening한 뒤 외부 Evidence와 당사 Current State를 독립적으로 분석하여 Business Opportunity, Gap, Strategy 및 최종 대응안을 생성하는 멀티에이전트 AI PoC 프로젝트다.

## Source of Truth

문서 우선순위는 다음과 같다.

1. Accepted Architecture Decisions
   - 전체 Architecture, Component 순서 및 역할 변경의 최우선 기준
2. Latest Master Plan / Development Roadmap
   - 현재 개발방향과 개발순서의 기준
3. Current Canonical Prompt Pack
   - 현재 Prompt baseline
   - 단, Accepted ADR에 의해 `ARCHITECTURE REVISION PENDING`으로 지정된 Component에서는 기존 Architecture/호출순서를 우선하지 않음
4. Regression Log
5. IT Logical Specification
6. Archive
7. Conversation History

Canonical Prompt Pack `v20260818`은 보존된 Prompt baseline이다.

ADR-001의 영향을 받는 04~08 Component의 Architecture, 역할 및 호출순서에 대해서는 Accepted ADR과 Latest Master Plan이 Canonical Pack의 기존 Architecture보다 우선한다.

대화 기록은 기준 문서를 대체하지 않는다.

## Current Status

- Current Canonical Pack: `v20260818`
- Canonical Prompt Pack `v20260818`: retained as stored baseline; newer AIR candidate rules are pending runtime validation
- Latest Master Plan: `MRI_AI_POC_MASTER_PLAN_v20260818_r4.md`
- Latest Development Roadmap: `MRI_AI_POC_DEVELOPMENT_ROADMAP_v20260818_r4.md`
- Current Development Checkpoint: `MRI_AI_POC_DEVELOPMENT_CHECKPOINT_20260818.md`
- ADR-001: `ACCEPTED`
- Architecture: Hypothesis-Driven External Research
- Front Logical Contract: `r4 defined`
- AIR v4 Supervisor orchestration: `GENERATED / RUNTIME TEST PENDING`
- Next logical development: Business Opportunity Hypothesis
- External Evidence components 04~07: `ARCHITECTURE REVISION PENDING`
- ZeroIn 08: developed/regression-tested logic exists, but its role is being repositioned primarily to `OPPORTUNITY_VALIDATION`
- IT feasibility check: `READY TO START IN PARALLEL`
- AIR Runtime: core compatibility gates passed in current environment; front-pipeline orchestration still in progress
- Generalization verified: No

## Architecture

ADR-001에 따라 External Research는 Issue-first broad research가 아니라 Hypothesis-driven targeted research로 수행한다. Screening 후 Company-blind Business Opportunity Hypothesis와 Evidence Question을 먼저 생성하고, 필요한 Source만 호출하여 Opportunity를 검증한다.

Company State와 Business Opportunity는 Gap Analysis 전까지 분리하며, Business Opportunity와 Integrated Current State는 Gap Analysis에서 처음 결합한다. MRI Issue 자체가 펀드·상품시장과 직접 대응되는 경우에만 Issue-level direct market evidence retrieval을 선택적으로 허용한다.

## Directory Guide

- `01_canonical/`: 현재 Canonical Prompt Pack과 버전 포인터
- `02_archive/`: 과거 Prompt 및 개발 이력. 실행 기준으로 사용하지 않음
- `03_regression/`: Regression Log와 테스트 케이스
- `04_it_spec/`: Logical Requirement 및 IT Feasibility Mapping
- `05_runtime/`: AIR Mapping 등 Runtime 구현 자료. 생성 결과물은 Git에서 제외
- `06_project_docs/`: Master Plan, Development Roadmap, Architecture Decisions

## Canonical and Archive Rules

- Archive는 참고자료이며 실행 기준으로 사용하지 않는다.
- Canonical과 Archive를 혼합하지 않는다.
- Canonical Prompt Pack은 기존 파일을 삭제하거나 덮어쓰지 않고 새 버전 파일을 추가한다.
- `CURRENT_VERSION.txt`만 현재 Pack을 가리키도록 갱신한다.
- Agent 버전과 Canonical Pack 버전은 별도로 관리한다.

## Protected Baseline Documents

다음 기준 문서는 초기 Git 이전 과정에서 내용과 줄바꿈을 변경하지 않는다.

- `01_canonical/MRI_AI_POC_CANONICAL_PROMPT_PACK_v20260818.md`
- `06_project_docs/MRI_AI_POC_MASTER_PLAN_v20260818.md`
- `06_project_docs/MRI_AI_POC_DEVELOPMENT_ROADMAP_v20260818.md`

## Git Workflow

- GitHub 원격 저장소는 회사 정책에 맞는 private 저장소를 사용한다.
- 작업 시작 전 `pull`, 작업 종료 전 변경 검토 후 `commit` 및 `push`한다.
- PC와 노트북은 각각 독립적인 clone을 사용한다.
- 회사 내부 PDF, MRI 원문, API key, `.env`, 자격증명 및 Runtime 결과물은 커밋하지 않는다.
