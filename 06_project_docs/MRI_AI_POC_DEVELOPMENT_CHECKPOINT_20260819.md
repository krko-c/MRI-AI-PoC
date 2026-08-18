# MRI AI PoC Development Checkpoint — 2026-08-19

## Current Git baseline

Latest known baseline before this update:
`d22eac2` plus the pending r5 local update package if not yet committed.

This checkpoint is a living current-status summary.

## New accepted direction

### ADR-003 — Parallel Research Lanes and Implementation Neutrality

The project will not adopt the external evaluator's simplified conclusion that the system should be exactly four Agents.

The useful part of that review is accepted:

- development has spent enough time on the front pipeline,
- Company State Research must move forward now,
- Market / Competitor Intelligence must become explicit,
- downstream research should be prototyped end-to-end,
- logical steps should not be automatically mapped to separate physical Agents.

The overcorrections are rejected:

- no fixed 4-Agent architecture,
- no automatic BO/EQ/Router/Research/Integration collapse,
- no deletion of Fidelity as a logical function,
- no reduction of final output to an Issue Brief,
- no assumption that human review makes QC/provenance unnecessary.

## Final target clarified

The AI still produces its own complete MRI analysis / response draft.

Department review is parallel and independent.

The user combines:
- AI analysis,
- department responses,
- other internal inputs

into the final submission.

"Human synthesis" is not a separate large automation target; it is simply the user's final review and combination step.

## Updated execution architecture

```text
MRI
→ Extraction
→ Fidelity
→ Screening
   ├→ BO / Opportunity Research
   ├→ Market / Competitor Intelligence
   ├→ Company / Internal State Research
   └→ Department Review

→ Evidence / State Integration
→ Gap
→ Strategy
→ Final MRI Response Draft
→ Human Review / Submission
```

## Information barrier

BO generation remains company-blind.

Company State and Department Responses may be collected in parallel, but must not be used to generate the initial BO hypothesis.

## Current priority shift

Front pipeline:
- sufficient to proceed,
- v4 one runtime test still required,
- v5 after observed result,
- no more disproportionate stage-ownership work before downstream prototype.

Priority unfinished work:

```text
1. BO Production
2. Company State Research
3. Market / Competitor Intelligence
4. Evidence Question / Router
5. IT feasibility
6. Evidence Integration
7. Gap / Strategy
8. Final MRI Response
```

## BO status

H02 lesson retained:
- do not jump industry growth → ETF,
- investable universe / liquidity / investor demand remain critical assumptions,
- BO duplication by implementation form is prohibited.

Next:
H03 role-boundary regression.

## Market / Competitor Intelligence

New explicit purpose.

External research must support both:
- OPPORTUNITY_VALIDATION
- MARKET_COMPETITOR_INTELLIGENCE

They may use overlapping sources but are not the same analytical objective.

## Company State

May begin after Screening in parallel.

Sources may include:
- product / fund data,
- historical MRI responses,
- internal plans / documents,
- approved internal data,
- department responses when available.

UNKNOWN != ABSENCE.

## Physical Agent policy

`Logical Step != Physical Agent`

No fixed physical Agent count.

Agent boundaries will be decided only after:
- front runtime evidence,
- one-issue end-to-end prototype,
- source / permission / orchestration requirements are clear.

## Immediate next

```text
H03 BO regression
→ BO Production Prompt v1

in parallel:
Company State contract
Market / Competitor Intelligence contract
Evidence Question / Router
IT feasibility draft

office:
AIR v4 one runtime test

then:
one-issue thin end-to-end prototype
→ physical Agent topology decision
```

## Current state

- ADR-001: ACCEPTED
- ADR-002: ACCEPTED
- ADR-003: ACCEPTED
- Front logic: substantially developed
- AIR v4: runtime pending
- BO: in development
- Company State: design starts now
- Market / Competitor Intelligence: newly explicit / design starts now
- Department Review: parallel lane defined
- Physical Agent count: NOT FIXED
- Final target: complete MRI response draft
- Generalization: NOT VERIFIED
