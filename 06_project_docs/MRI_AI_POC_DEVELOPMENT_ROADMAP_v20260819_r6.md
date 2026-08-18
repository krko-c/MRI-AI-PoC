# MRI AI PoC Development Roadmap v20260819 r6

## 0. Development Principle

The project is moving from **front-pipeline refinement** to **end-to-end research capability**.

Do not collapse the logical architecture merely to reduce Agent count.

Do not assume each logical step requires a separate physical Agent.

The next goal is to build enough of the downstream system to test one MRI issue end-to-end.

## Phase A — Front Pipeline Closure

Current:
- Extraction developed
- Fidelity logic developed
- Screening logic developed
- AIR v4 generated
- runtime orchestration pending

Remaining:
1. run v4 once,
2. record actual orchestration behavior,
3. build v5 if warranted,
4. perform minimum regression.

Exit:
- usable validated issue input,
- usable Screening result,
- no endless optimization of stage ownership.

## Phase B — BO Production Logic

Continue current work.

### Regression set
- H01 reverse-money-move: direct financial-market opportunity
- H02 pet industry: conditional investability
- H03 youth financial vulnerability: role-boundary / partner-dependent case

### Output
- BO hypothesis
- hypothesis chain
- critical assumptions
- evidence questions
- validation priority
- validation status

### Rules
- 1–3 default / max 4
- no scope-only duplication
- no company-state leakage
- no unsupported named entities
- no industry-growth → ETF shortcut

Exit:
`BO Production Prompt v1`

## Phase C — Company State Research Contract

Start now, in parallel with B.

Define:
- what "current state" means,
- source taxonomy,
- internal retrieval order,
- UNKNOWN vs ABSENCE,
- historical MRI response use,
- product / fund data use,
- internal plan / document use,
- department-response integration,
- as-of handling,
- evidence IDs and provenance.

Do not wait for full external-research completion.

## Phase D — Market / Competitor Intelligence Contract

New explicit lane.

Define:
- market status questions,
- competitor / peer actions,
- financial-group actions,
- product launch / supply trends,
- policy / industry developments,
- lookback windows,
- competitor universe rules,
- source hierarchy,
- evidence-purpose tags.

Distinguish:
```text
OPPORTUNITY_VALIDATION
MARKET_COMPETITOR_INTELLIGENCE
BOTH
```

## Phase E — Evidence Question / Router

Keep the logical chain:

```text
BO
→ Evidence Question
→ Router
→ Targeted Research
→ Evidence Integration
→ Validated BO
```

Physical implementation remains open.

Router design:
- choose only necessary source(s),
- merge duplicate questions,
- preserve as-of,
- preserve evidence category,
- distinguish no result from no evidence.

## Parallel Track — IT Feasibility

Start before final field specification.

Check:
- ZeroIn historical as-of
- requested-window setup changes
- FreeSIS historical replay
- News full text
- Policy full text / status / effective date
- AIR API / Tool / batch access
- internal product / document retrieval interfaces

This is feasibility, not final schema negotiation.

## Phase F — One-Issue Thin End-to-End Prototype

Before overbuilding AIR components, take one screened MRI issue and run:

```text
Validated Issue
→ BO
→ external validation
→ market / competitor intelligence
→ company state
→ gap
→ strategy
→ final MRI response draft
```

Manual handoff is acceptable in this phase.

Purpose:
- discover which logical components need dedicated Agents,
- discover where Tool boundaries matter,
- verify output usefulness,
- identify missing data.

## Phase G — Evidence / State Integration

Define explicit source classes:

```text
MRI_SOURCE
EXTERNAL_MARKET
EXTERNAL_COMPETITOR
EXTERNAL_POLICY
INTERNAL_SYSTEM
INTERNAL_DOCUMENT
DEPARTMENT_FACT
DEPARTMENT_PROPOSAL
AI_INFERENCE
```

For each claim preserve:
- source class
- evidence ID
- status
- as-of date
- confidence / verification state where applicable

`UNKNOWN != ABSENCE`.

## Phase H — Gap / Strategy

Input:
- validated BO
- market / competitor intelligence
- company state
- department evidence if available

Output:
- gap
- implications
- strategic options
- recommended response direction
- constraints
- unresolved questions

Gap + Strategy may later become one physical Agent or multiple components; not fixed now.

## Phase I — Final MRI Response

Final target:
complete issue-level MRI response draft.

Not merely:
- issue brief,
- department request,
- data dump.

Include:
- issue summary
- market / competitor status
- company current state
- business opportunity
- gap
- response strategy
- department input
- unknowns / constraints
- sources

Human remains final reviewer / submitter.

## Phase J — Physical AIR Architecture

Only after one thin end-to-end prototype.

Decide Agent boundaries using:
- data permissions
- source/tool boundaries
- parallelism
- bias isolation
- runtime reliability
- handoff quality
- cost / latency

No target Agent count is preselected.

## Immediate Work Order

### Now
1. H03 BO regression
2. BO Production Prompt v1
3. Company State contract
4. Market / Competitor Intelligence contract
5. Evidence Question / Router
6. IT feasibility draft

### Office
7. AIR v4 one runtime test
8. v5 only from observed result

### Then
9. one-issue thin end-to-end prototype
10. decide physical Agent topology
11. formal dataset request
12. expand regression and production implementation
