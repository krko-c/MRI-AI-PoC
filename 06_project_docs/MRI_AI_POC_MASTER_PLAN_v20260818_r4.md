# MRI AI PoC Master Plan v20260818 r4

## 0. Purpose and Status

This document is the current logical design snapshot after the 2026-08-18 AIR Studio runtime experiments and subsequent architecture review.

r4 does **not** replace ADR-001. The Hypothesis-Driven External Research Architecture remains in force.

Key r4 changes:
1. Define the Fidelity Correction Contract.
2. Separate deterministic structural validation from semantic LLM validation.
3. Define workflow ownership of `analysis_as_of_date`.
4. Add BO hypothesis-count and evidence-question dedup rules.
5. Keep AIR v4 as an orchestration experiment only; r4 logical changes are to be implemented in v5.
6. Do not promote AIR v4 prompts to the Canonical Prompt Pack until runtime validation is complete.

## 1. Source of Truth

Conflict resolution order:

1. Accepted ADRs
2. Latest Master Plan / Development Roadmap
3. Canonical Prompt Pack
4. Regression Log / Regression Policy
5. IT Logical Spec
6. Runtime / AIR Mapping records
7. Archive
8. Conversation history

Important:
- AIR JSON may contain the newest **candidate implementation rules**, but it is not automatically canonical.
- Runtime candidate rules must be promoted to a new Canonical Prompt Pack only after validation.
- `GENERALIZATION VERIFIED` must not be used without unseen generalization evidence.

## 2. Project Objective

The PoC aims to transform a newly received MRI report into a traceable asset-management response process:

```text
MRI understanding
→ source fidelity
→ asset-management relevance screening
→ business opportunity hypotheses
→ targeted external validation
→ validated opportunity
→ company current state
→ gap
→ strategy
→ final department routing / request design
→ final response / QC
```

The logical process may contain many steps, but those steps are **not required to map 1:1 to AIR Agents**.

## 3. ADR-001 Architecture

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
Optional Strategy-specific Research
  ↓
Final Strategy
  ↓
Final Department Routing / Request Design
  ↓
Final Response
  ↓
QC
```

Core principles:
- External research validates BO hypotheses; it does not re-prove MRI issues by default.
- Company Current State must not define BO.
- Company State and Opportunity remain separated until Gap Analysis.
- `UNKNOWN != ABSENCE`.
- All external evidence processing must respect `analysis_as_of_date`.
- Historical replay cannot use information after the replay date.
- Provenance is preserved when the source interface exposes it.

## 4. Logical Step != Physical Agent

A logical step is a reasoning responsibility. A physical AIR Agent is an implementation choice.

Separate Agents are more justified when:
- data sources or permissions differ,
- early information leakage would bias later reasoning,
- independent semantic validation is required,
- parallel investigation is useful.

A single Agent with internal steps may be preferable when:
- the same source is read continuously,
- the work is mostly sequential reasoning,
- handoff itself causes stage-ownership drift,
- no independent intermediate artifact is required.

Therefore:
- Extraction / Fidelity / Screening remain separate logical responsibilities.
- BO / Evidence Question / Validation Router remain separate logical responsibilities.
- Final physical Agent count is decided after AIR runtime validation.

## 5. Workflow Input Contract

`analysis_as_of_date` is owned by Workflow Start.

```json
{
  "workflow_input": {
    "analysis_as_of_date": "2026-08-18",
    "run_mode": "CURRENT"
  }
}
```

Rules:

### CURRENT
If the user does not provide a date:
`analysis_as_of_date = workflow execution date`

### HISTORICAL_REPLAY
`analysis_as_of_date` is required.

All downstream Agents and Tools inherit the same value and must not mutate it.

## 6. Front Pipeline Contract

### 6.1 Stage 01 — Raw Issue Extraction

Purpose:
- extract all top-level MRI issues,
- preserve issue order and state/modality,
- avoid business/strategy inference.

Stage 01 output is **raw** and must remain preserved even if later correction is needed.

Runtime adapter rule when page metadata is unavailable:
- `page = null`
- `source_pages = []`
- do not fabricate page numbers.

### 6.2 Stage 02 — Fidelity Validation and Validated View

Stage 02:
1. evaluates whether Stage 01 is faithful to the MRI source,
2. when locally repairable, creates a **validated downstream view** without overwriting raw extraction.

Raw artifact:
`sections.issue_extraction`

Downstream artifact:
`sections.validated_issue_view`

Statuses:
`PASS | CORRECTABLE | FAIL`

#### PASS
No material meaning distortion.
Action: `validated_issue_view` may mirror raw extraction.

#### CORRECTABLE
Issue itself is valid, but one or more fields contain local semantic distortion.
Action:
- apply only the minimum necessary corrections into `validated_issue_view`,
- preserve `issue_extraction` unchanged.

#### FAIL
Stage 01 cannot be safely repaired with local correction.
Examples:
- missing top-level issue,
- merged unrelated issues,
- false split,
- invented issue,
- source boundary collapse.

Action:
- Screening is blocked,
- Stage 02 does not redo full extraction itself.

### 6.3 Fidelity Payload Pattern

```json
{
  "sections": {
    "issue_extraction": {"issues": []},
    "fidelity_validation": {
      "overall_status": "PASS | CORRECTABLE | FAIL",
      "issues": [
        {
          "topic_id": "S01",
          "validation_status": "PASS | CORRECTABLE | FAIL",
          "findings": [],
          "corrections": []
        }
      ]
    },
    "validated_issue_view": {"issues": []},
    "screening_result": null
  }
}
```

### 6.4 Stage 03 — Screening

Stage 03 screens **only `validated_issue_view`**.

Five lenses:
- product
- investment_theme
- customer
- channel
- group_collaboration

Each lens: `0 / 1 / 2`

Decision:
- any lens == 2 → OPPORTUNITY
- no 2, at least one 1 → MONITOR
- all 0 → EXCLUDE
- fidelity FAIL → VALIDATION_BLOCKED

No total score.

#### Score 2 Gate
A score of 2 requires:

```text
MRI-confirmed change
→ concrete asset-manager mechanism
→ practical asset-management use
```

If external validation is still required to establish investability, customer demand, liquidity, or product viability, the lens must not receive 2 solely from thematic attractiveness.

## 7. Validation Architecture

### 7.1 Deterministic Structural Gate

Structural conditions should not rely on the same LLM that generated the payload.

Examples:

Stage 01:
- issues array exists,
- topic_id exists,
- no duplicate topic_id,
- issue count matches actual array length,
- future-stage sections remain null.

Stage 02:
- status is PASS/CORRECTABLE/FAIL,
- CORRECTABLE has corrections,
- PASS/CORRECTABLE has `validated_issue_view`,
- FAIL leaves screening null.

Stage 03:
- exactly five lenses,
- score values are 0/1/2,
- no total-score field,
- classification matches deterministic rule,
- prohibited score/basis combinations are rejected.

These checks are implementation candidates for code/tool validation in AIR v5 or the orchestration layer.

### 7.2 Semantic Validation

LLM judgment remains necessary for:
- state/modality distortion,
- recommendation leakage,
- issue-boundary meaning,
- source entailment,
- asset-manager directness,
- whether Score 2 is semantically justified.

### 7.3 LLM Self-check

Self-check fields may remain as diagnostics, but they do not have final gate authority.

## 8. Retry and Stop Policy

### Stage 01 structural failure
```text
Stage 01
→ deterministic structural check FAIL
→ retry Stage 01 once
→ second FAIL = WORKFLOW_ERROR
```

### Stage 02 fidelity FAIL
```text
Stage 02 FAIL
→ retry Stage 01 once
→ rerun Stage 02
→ second FAIL = VALIDATION_BLOCKED
```

No unlimited retries.

`errors[]` is active.

## 9. BO Hypothesis Contract

Input:
- MRI issue from validated view,
- Screening Result,
- `analysis_as_of_date`.

Allowed:
- general asset-management mechanism knowledge.

Forbidden:
- company current state,
- internal product data,
- retrieved external evidence,
- unsupported named entities.

Each BO contains:
- opportunity_id
- hypothesis
- opportunity_scope
- asset_manager_role
- asset_manager_connection
- hypothesis_chain
- critical_assumptions
- evidence_questions
- validation_priority
- validation_status

Hypothesis chain:
`MRI_OBSERVATION → INFERRED_IMPLICATION → OPPORTUNITY_HYPOTHESIS`

### BO count control
Per issue:
- default: 1–3 BOs
- hard maximum: 4

Do not create separate BOs merely because `opportunity_scope` differs.
Separate BOs only when customer problem or economic mechanism is meaningfully different.

All newly generated BOs start as `UNVALIDATED`.

## 10. Evidence Question Deduplication

Before routing:

```text
Evidence Questions
→ Normalize
→ Deduplicate / Merge
→ Opportunity Validation Router
```

Questions from different BOs should be merged when they seek substantially the same evidence.

This is a logical function and is not yet fixed as a separate Agent.

## 11. IT Feasibility Track

A lightweight feasibility inquiry may run in parallel with BO / Router design.

Questions:
- Can ZeroIn support historical as-of lookup?
- Can setup amount changes be queried for requested windows?
- Can FreeSIS replay historical periods?
- Can AIR call ZeroIn / FreeSIS through an API, Tool, or batch interface?
- Can News provide full article text?
- Can Policy data provide full text plus status / effective date?

Detailed field specifications remain later work.

## 12. AIR Runtime Status

Confirmed in current AIR environment:
- Agent → Agent context transfer
- Agent → Knowledge Base
- Agent → Tool
- Conditional routing
- Export → Import → Run

Known limitations:
- Agent handoff is rich LLM context, not immutable typed-object transfer.
- page provenance is unavailable in current KB responses.
- conditional routing is whole-output Contains based.
- exported Tool / KB nodes are dependency references.
- cross-environment standalone portability is unverified.

### AIR v4

`MRI_01_02_03_v4_SUPERVISOR_ORCHESTRATED.json`

Status:
`GENERATED / RUNTIME TEST PENDING`

Its purpose is to validate **Supervisor-managed stage ownership**.

r4 logical changes are **not retrofitted into v4**.

If v4 orchestration passes, v5 will incorporate:
- validated_issue_view,
- PASS/CORRECTABLE/FAIL flow,
- deterministic structural checks where feasible,
- retry/stop logic,
- active errors[],
- analysis_as_of_date propagation.

### Fallback if Supervisor orchestration fails

```text
A. Supervisor-managed AIR orchestration
↓ fail
B. independent stage invocation with explicit payload handoff
↓ if needed
C. deterministic code orchestrator with stage-level validation
```

## 13. Canonical Prompt Pack Status

The existing Canonical Prompt Pack remains the last formal canonical baseline.

However:
- some AIR candidate rules are newer than the current Pack,
- those rules are **candidate rules pending runtime validation**,
- v4 prompt text must not be blindly promoted as canonical before validation,
- after runtime stabilization, create a new Canonical Prompt Pack version and update the pointer.

## 14. Current Status

| Area | Status |
|---|---|
| Architecture | Substantially defined |
| Front Logical Contract | r4 defined |
| AIR Front Orchestration | v4 runtime pending |
| Deterministic Structural Gate | Logical design defined; implementation pending |
| BO Hypothesis | In development |
| Evidence Question | In development |
| Validation Router | Not yet implemented |
| Dataset Request | Pending logical router/spec |
| IT Feasibility | Can begin in parallel |
| Company State | Not developed |
| Gap / Strategy | Not developed |
| Final Department Routing / QC | Not developed |
| Generalization | NOT VERIFIED |

## 15. Immediate Next

1. Run AIR v4 once for orchestration behavior.
2. Continue BO H02 regression and production prompt design.
3. Design Evidence Question normalization/dedup.
4. Design Validation Router.
5. In parallel, send lightweight IT feasibility questions.
6. After BO / Router logic stabilizes, produce detailed dataset specifications.
