# MRI AI PoC Master Plan

_Last updated: 2026-08-19_

## 0. Purpose

This is the **live Master Plan** for the MRI AI PoC.

Past `r1/r2/r3/...` files are retained as historical snapshots only.  
The live document is updated in place and Git history is the primary version history.

## 1. Project Objective

The system supports the product-strategy analyst's own end-to-end MRI work.

The AI should help the analyst:

```text
MRI understanding
→ issue relevance screening
→ business-opportunity hypothesis
→ opportunity validation
→ market / competitor intelligence
→ company / internal current-state research
→ evidence integration
→ gap analysis
→ response strategy
→ complete MRI response draft
```

Relevant departments review the same screened issues in parallel.

Department responses are one input among several.  
They are not the purpose of the system and are not the sole source of Company State.

The user remains the final human owner of review, combination, judgment, and submission.

## 2. What the System Is Not

The project is not primarily:
- a department-routing tool,
- a question-generation tool,
- a simple issue-brief generator,
- a fully autonomous submitter,
- a fixed 4-Agent system,
- a fixed N-Agent system.

## 3. Source of Truth

1. Accepted ADRs
2. This live Master Plan / live Development Roadmap
3. Current Canonical Prompt Pack
4. Regression records / policies
5. IT logical specifications
6. Runtime / AIR mapping
7. historical snapshots / archive
8. conversation history

Candidate AIR prompts are not automatically canonical.

## 4. Core Architecture

```text
MRI
↓
Raw Issue Extraction
↓
Fidelity Validation
↓
Validated Issue View
↓
Screening
   │
   ├────────────→ BO / Opportunity Research
   │                - BO hypothesis
   │                - assumptions
   │                - evidence questions
   │                - validation routing
   │                - targeted research
   │                - validated BO
   │
   ├────────────→ Market / Competitor Intelligence
   │                - market status
   │                - competitor / peer actions
   │                - product / supply trends
   │                - financial-group actions
   │                - policy / industry developments
   │
   ├────────────→ Company / Internal State Research
   │                - products / funds
   │                - historical MRI responses
   │                - internal plans / documents
   │                - approved internal data
   │
   └────────────→ Department Review
                    - current activities
                    - possible actions / ideas
                    - future plans
                    - constraints

        Opportunity questions ─┐
        Market-intel questions ├→ Shared Research Request Registry
                               ↓
                     Cross-lane Normalize / Dedup
                               ↓
                        Source / Tool Router
                               ↓
                         Shared Evidence Pool
                         ↙                 ↘
                 BO interpretation     Market-intel interpretation

External / internal / department results
↓
Evidence / State Integration
↓
Gap
↓
Strategy
↓
Complete MRI Response Draft
↓
Human Review / Combination / Submission
```

## 5. Logical Step != Physical Agent

Logical responsibilities remain explicit for reasoning quality and traceability.

They do not imply one physical AIR Agent per step.

Physical Agent boundaries will be decided using:
- source / permission boundaries,
- information barriers,
- independent-validation need,
- parallelism benefit,
- runtime reliability,
- handoff quality,
- latency / cost,
- maintainability.

No fixed Agent count is accepted before the Thin End-to-End prototype and AIR runtime evidence.

## 6. Front Pipeline

### 6.1 Raw Extraction
Preserve:
- top-level issue boundaries,
- order,
- state / modality,
- source meaning.

### 6.2 Fidelity Validation
Statuses:
- PASS
- CORRECTABLE
- FAIL

Raw extraction remains immutable.

Stage 02 creates `validated_issue_view`.

- PASS → validated view may mirror raw extraction
- CORRECTABLE → only minimal local corrections
- FAIL → Screening blocked and retry / stop policy applies

Fidelity remains a required **logical function**.  
Whether it needs a dedicated physical Agent is an implementation question.

### 6.3 Screening
Consumes only `validated_issue_view`.

Five lenses:
- product
- investment_theme
- customer
- channel
- group_collaboration

Decision:
- any 2 → OPPORTUNITY
- no 2 and at least one 1 → MONITOR
- all 0 → EXCLUDE
- Fidelity FAIL → VALIDATION_BLOCKED

No total score.

## 7. Deterministic vs Semantic Validation

### Deterministic structural checks
Prefer code / tool / process gates for:
- required schema
- duplicate IDs
- allowed enums
- five-lens count
- score domain
- classification consistency
- future-stage ownership fields
- forbidden-input presence

### Semantic LLM checks
Use LLM judgment for:
- state / modality distortion
- recommendation leakage
- issue-boundary meaning
- source entailment
- asset-manager directness
- BO overreach

LLM self-check is diagnostic only.

## 8. Workflow Date

`analysis_as_of_date` is owned by Workflow Start.

- CURRENT: execution date if not supplied
- HISTORICAL_REPLAY: explicit date required
- downstream components inherit unchanged

## 9. BO Information Barrier

Parallel execution does **not** mean shared context.

Initial BO generation may receive only:

```text
analysis_as_of_date
validated_issue
screening_result
```

It must not receive:
- company_state
- department_responses
- internal_product_data
- internal_business_plan
- market_research_result generated by another lane

Implementation requirement:
the orchestrator must physically omit forbidden fields from BO initial input.

Prompt-only prohibition is insufficient.

Candidate deterministic check:

```text
forbidden_input_present == false
```

## 10. BO Logical Contract

BO is a hypothesis, not a fact.

Logical sequence:

```text
MRI observation
→ inferred implication
→ opportunity hypothesis
→ critical assumptions
→ evidence questions
→ validation
```

Per issue:
- default 1–3 BOs
- hard max 4
- scope-only differences do not justify separate BOs
- implementation vehicles do not automatically create separate BOs

BO remains logically upstream of Company State.

## 11. Market / Competitor Intelligence

This is an explicit research purpose, separate from Opportunity Validation.

It answers:
- what is changing in the relevant market?
- what are peers / competitors doing?
- what are financial groups doing?
- what related products are being launched / supplied?
- what policy / industry developments matter?

Research-purpose tags:

```text
OPPORTUNITY_VALIDATION
MARKET_COMPETITOR_INTELLIGENCE
BOTH
```

## 12. Shared Research / Cross-Lane Dedup

Opportunity Validation and Market / Competitor Intelligence may require the same news, policy, product or market evidence.

Do not solve this only with post-hoc tags.

Before retrieval:

```text
Opportunity Evidence Questions
+
Market-Intel Research Questions
↓
Shared Research Request Registry
↓
Normalize
↓
Cross-lane Deduplicate / Merge
↓
Source / Tool Router
↓
Shared Evidence Pool
```

The same Evidence object may then be interpreted for different purposes.

## 13. Company / Internal State Research

May start immediately after Screening in parallel with other lanes.

Potential sources:
- internal product / fund data
- historical MRI responses
- internal business / marketing plans
- approved internal documents
- other approved operational data
- department responses when available

Status vocabulary must distinguish:
- CONFIRMED_PRESENT
- CONFIRMED_ABSENT
- NOT_FOUND
- UNKNOWN

`UNKNOWN != ABSENCE`.

Search coverage must be recorded before absence is claimed.

## 14. Department Review

Department Review starts after Screening and proceeds in parallel.

Purpose:
- relevant departments independently review the issue,
- state current activity,
- identify possible actions,
- share plans,
- identify constraints.

Department responses remain distinguishable as:
- DEPARTMENT_FACT
- DEPARTMENT_PROPOSAL

They must not be presented as AI-generated fact or vice versa.

## 15. Evidence / State Integration

Preserve source class and provenance.

Candidate source classes:
- MRI_SOURCE
- EXTERNAL_MARKET
- EXTERNAL_COMPETITOR
- EXTERNAL_POLICY
- INTERNAL_SYSTEM
- INTERNAL_DOCUMENT
- DEPARTMENT_FACT
- DEPARTMENT_PROPOSAL
- AI_INFERENCE

Integration is not flattening.  
Contradictions, unknowns, and source differences remain visible.

## 16. Gap and Strategy

Inputs:
- validated BO
- Market / Competitor Intelligence
- Company State
- Department evidence if available

Outputs:
- material gap
- implications
- strategic options
- recommended response direction
- constraints
- unresolved questions

## 17. Final Target

The target is a **complete MRI response draft**, not merely an Issue Brief.

The canonical output contract is currently:

`06_project_docs/contracts/FINAL_MRI_RESPONSE_SCHEMA_v0.md`

This schema is intentionally provisional until one Thin End-to-End issue is completed.

## 18. Development Principle

Do not freeze upstream schemas only by inspecting upstream outputs.

The next major design step is:

```text
Final Response Schema v0
→ one issue Thin End-to-End
→ inspect what was actually used
→ revise BO / Company State / Market Intel / Router contracts
→ then freeze v1 contracts
```

Manual handoff is explicitly allowed during the Thin E2E.

## 19. AIR Runtime

AIR v4 remains an orchestration experiment.

Required front work:
1. run v4 once,
2. record actual result,
3. build v5 only from observed behavior,
4. perform minimum front regression.

Do not pause downstream development while waiting for this test.

## 20. Canonical Prompt Pack

Current canonical pack remains the stored baseline.

Older components 04–08 that conflict with ADR-001/002/003 are not production-authoritative merely because their old flags say otherwise.

Until formally reconciled:
- treat them as architecture-revision candidates / historical implementations,
- do not assume their downstream relationships are current.

## 21. Historical Snapshot Policy

Existing `r1/r2/r3/r4/r5/r6` files are retained.

They are historical snapshots, not live pointers.

Going forward:
- update `MRI_AI_POC_MASTER_PLAN.md`
- update `MRI_AI_POC_DEVELOPMENT_ROADMAP.md`
- update `MRI_AI_POC_DEVELOPMENT_CHECKPOINT.md`

Use Git history for normal version comparison.

Create a new frozen snapshot only for a meaningful milestone, not every edit.
