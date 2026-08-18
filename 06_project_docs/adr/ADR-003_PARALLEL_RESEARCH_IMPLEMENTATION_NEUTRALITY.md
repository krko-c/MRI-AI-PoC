# ADR-003 — Parallel Research Lanes and Implementation Neutrality

- Date: 2026-08-19
- Status: ACCEPTED

## Decision

After Screening, research may proceed in parallel across:
- BO / Opportunity Research,
- Market / Competitor Intelligence,
- Company / Internal State Research,
- Department Review.

Parallel execution does not imply shared context.

Initial BO generation physically excludes:
- Company State,
- Department Responses,
- internal product data,
- other-lane market-research results.

Logical steps remain explicit, but physical Agent count is not fixed in advance.

The final target remains a complete MRI response draft for human review, combination, and submission.

Market / Competitor Intelligence is an explicit research purpose, not merely a by-product of BO validation.

Opportunity and Market-Intel questions should use a shared research-request registry and cross-lane deduplication before retrieval where they rely on overlapping sources.
