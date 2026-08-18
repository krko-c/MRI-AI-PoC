# MRI AI PoC Master Plan v20260819 r6

## 0. Purpose and Status

r6 consolidates the current development direction after:
- ADR-001: Hypothesis-Driven External Research,
- ADR-002: Department Review as a parallel internal evidence lane,
- ADR-003: Parallel Research Lanes and Implementation Neutrality.

The key shift is **not** to simplify the logical architecture into an arbitrary small number of Agents.

The shift is:

1. preserve the logical reasoning controls that prevent overreach,
2. stop equating logical steps with physical Agents,
3. move development attention from the already-developed front pipeline toward the actual research workload,
4. explicitly add Market / Competitor Intelligence,
5. allow Company State Research to start in parallel after Screening,
6. keep the final target as a complete MRI response draft for human review and synthesis.

## 1. Project Objective

The project supports the product-strategy analyst's own end-to-end MRI work.

The AI should help the analyst:

```text
understand the MRI
→ identify relevant issues
→ develop business-opportunity hypotheses
→ validate them with evidence
→ investigate market / competitor developments
→ investigate company current state
→ identify gaps
→ develop response strategies
→ prepare a complete MRI response draft
```

At the same time, relevant departments review the same screened issues in parallel.

Department responses are one input among several.

The final user remains responsible for human judgment, combining materials, and formal submission.

## 2. What the system is NOT

The system is not primarily:
- a department-routing tool,
- a question-generation tool,
- an Issue Brief generator,
- a fully autonomous final submitter,
- a fixed 4-Agent system,
- a fixed 21-Agent system.

## 3. Source-of-Truth Order

1. Accepted ADRs
2. Latest Master Plan / Development Roadmap
3. Canonical Prompt Pack
4. Regression Log / Regression Policy
5. IT Logical Spec
6. Runtime / AIR Mapping
7. Archive
8. Conversation history

Current Canonical Pack remains the stored baseline until newer candidate rules are runtime/regression validated.

## 4. Current Logical Architecture

```text
MRI
↓
01 Raw Issue Extraction
↓
02 Fidelity Validation
↓
Validated Issue View
↓
03 Screening
   │
   ├───────────────────────→ A. BO / Opportunity Research
   │                           - BO Hypothesis
   │                           - Critical Assumptions
   │                           - Evidence Questions
   │                           - Validation Routing
   │                           - Targeted Research
   │                           - Evidence Integration
   │                           - Validated BO
   │
   ├───────────────────────→ B. Market / Competitor Intelligence
   │                           - market status
   │                           - competitor actions
   │                           - financial-group responses
   │                           - product launches / supply
   │                           - policy / industry developments
   │
   ├───────────────────────→ C. Company / Internal State Research
   │                           - products / funds
   │                           - historical MRI responses
   │                           - internal plans / documents
   │                           - approved internal data
   │
   └───────────────────────→ D. Department Review
                               - current activities
                               - actions / ideas
                               - future plans
                               - implementation constraints

                   ↓
          Evidence / State Integration
                   ↓
                 Gap
                   ↓
               Strategy
                   ↓
          Final MRI Response Draft
                   ↓
          Human Review / Submission
```

## 5. Parallelism vs Information Boundaries

Research lanes may run in parallel for speed.

But context boundaries must be preserved.

### BO Generation
Must not consume:
- Company State,
- Department Responses,
- internal product availability.

Reason:
avoid redefining the opportunity around what the company already has.

### Market / Competitor Intelligence
Independent external intelligence lane.

### Company State
May begin after Screening for operational efficiency.

### Department Review
May begin after Screening because it has human lead time.

## 6. Front Pipeline Contract

### 6.1 Raw Extraction
Preserve source-derived issue structure and state/modality.

### 6.2 Fidelity
Statuses:
`PASS | CORRECTABLE | FAIL`

Raw extraction remains immutable.

Stage 02 creates:
`validated_issue_view`

- PASS → validated view
- CORRECTABLE → minimal local correction
- FAIL → Screening blocked

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
- no 2, at least one 1 → MONITOR
- all 0 → EXCLUDE
- Fidelity FAIL → VALIDATION_BLOCKED

No total score.

## 7. Validation Architecture

### Deterministic
Use code/tool/process gates where feasible for:
- schema structure,
- duplicate IDs,
- required fields,
- valid score domains,
- classification consistency,
- stage ownership constraints.

### Semantic LLM validation
Retain for:
- state/modality distortion,
- recommendation leakage,
- issue-boundary meaning,
- asset-manager directness,
- source entailment.

### Human review
Human review is the final control, but it does not replace machine validation where machine validation meaningfully reduces rework.

## 8. Business Opportunity Logic

BO remains logically upstream of Company State.

Per issue:
- default 1–3 BOs,
- hard max 4,
- scope difference alone does not justify a new BO.

Each BO:
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
- validation_status

New BO status begins:
`UNVALIDATED`

Logical sequence:

```text
BO Hypothesis
→ Evidence Question
→ Validation Routing
→ Targeted Research
→ Evidence Integration
→ Validated BO
```

Important:
this sequence is a **logical contract**, not a physical-Agent count commitment.

## 9. Market / Competitor Intelligence

This is now an explicit architecture lane.

It answers questions such as:
- what is the market doing?
- what are other asset managers doing?
- what are banks / securities firms / financial groups doing?
- what related products have been launched?
- what relevant policies / industry structures are changing?

This lane is distinct from Opportunity Validation.

A fact may be relevant to both, but the purpose must be tagged.

Candidate evidence-purpose tag:
```text
OPPORTUNITY_VALIDATION
MARKET_COMPETITOR_INTELLIGENCE
BOTH
```

## 10. Company / Internal State Research

Company State is a major development area and should not wait until all external research is finished.

It may run in parallel after Screening.

Potential sources:
- internal fund / product data,
- internal plans,
- historical MRI responses,
- marketing / business documents,
- approved internal operational data,
- department responses when received.

Important:
Company State must not flow backward into initial BO generation.

## 11. Department Review

Department Review remains a parallel human lane.

Its role:
- review the same issue independently,
- describe current actions,
- propose possible actions,
- provide future plans,
- surface constraints.

Department responses are tagged separately from:
- internal system facts,
- external facts,
- AI inference.

## 12. Evidence / State Integration

The integration layer combines, without collapsing provenance:

```text
MRI source facts
External BO evidence
Market / competitor intelligence
Internal system facts
Department facts
Department proposals
AI inference
```

`UNKNOWN != ABSENCE` remains mandatory.

## 13. Gap and Strategy

```text
Validated Opportunity
+
Market / Competitor Intelligence
+
Company Current State
+
Department Evidence
→ Gap
→ Strategy
```

Strategy is the AI / analyst's own response logic, not merely a copy of department replies.

## 14. Final MRI Response

The final system target is a **complete MRI issue response draft**, not merely an intermediate Issue Brief.

The output should support the user's final work by providing, per issue:

- MRI issue interpretation
- current market / competitor status
- validated business opportunity
- company current state
- department input where available
- gap
- response strategy
- constraints / unknowns
- evidence / provenance
- status of unverified claims

The user may directly combine or edit the result into the formal response.

## 15. Logical Step != Physical Agent

This principle is now explicit and non-negotiable.

No physical Agent count is frozen.

Possible reasons to separate:
- distinct source / permission
- independent judgment
- parallel benefit
- information-barrier requirement
- runtime stability

Possible reasons to combine:
- same source
- continuous reasoning
- low handoff value
- handoff ownership drift
- excessive cost / latency

Physical architecture is decided after runtime tests and end-to-end prototyping.

## 16. Development Focus Shift

### Front pipeline
Status:
substantially developed.

Remaining:
- run AIR v4 once,
- build v5 from actual runtime result,
- close minimum regression.

Do not spend disproportionate time further optimizing stage ownership before downstream work exists.

### Highest-priority unfinished areas

```text
1. BO production logic
2. Company State Research
3. Market / Competitor Intelligence
4. Evidence Question / Router
5. IT feasibility / data access
6. Evidence integration
7. Gap / Strategy
8. Final MRI response
```

## 17. AIR Runtime

v4:
`GENERATED / RUNTIME TEST PENDING`

Purpose:
Supervisor orchestration experiment only.

After one runtime test:
- if viable → v5 front contract implementation
- if not viable → use fallback orchestration

Do not redesign the entire project around v4 behavior.

## 18. IT Feasibility

Begin in parallel.

Initial checks:
- ZeroIn historical as-of?
- requested-period setup amount changes?
- FreeSIS historical replay?
- AIR-callable API / Tool / batch?
- News full article text?
- Policy full text + status / effective date?
- internal document / product-data retrieval path?

## 19. Current Status

| Area | Status |
|---|---|
| ADR-001 | ACCEPTED |
| ADR-002 | ACCEPTED |
| ADR-003 | ACCEPTED |
| Front pipeline logic | substantially developed |
| AIR front runtime | v4 pending |
| BO | in development |
| Market / Competitor Intelligence | architecture defined / implementation pending |
| Company State | architecture defined / implementation pending |
| Department Review | parallel lane defined |
| Evidence Question / Router | in development |
| Evidence Integration | pending |
| Gap / Strategy | pending |
| Final MRI Response | pending |
| Physical Agent count | NOT FIXED |
| Generalization | NOT VERIFIED |

## 20. Immediate Next

1. Complete BO regression with H03 and freeze BO Production Prompt v1.
2. Define Company State Research contract in parallel.
3. Define Market / Competitor Intelligence contract in parallel.
4. Design Evidence Question dedup + Validation Router.
5. Prepare lightweight IT feasibility inquiry.
6. At office, run AIR v4 once.
7. Build front v5 only from observed v4 result.
8. Then prototype one issue end-to-end through research → gap → strategy → final response.
