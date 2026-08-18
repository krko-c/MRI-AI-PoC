# MRI AI PoC Development Checkpoint — 2026-08-18

## 오늘 결정

### 유지
- ADR-001 Hypothesis-Driven External Research Architecture
- 전체 Logical Workflow
- BO 이후 External Evidence → Company State → Gap → Strategy 구조
- UNKNOWN != ABSENCE
- analysis_as_of_date / historical replay 원칙

### 수정
- Logical Step과 AIR Agent를 1:1로 보지 않음
- AIR Physical Topology는 runtime 검증 후 결정
- 요청부서는 앞단에서 후보만 가능, 최종 요청부서/요청내용은 Strategy 이후 결정
- AIR-first 개발을 줄이고 Logical Prompt/Schema/Regression을 먼저 안정화

### 채택하지 않음
- Fast Lane / Deep Lane으로 전체 아키텍처를 갈아엎는 안
- Agent를 2개 또는 4개로 미리 고정하는 안
- Marker string을 장기 stage contract로 사용하는 안

## Immediate Next
- AIR: `MRI_01_02_03_v4_SUPERVISOR_ORCHESTRATED.json` 1회 runtime test
- Logical: BO Hypothesis Input/Output/Assumption/Evidence Question/Traceability/Regression
- 이후 Evidence Question → Validation Router → Dataset Requirement → IT Request

## 데이터 요청 전 완료해야 할 것
1. BO가 어떤 질문을 만드는지
2. 그 질문이 ZeroIn / FreeSIS / News / Policy 중 어디로 가는지
3. 각 데이터 grain / field / as-of / replay / evidence ID
4. Tool input / output schema

## 현재 상태 문구
- Architecture: substantially defined
- Front Logical Design: substantially developed
- AIR Front Physical Orchestration: in progress
- v4 Supervisor orchestration: generated, runtime validation pending
- BO Hypothesis: next logical development target
- Dataset request: pending logical router specification
- Generalization: NOT VERIFIED
