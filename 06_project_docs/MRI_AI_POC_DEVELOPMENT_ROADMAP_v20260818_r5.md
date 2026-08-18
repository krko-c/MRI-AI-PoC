# MRI AI PoC Development Roadmap v20260818 r5

## 0. r5 Change

ADR-002 changes the placement of department review.

Old interpretation:
```text
Strategy
→ Final Department Routing
→ Department Request
→ Final Response
```

New accepted interpretation:
```text
Screening
├→ Deep Analysis
└→ Department Review
      ↓
   Department Responses
      ↓
Internal / Company Evidence Integration
      ↓
Gap
→ Strategy
→ Final MRI Response
```

The owner / AI performs the full analysis independently; department responses are one parallel internal evidence source.

## Phase A — Front Pipeline Runtime Closure

Logical:
```text
Raw Extraction
→ Fidelity
→ Validated Issue View
→ Screening
```

AIR v4:
- orchestration experiment only,
- runtime pending.

AIR v5 target:
- validated_issue_view
- PASS/CORRECTABLE/FAIL
- deterministic structural checks
- one retry
- VALIDATION_BLOCKED / WORKFLOW_ERROR
- errors[]
- analysis_as_of_date

Department Review does not block this Phase.

## Phase B — BO Hypothesis

Input:
- validated issue
- Screening Result
- analysis_as_of_date

Output:
- default 1–3, max 4 BOs,
- no duplication by scope alone,
- critical assumptions,
- evidence questions,
- validation priority,
- UNVALIDATED status.

Regression priorities:
- direct finance-market case,
- conditional industry-theme case,
- partner-dependent / adjacent customer case.

## Phase C — Evidence Questions / Router

```text
Questions
→ Normalize
→ Deduplicate
→ Router
```

Route only needed evidence.

## Phase D — Department Review Logical Design

This Phase can be designed in parallel with C.

Define:
- department relevance rule,
- request schema,
- response schema,
- provenance / source tagging,
- pending / received / not-required statuses,
- handling of conflicting department responses,
- handling of no response.

Candidate request fields:
- issue_id
- relevant_departments
- review_reason
- requested_current_state
- requested_actions_or_opportunities
- requested_future_plan
- specific_questions

Important:
- Department Review is an independent issue review.
- It is not a post-strategy confirmation step.
- It may start immediately after Screening.

## Parallel Track — IT Feasibility

Ask capability-only questions before final field specs.

- ZeroIn historical as-of?
- period setup changes?
- FreeSIS historical replay?
- AIR-callable interface?
- News full text?
- Policy full text + status/effective date?

## Phase E — Dataset Logical Specification

Define for each source:
- purpose
- grain
- fields
- as-of
- replay
- filters
- evidence ID
- UNKNOWN handling
- Tool input/output

## Phase F — Formal IT Request

Submit detailed, coherent request after BO/Router/data-spec stabilize.

## Phase G — External Research / Evidence Integration

Execute BO evidence questions and update validation status.

## Phase H — Internal / Company State

Integrate multiple internal sources:
- internal product/fund data
- internal plans/docs
- historical MRI responses
- department responses
- other approved internal evidence

Department response is one source.

## Phase I — Gap / Strategy

```text
Validated BO
+
Internal / Company State
+
Department Evidence
→ Gap
→ Strategy
```

## Phase J — Final MRI Response / QC

Final output combines:
- source facts
- external evidence
- internal facts
- department facts
- department proposals
- AI inference / recommendation

QC preserves provenance and category boundaries.

## Immediate Sequence

### Logical development
1. Continue BO H03.
2. Freeze BO Production Prompt v1.
3. Design Evidence Question dedup + Router.
4. Draft Department Review request/response contract.
5. Prepare IT feasibility inquiry.

### Office / AIR
6. Run v4 orchestration test.
7. Build v5 after result.

### Then
8. Dataset specification.
9. Formal IT request.
10. Evidence / Company State / Gap / Strategy integration.
