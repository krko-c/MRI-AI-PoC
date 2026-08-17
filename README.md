# MRI AI PoC

MRI 리포트의 주요 이슈를 구조화하고, 국내 자산운용사 관점에서 Screening한 뒤 외부 Evidence와 당사 Current State를 독립적으로 분석하여 Business Opportunity, Gap, Strategy 및 최종 대응안을 생성하는 멀티에이전트 AI PoC 프로젝트다.

## Source of Truth

문서 우선순위는 다음과 같다.

1. Current Canonical Prompt Pack
2. Master Plan
3. Regression Log
4. IT Logical Specification
5. Archive
6. Conversation History

Canonical 파일이 실제 기준본이며 대화 기록은 기준본을 대체하지 않는다.

## Current Status

- Current Canonical Pack: `v20260818`
- Current development stage: Policy / Legal Retrieval Planner `v1.2` Final Candidate
- Next development: `08_ZEROIN_RETRIEVAL_CANDIDATE_FINDER_v1.0`
- External Evidence Extractor `v1.0`: Draft, do not use yet
- AIR Runtime: Unvalidated / Deferred
- Generalization verified: No

## Architecture

Market / Opportunity Lane과 Company State Lane은 독립적으로 진행하며, Business Opportunity와 Integrated Current State는 Gap Analysis에서 처음 결합한다.

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

