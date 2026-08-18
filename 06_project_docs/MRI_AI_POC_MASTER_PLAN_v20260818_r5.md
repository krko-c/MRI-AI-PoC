# MRI AI PoC Master Plan v20260818 r5

## 0. Purpose and Status

r5 incorporates ADR-002: **Department Review is a parallel internal evidence lane, not a late-stage Final Department Routing step.**

The core ADR-001 Hypothesis-Driven External Research architecture remains in force.

The PoC objective is to help the product-strategy owner independently analyze MRI issues end-to-end while also collecting relevant departments' independent reviews, then combine all evidence into a final MRI current-status / strategy response.

## 1. Source of Truth

1. Accepted ADRs
2. Latest Master Plan / Development Roadmap
3. Canonical Prompt Pack
4. Regression Log / Regression Policy
5. IT Logical Spec
6. Runtime / AIR Mapping records
7. Archive
8. Conversation history

AIR runtime candidate rules are not automatically canonical.

## 2. Project Objective

The system is not primarily a department-routing tool.

It supports the full analyst process:

```text
MRI understanding
→ source fidelity
→ asset-management relevance screening
→ business-opportunity hypotheses
→ targeted external validation
→ validated opportunity
→ internal / company evidence
→ gap
→ strategy
→ final MRI response
```

At the same time, relevant departments independently review screened issues and return:
- what they are doing now,
- what they could do,
- what opportunities / actions they see,
- what they plan to do.

Those responses are one input to the final analysis.

## 3. Current Logical Workflow

```text
CURRENT MRI
  ↓
Issue Extraction
  ↓
Source / Fidelity Validation
  ↓
Validated Issue View
  ↓
MRI Screening
  │
  ├───────────────────────────────┐
  │                               │
  ↓                               ↓
Business Opportunity          Department Review
Hypothesis                    Request / Response
  ↓                               ↓
Evidence Questions            Department Evidence
  ↓                               │
Validation Router                 │
  ↓                               │
External Research                 │
  ↓                               │
Evidence Integration              │
  ↓                               │
Validated Business Opportunity    │
  │                               │
  └──────────────┬────────────────┘
                 ↓
        Internal / Company State
        ├─ product / fund data
        ├─ historical responses
        ├─ business / marketing plans
        ├─ department responses
        └─ other approved internal evidence
                 ↓
             Gap Analysis
                 ↓
              Strategy
                 ↓
        Final MRI Response / QC
```

Important:
- Department Review may start immediately after Screening.
- It does not wait for Strategy.
- Department response is not the sole source of Company State.
- The owner / AI still performs independent analysis across all relevant issues.

## 4. Logical Step != Physical Agent

Logical responsibilities are maintained independently from AIR Agent count.

Separate physical Agents are justified mainly when:
- data / permissions differ,
- information leakage can bias reasoning,
- independent judgment is useful,
- parallel execution is valuable.

Department Review is a logical parallel lane. It is **not yet fixed as a dedicated AIR Agent**.

## 5. Workflow Input Contract

`analysis_as_of_date` owner: Workflow Start.

- CURRENT: execution date if not explicitly provided.
- HISTORICAL_REPLAY: explicit date required.
- downstream inherits without mutation.

## 6. Front Pipeline Contract

### 6.1 Stage 01 Raw Extraction
Preserve raw source-derived issues.

### 6.2 Stage 02 Fidelity
Output:
`PASS | CORRECTABLE | FAIL`

Raw extraction remains untouched.

Stage 02 creates:
`validated_issue_view`

- PASS: validated view may mirror raw.
- CORRECTABLE: minimum local corrections applied to validated view.
- FAIL: Screening blocked; Stage 02 does not redo the full extraction.

### 6.3 Stage 03 Screening

Screen only `validated_issue_view`.

Five lenses:
- product
- investment_theme
- customer
- channel
- group_collaboration

Decision:
- any 2 → OPPORTUNITY
- no 2, any 1 → MONITOR
- all 0 → EXCLUDE
- Fidelity FAIL → VALIDATION_BLOCKED

No total score.

Score 2 requires:

```text
MRI-confirmed change
→ concrete asset-manager mechanism
→ practical asset-management use
```

## 7. Validation Architecture

Structural validation should be deterministic where feasible.

Examples:
- required arrays / fields,
- duplicate topic_id,
- five-lens count,
- score domain,
- no total score,
- deterministic classification consistency,
- stage ownership fields.

Semantic LLM validation remains for:
- state / modality distortion,
- recommendation leakage,
- issue-boundary meaning,
- asset-manager directness.

LLM self-check is diagnostic only.

Retry:
- Stage 01 structural fail: retry once → second fail = WORKFLOW_ERROR.
- Fidelity fail: retry Stage 01 once → rerun Fidelity → second fail = VALIDATION_BLOCKED.

## 8. Business Opportunity Contract

Input:
- validated MRI issue,
- Screening Result,
- analysis_as_of_date.

Forbidden:
- company current state,
- internal product data,
- retrieved external evidence,
- unsupported named entities.

Per issue:
- default 1–3 BOs,
- hard max 4,
- different scope alone does not justify a separate BO.

Each BO includes:
- opportunity_id
- hypothesis
- opportunity_scope
- asset_manager_role
- hypothesis_distance
- asset_manager_connection
- hypothesis_chain
- critical_assumptions
- evidence_questions
- validation_priority
- validation_status = UNVALIDATED

Hypothesis chain:
`MRI_OBSERVATION → INFERRED_IMPLICATION → OPPORTUNITY_HYPOTHESIS`

## 9. Evidence Question Deduplication

Before routing:

```text
Generate
→ Normalize
→ Deduplicate / Merge
→ Validation Router
```

This is a logical function, not yet a fixed Agent.

## 10. Department Review Lane

### 10.1 Trigger

After Screening, the workflow may identify relevant departments.

This is not a final strategy decision. It is a request for an **independent department review**.

### 10.2 Requested content

Candidate request fields:

```text
issue_id
relevant_departments
review_reason
requested_current_state
requested_actions_or_opportunities
requested_future_plan
specific_questions
```

Typical intent:

> "From your department's perspective, review this issue and tell us what you currently do, what you could do, and what plans / ideas you have."

### 10.3 Department response as evidence

Department responses may contain:
- current facts,
- plans,
- ideas,
- constraints,
- feasibility judgments.

These must be tagged distinctly from AI-generated inference.

### 10.4 Timing

Department Review and Deep Analysis proceed in parallel.

Do not serialize:

```text
Strategy
→ Department Request
```

as the normal design.

## 11. Internal / Company State

Company State is built from multiple internal evidence sources.

```text
Internal / Company State
= internal data
+ internal documents
+ historical response
+ department response
+ other approved evidence
```

Department response is one source, not the whole state.

Company State must not flow backward into BO generation.

## 12. Gap and Strategy

```text
Validated Opportunity
+
Internal / Company State
+
Department Evidence
→ Gap
→ Strategy
```

Department ideas may inform Strategy, but do not automatically become Strategy.

## 13. Final MRI Response

Final output is the integrated MRI response, not merely a list of questions sent to departments.

The final response should be able to distinguish:
- MRI source facts,
- external evidence,
- internal system facts,
- department-provided facts,
- department proposals,
- AI inference / recommendation.

## 14. IT Feasibility Track

A lightweight feasibility inquiry may proceed in parallel:
- ZeroIn historical as-of?
- period setup changes?
- FreeSIS historical replay?
- AIR-callable API / Tool / batch?
- News full text?
- Policy full text + status / effective date?

## 15. AIR Runtime Status

AIR v4 remains:
`GENERATED / RUNTIME TEST PENDING`

v4 purpose:
- validate Supervisor-managed stage ownership only.

r4/r5 logical changes are not retrofitted into v4.

If v4 orchestration passes, v5 should incorporate:
- validated_issue_view,
- PASS/CORRECTABLE/FAIL,
- deterministic gates where feasible,
- retry / stop,
- errors[],
- analysis_as_of_date.

Department Review lane AIR implementation will be decided later and does not block v4.

## 16. Canonical Prompt Status

Current Canonical Pack remains the stored baseline.

New logical rules remain candidate rules until runtime / regression stabilization.

## 17. Current Status

| Area | Status |
|---|---|
| ADR-001 | ACCEPTED |
| ADR-002 | ACCEPTED |
| Front Logical Contract | r5 defined |
| AIR Front Orchestration | v4 runtime pending |
| BO Hypothesis | in development |
| Department Review | logical lane defined; AIR implementation pending |
| Evidence Question / Router | in development |
| IT feasibility | can begin in parallel |
| Company State | not developed |
| Gap / Strategy | not developed |
| Final MRI Response | not developed |
| Generalization | NOT VERIFIED |

## 18. Immediate Next

1. Continue BO H03 regression / Production Prompt.
2. Design Evidence Question dedup + Router.
3. Prepare lightweight IT feasibility questions.
4. At office, run AIR v4 once for orchestration.
5. Build v5 only after v4 result.
6. Later design Department Review request/response schema and integration contract.
