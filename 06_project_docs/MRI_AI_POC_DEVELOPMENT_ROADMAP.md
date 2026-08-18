# MRI AI PoC Development Roadmap

_Last updated: 2026-08-19_

## 0. Current Development Mode

The project is now in **Thin End-to-End first** mode.

The immediate objective is not to perfect BO, Company State, or Router contracts independently.

The objective is to run one screened issue through the full analytical chain and use the result to decide what each upstream component actually needs to produce.

## Phase 0 — Live Documentation Structure

Status: STARTED

Maintain:
- `MRI_AI_POC_MASTER_PLAN.md`
- `MRI_AI_POC_DEVELOPMENT_ROADMAP.md`
- `MRI_AI_POC_DEVELOPMENT_CHECKPOINT.md`
- `adr/README.md`

Existing versioned r-files remain historical snapshots.

## Phase 1 — Final MRI Response Schema v0

Status: CREATED AS PROVISIONAL CONTRACT

Purpose:
define the end state of one issue before freezing upstream schemas.

The v0 schema is not a final submission template.  
It is the structured content contract for the AI's complete issue-level MRI response draft.

Required top-level content:
1. issue interpretation
2. market / competitor status
3. company current state
4. validated business opportunity
5. gap
6. response strategy
7. department input, if available
8. constraints / unknowns
9. evidence / provenance
10. overall confidence / verification state

Each substantive claim must be able to carry:
- source class
- evidence reference
- status

## Phase 2 — One-Issue Thin End-to-End

Status: NEXT

Use one already-screened issue.

Recommended first case:
H02 — pet-industry activation.

Why:
- requires investability reasoning,
- requires Market / Competitor Intelligence,
- requires Company State,
- exposes the risk of jumping directly from industry growth to ETF/product strategy.

Run manually if necessary:

```text
Validated Issue
→ BO v0
→ Opportunity Validation
→ Market / Competitor Intelligence
→ Company State
→ Evidence / State Integration
→ Gap
→ Strategy
→ Final MRI Response v0
```

Do not wait for final AIR topology.

## Phase 3 — End-to-End Reverse Review

After Phase 2, inspect:

### BO
- which BO fields were actually used?
- which assumptions mattered?
- which evidence questions mattered?
- which fields were redundant?
- what was missing?

### Company State
- what internal facts were necessary?
- what search coverage was needed?
- where did NOT_FOUND vs ABSENCE matter?

### Market / Competitor Intelligence
- which market / competitor facts entered the final response?
- what research was redundant with Opportunity Validation?
- what source hierarchy is needed?

### Evidence / Router
- which searches duplicated across lanes?
- what should be merged before retrieval?
- which Tool/source should answer each evidence type?

## Phase 4 — Contract v1 Freeze

Only after Phase 3.

Freeze:
- BO Production Prompt v1
- Company State Contract v1
- Market / Competitor Intelligence Contract v1
- Shared Research Registry / Router Contract v1
- Evidence Pool Contract v1
- Final MRI Response Contract v1

## Phase 5 — Regression

Run H01 / H02 / H03 using the v1 contracts.

### H01
Reverse-money-move:
- DIRECT market / product mechanism

### H02
Pet industry:
- CONDITIONAL investability
- no growth → ETF shortcut

### H03
Youth financial vulnerability:
- asset-manager role boundary
- PARTNER_DEPENDENT where appropriate

Only after this regression should BO Production Prompt v1 be treated as a meaningful production candidate.

## Parallel Track A — Company State Design

May start during Thin E2E.

Focus:
- source taxonomy
- retrieval coverage
- as-of
- historical response use
- product / fund data
- internal plans
- UNKNOWN vs ABSENCE
- department-response integration

## Parallel Track B — Market / Competitor Intelligence

May start during Thin E2E.

Focus:
- market status
- competitor actions
- financial-group actions
- product supply / launch
- policy / industry developments
- lookback window
- competitor universe
- source hierarchy

## Parallel Track C — Shared Research / Router

Opportunity and Market-Intel questions feed a common registry.

```text
Lane Questions
→ Shared Request Registry
→ Cross-lane Dedup
→ Router
→ Evidence Pool
→ lane-specific interpretation
```

## Parallel Track D — IT Feasibility

Ask capability questions now, not after all schema work.

Check:
- ZeroIn historical as-of support
- setup amount change windows
- FreeSIS historical replay
- AIR-callable interfaces
- News full text
- Policy full text + status/effective date
- internal product / document retrieval interfaces

This remains feasibility, not final field negotiation.

## AIR Front Track

At office:
1. run v4 once,
2. record execution signature,
3. decide Supervisor vs fallback,
4. create v5 only from observed result.

This track does not block Thin E2E.

## Physical Agent Architecture

Decide **after**:
- Thin E2E,
- front runtime evidence,
- source / permission analysis.

No fixed Agent count.

## Immediate Work Order

1. Final MRI Response Schema v0 — DONE in this package
2. Run H02 Thin End-to-End — NEXT
3. Reverse-review H02 output
4. Draft v1 contracts
5. H01 / H02 / H03 regression
6. office AIR v4 test in parallel
7. decide physical Agent topology
8. formal data specification / IT request
9. production implementation expansion
