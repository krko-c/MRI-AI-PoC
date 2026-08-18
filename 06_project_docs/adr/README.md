# Architecture Decision Record Index

This folder is the canonical index for accepted architecture decisions.

## ADR-001 — Hypothesis-Driven External Research

Status: `ACCEPTED`

Current source:
`../MRI_AI_POC_ARCHITECTURE_DECISIONS.md`

Core effect:
- Business Opportunity is generated before Company State is allowed to influence it.
- external research primarily validates BO hypotheses,
- direct issue-level market retrieval is an exception when MRI directly maps to fund/product market,
- Company State and Opportunity remain separated until Gap.

## ADR-002 — Department Review as a Parallel Internal Evidence Lane

Status: `ACCEPTED`

Expected file:
`ADR-002_DEPARTMENT_REVIEW_PARALLEL.md`

Core effect:
- Department Review starts after Screening,
- it proceeds in parallel with the analyst / AI research,
- department responses are one internal evidence source,
- Department Routing is not the final purpose of the workflow.

## ADR-003 — Parallel Research Lanes and Implementation Neutrality

Status: `ACCEPTED`

Expected file:
`ADR-003_PARALLEL_RESEARCH_IMPLEMENTATION_NEUTRALITY.md`

Core effect:
- Company State and Market / Competitor research may start in parallel,
- BO initial generation remains information-isolated,
- logical steps do not imply physical Agent count,
- final target remains a complete MRI response draft.

## Maintenance Rule

When a new ADR is accepted:
1. add it to this index,
2. update the live Master Plan and Roadmap if it changes current architecture,
3. do not create a new Master/Roadmap r-file solely for that edit,
4. use Git history for normal change tracking.
