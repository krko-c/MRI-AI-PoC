# MRI AI PoC Development Checkpoint — 2026-08-18

## Current Git baseline before this update

Latest known baseline:
`d22eac2` — `docs: update current project pointers to r4`

This checkpoint is a living current-status summary.

## New architecture clarification — ADR-002

Department Review is **not** the final purpose of the PoC and is **not** normally performed only after Strategy.

The owner / AI:
- independently screens and analyzes all relevant MRI issues,
- performs BO / external / internal / gap / strategy work,
- and synthesizes the final MRI response.

Relevant departments independently review screened issues in parallel and provide:
- current activities,
- actions they can take,
- opportunities / ideas,
- future plans.

Their responses are one internal evidence source.

## Updated workflow

```text
MRI
→ Extraction
→ Fidelity / Validated View
→ Screening
    ├→ Deep Analysis
    │   ├→ BO
    │   ├→ External Evidence
    │   └→ Validated Opportunity
    │
    └→ Department Review
        └→ Department Responses

Validated Opportunity
+
Internal Data / Documents
+
Department Responses
→ Company State / Evidence Integration
→ Gap
→ Strategy
→ Final MRI Response
```

## What changed from r4

Removed as normal architecture:
`Strategy → Final Department Routing → Department Request`

Replaced by:
`Screening → parallel Department Review`

Department response is not equivalent to Company Current State; it is one source within it.

## Existing r4 decisions remain

### Fidelity
- raw extraction preserved
- Stage 02 creates validated_issue_view
- PASS / CORRECTABLE / FAIL
- Screening uses validated view

### Validation
- deterministic structural gate where feasible
- semantic validation by LLM
- self-check diagnostic only
- one retry
- WORKFLOW_ERROR / VALIDATION_BLOCKED
- active errors[]

### analysis_as_of_date
- owned by Workflow Start
- CURRENT default execution date
- HISTORICAL_REPLAY explicit required date

### BO
- default 1–3 / max 4
- no duplication by scope alone
- evidence question normalize / dedup before Router

## AIR

v4:
`GENERATED / RUNTIME TEST PENDING`

Purpose remains:
- Supervisor-managed stage ownership test only.

Department Review lane does not need to be implemented before the v4 test.

## Current logical development target

```text
BO H03
→ BO Production Prompt v1
→ Evidence Question dedup
→ Validation Router
```

In parallel:
- Department Review request/response contract
- IT feasibility inquiry

## Current state

- ADR-001: ACCEPTED
- ADR-002: ACCEPTED
- Master Plan: r5
- Roadmap: r5
- AIR v4: runtime pending
- BO: in development
- Department Review: logical lane defined
- Company State / Gap / Strategy: not developed
- Generalization: NOT VERIFIED
