# ADR-002 — Department Review as a Parallel Internal Evidence Lane

- Date: 2026-08-18
- Status: ACCEPTED
- Scope: MRI AI PoC logical workflow
- Supersedes: the prior placement of `Final Department Routing / Request Design` as a late-stage step after Strategy

## 1. Context

The PoC supports a real operating process in which the product-strategy owner does not simply route MRI issues to departments and wait for answers.

The owner:
1. screens the MRI,
2. performs independent analysis of each relevant issue,
3. investigates external market / policy / product evidence,
4. develops business-opportunity hypotheses,
5. reviews company current state,
6. identifies gaps and strategies,
7. and combines these analyses into the final MRI response.

In parallel, relevant departments are asked to review the same screened issue from their own operational perspective and provide:
- current activities,
- actions they can take,
- ideas / opportunities they see,
- future plans,
- and other issue-specific comments.

Department responses are therefore **one internal evidence input among several**, not the final purpose of the workflow and not merely a confirmation request after Strategy is already complete.

## 2. Decision

After MRI Screening, create a parallel `Department Review` lane.

```text
MRI
→ Extraction
→ Fidelity / Validated Issue View
→ Screening
        │
        ├──────────────────────────────────────────────┐
        │                                              │
        ↓                                              ↓
Business Opportunity / External Analysis        Department Review
        ↓                                              ↓
Validated Opportunity                         Department Responses
        │                                              │
        ├───────────────┐               ┌──────────────┘
        │               │               │
        ↓               ↓               ↓
Internal Data / Company State ← Department Responses
        ↓
Evidence Integration
        ↓
Gap Analysis
        ↓
Strategy
        ↓
Final MRI Response
```

Department Review may start as soon as Screening has identified that an issue is relevant enough to request review.

It does **not** need to wait for:
- external validation,
- Company State completion,
- Gap Analysis,
- Strategy completion.

This allows the department review process and the analyst / AI deep-analysis process to proceed in parallel.

## 3. Department Review Role

Department Review is an independent internal perspective.

Its purpose is not:

> "AI has already decided the strategy; please confirm missing facts."

Its purpose is closer to:

> "Review this MRI issue from your department's perspective. What are you doing now, what could you do, and what are your plans or ideas?"

Therefore department responses may contribute:
- factual Company Current State,
- planned initiatives,
- implementation constraints,
- new business ideas,
- operational feasibility,
- department-specific judgment.

The final system must preserve the distinction between:
- system-retrieved internal facts,
- department-provided facts,
- department proposals / opinions,
- AI-generated inference.

## 4. Department Review Output Contract

Candidate logical fields:

```text
issue_id
relevant_departments[]
review_reason
requested_current_state[]
requested_actions_or_opportunities[]
requested_future_plan[]
specific_questions[]
response_status
department_responses[]
```

The exact schema remains subject to later implementation design.

## 5. Relationship to Company Current State

Department responses are **not equivalent to Company Current State as a whole**.

Company / internal evidence may include:

```text
1. internal product / fund data
2. historical MRI responses
3. internal business / marketing plans
4. department responses
5. other approved internal records
```

Department responses are one evidence source within this broader internal evidence set.

## 6. Relationship to Strategy

Strategy is produced after integrating:
- validated external opportunity evidence,
- internal / company evidence,
- department responses where available,
- identified gaps.

A department response can affect the strategy, but the final strategy is not simply a copy or aggregation of department responses.

## 7. Operational Timing

Normal path:

```text
Screening
→ Department Review Request can start immediately
→ Deep analysis proceeds in parallel
→ Responses are integrated when available
```

If a department response is delayed, the deep-analysis lane may continue.

The workflow should distinguish:
- `DEPARTMENT_RESPONSE_PENDING`
- `DEPARTMENT_RESPONSE_RECEIVED`
- `DEPARTMENT_RESPONSE_NOT_REQUIRED`

Finalization policy for incomplete responses will be defined later.

## 8. Consequences

### Positive
- reflects the actual working process,
- reduces unnecessary serial waiting,
- treats departments as independent contributors rather than post-hoc confirmers,
- improves final strategy by combining AI analysis with operational knowledge,
- avoids over-reading `Department Routing` as the main purpose of the PoC.

### Trade-offs
- workflow becomes explicitly parallel,
- department response provenance must be tracked,
- Company State must merge multiple internal evidence types,
- final response needs to distinguish system analysis from department opinion.

## 9. What does not change

ADR-001 remains valid:
- BO remains company-blind until external opportunity validation,
- Company State does not define BO,
- external research validates opportunity hypotheses,
- `UNKNOWN != ABSENCE`,
- `analysis_as_of_date` rules remain.

Department Review is a parallel internal evidence lane; it does not move internal company information into BO generation.
