# MRI AI PoC Development Checkpoint

_Last updated: 2026-08-19_

## Current Direction

The project has changed from:

> refine each upstream component, freeze it, then connect later

to:

> define a provisional final output, run one issue end-to-end, then freeze the upstream contracts based on actual downstream use.

This is the main current development decision.

## Accepted Architecture Decisions

- ADR-001: Hypothesis-Driven External Research
- ADR-002: Department Review as a parallel internal evidence lane
- ADR-003: Parallel Research Lanes and Implementation Neutrality

See:
`06_project_docs/adr/README.md`

## Current Logical Architecture

```text
MRI
→ Extraction
→ Fidelity
→ Screening
   ├→ BO / Opportunity Research
   ├→ Market / Competitor Intelligence
   ├→ Company / Internal State Research
   └→ Department Review

Opportunity questions + Market-Intel questions
→ Shared Research Request Registry
→ Cross-lane Dedup
→ Router
→ Shared Evidence Pool

All results
→ Evidence / State Integration
→ Gap
→ Strategy
→ Complete MRI Response Draft
→ Human Review / Combination / Submission
```

## Newly Added Controls

### BO information barrier
Initial BO input physically excludes:
- Company State
- Department Responses
- internal product data
- other-lane market research output

Prompt-only prohibition is not enough.

### Shared research
Opportunity Validation and Market / Competitor Intelligence do not independently retrieve identical evidence by default.

Questions are normalized and deduplicated across lanes before Tool/source calls.

### Live-document policy
Normal edits now update:
- Master Plan live file
- Roadmap live file
- Checkpoint live file

Old r-files remain history.

## Front Pipeline

Status:
substantially developed.

Still required:
- AIR v4 one runtime test
- v5 based on observed result
- minimum regression

Not current primary development focus.

## BO

Current state:
- H01/H02/H03 design cases exist
- BO logic is promising
- BO Production Prompt is **not frozen yet**

Reason:
its schema must first prove useful in Thin End-to-End.

## Company State

Design direction:
- may run after Screening in parallel
- UNKNOWN != ABSENCE
- search coverage required
- department response is one source, not entire Company State

## Market / Competitor Intelligence

Now an explicit lane.

Distinct from Opportunity Validation, but shares an Evidence Pool where sources overlap.

## Final Output

Target:
complete MRI response draft.

A provisional structured contract now exists:

`06_project_docs/contracts/FINAL_MRI_RESPONSE_SCHEMA_v0.md`

This is the endpoint for the next Thin E2E.

## Immediate Next

H02 Thin End-to-End:

```text
Validated Issue
→ BO v0
→ Opportunity Validation
→ Market / Competitor
→ Company State
→ Integration
→ Gap
→ Strategy
→ Final MRI Response v0
```

Manual handoff is allowed.

After the result:
- remove unused fields
- add missing fields
- fix duplicated research
- then freeze v1 contracts.

## Physical Agent Count

NOT FIXED.

No fixed 4-Agent or 21-Agent architecture is accepted.

## Generalization

NOT VERIFIED.
