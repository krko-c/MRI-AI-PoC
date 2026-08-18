# MRI AI PoC Development Roadmap v20260818 r4

## 0. Purpose

r4 updates the development sequence after AIR runtime experiments and the architecture review.

Overall ADR-001 architecture is unchanged.

## Phase A — Front Pipeline Runtime Closure

### A1. Logical contract
```text
Raw Extraction
→ Fidelity
   ├ PASS
   ├ CORRECTABLE → Validated Issue View
   └ FAIL → Block / retry
→ Screening on Validated Issue View
```

### A2. AIR v4
Purpose:
- test Supervisor-managed stage ownership only.

Status:
`runtime pending`

Do not retrofit r4 logic into v4 before this test.

### A3. AIR v5
Create only after v4 orchestration result is known.

v5 target:
- `validated_issue_view`
- PASS/CORRECTABLE/FAIL
- Screening only from validated view
- deterministic structural checks where AIR supports them
- one retry
- VALIDATION_BLOCKED
- WORKFLOW_ERROR
- errors[]
- analysis_as_of_date

### Phase A exit criteria
- stage ownership preserved
- raw extraction preserved
- validated view exists for PASS/CORRECTABLE
- FAIL blocks Screening
- 5-lens Screening works on validated view
- structural-invalid payload does not silently continue

## Phase B — BO Hypothesis Logical Development

Input:
- validated MRI issue
- Screening Result
- `analysis_as_of_date`

Output:
- 1–3 BOs by default
- max 4
- different scope alone is not enough to create a separate BO
- each BO has critical assumptions and evidence questions
- all BOs start UNVALIDATED

Traceability:
`BO_ID → ASSUMPTION_ID → EVIDENCE_QUESTION_ID`

Exit:
- fact vs inference separation
- no company-state leakage
- no external fact laundering
- no unsupported named entities
- no simple growth-industry → ETF jump
- no unnecessary BO duplication
- validation priority assigned

## Phase C — Evidence Question Normalization and Router

### C1. Generate questions
Convert critical assumptions into explicit evidence questions.

### C2. Dedup / merge
Normalize materially equivalent questions before routing.

### C3. Validation Router
Route only necessary questions to:
- ZeroIn
- FreeSIS
- News
- Policy / Legal
- other approved sources later

Exit:
- no automatic all-source retrieval
- duplicate evidence requests reduced
- timeframe / grain / filter explicit
- UNKNOWN != ABSENCE

## Parallel Track — IT Feasibility

Begin before detailed dataset request.

Initial questions:
- historical as-of in ZeroIn?
- setup-amount changes by requested periods?
- historical replay in FreeSIS?
- AIR-callable interface: API / Tool / batch?
- full article text for News?
- full legal/policy text plus status/effective date?

## Phase D — Dataset Logical Specification

For each dataset:
- purpose
- logical consumer
- query intent
- grain
- required fields
- optional fields
- as-of support
- historical replay
- filters
- evidence ID
- UNKNOWN handling
- Tool input
- Tool output

## Phase E — Formal IT Request

Submit one coherent request after BO / Router / data-spec work is stable.

Include:
- purpose
- fields
- grain
- time basis
- sample query
- expected output
- AIR/API/Tool interface expectation

## Phase F — External Research / Evidence Integration

After data access:
- execute evidence questions
- normalize evidence
- detect contradiction
- integrate evidence
- update BO validation status

Potential taxonomy:
- SUPPORTED
- PARTIALLY_SUPPORTED
- NOT_SUPPORTED
- INSUFFICIENT_EVIDENCE

## Phase G — Company Current State

Only after external BO validation.

Do not allow Company State to redefine BO.

## Phase H — Gap / Strategy

```text
Validated Opportunity
VS
Company Current State
→ Gap
→ Strategy Hypothesis
```

## Phase I — Final Department Routing / Response / QC

Final routing determines:
- whether request is required
- department
- reason
- current-state request
- plan request
- exact questions/material

QC:
- source/inference/evidence distinction
- as-of date
- replay integrity
- provenance
- unsupported named entities
- state/modality
- company-state leakage
- recommendation overreach

## Immediate Sequence

### Office / AIR
1. Run v4 once for orchestration.
2. Decide fallback only if needed.
3. Build v5 after result.

### Logical development
4. Continue BO H02.
5. Freeze BO production prompt v1.
6. Design evidence-question normalization/dedup.
7. Design router.

### In parallel
8. Send IT feasibility inquiry.

### Then
9. Freeze dataset specs.
10. Send formal IT request.
