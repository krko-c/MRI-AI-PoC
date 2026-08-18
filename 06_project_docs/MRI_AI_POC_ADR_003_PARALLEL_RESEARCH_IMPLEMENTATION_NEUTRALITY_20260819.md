# ADR-003 — Parallel Research Lanes and Implementation Neutrality

- Date: 2026-08-19
- Status: ACCEPTED
- Scope: MRI AI PoC logical architecture and development prioritization
- Related: ADR-001, ADR-002

## 1. Context

After clarifying the real operating process and reviewing external feedback, the project needs to distinguish three different questions:

1. What logical reasoning steps are required for a trustworthy MRI analysis?
2. Which of those steps should run in parallel for practical speed?
3. How many physical AIR Agents should implement those logical steps?

Earlier design work decomposed many logical responsibilities in detail. That decomposition remains useful for traceability and control, but it must not be interpreted as a commitment to one physical Agent per logical step.

At the same time, practical development effort has been disproportionately concentrated on the front pipeline (`Extraction → Fidelity → Screening`). The next phase must shift effort toward the research work that constitutes most of the analyst's actual workload:
- Company / internal current-state research,
- market / competitor intelligence,
- business-opportunity validation,
- gap / strategy development.

## 2. Decision

### 2.1 Preserve logical decomposition

The project retains the major logical responsibilities already defined, including:

```text
BO Hypothesis
→ Evidence Question
→ Validation Routing
→ Targeted Research
→ Evidence Integration
→ Validated BO
```

These are reasoning responsibilities and traceability checkpoints.

They are **not** a commitment to six separate physical Agents.

### 2.2 Do not pre-fix physical Agent count

Physical Agent count remains an implementation decision.

Agents may be combined or separated based on:
- source / permission boundaries,
- need for independent judgment,
- information-leakage control,
- runtime reliability,
- parallel-execution benefit,
- cost / latency,
- maintainability.

No fixed target such as "4 Agents" or "21 Agents" is accepted at this stage.

### 2.3 Add explicit Market / Competitor Intelligence

External research has two distinct logical purposes:

```text
A. Opportunity Validation
B. Market / Competitor Intelligence
```

Opportunity Validation tests whether a BO hypothesis is supported.

Market / Competitor Intelligence describes what the market, competitors, financial groups, relevant products, policies, and industry participants are actually doing.

The second purpose must be explicit in the architecture rather than treated as an incidental by-product of BO validation.

### 2.4 Allow Company State Research to run in parallel

After Screening, Company / Internal State Research may begin in parallel with Opportunity Research and Department Review.

However, information barriers remain:

```text
BO generation must not consume:
- Company State results
- Department Responses
```

This preserves ADR-001's company-blind BO principle while allowing practical parallel execution.

### 2.5 Final output remains a complete MRI response

The system's target is not merely an "Issue Brief" or a department-request form.

The analyst / AI still produces its own full issue-level analysis and response draft, including:
- issue interpretation,
- relevant external facts,
- market / competitor developments,
- company current state,
- business opportunity,
- gap,
- response strategy,
- evidence / source status.

Department responses are parallel inputs that the user combines with the AI's own analysis.

The user remains the final human owner of synthesis, judgment, and submission.

## 3. Updated Parallel Architecture

```text
MRI
↓
Extraction
↓
Fidelity / Validated Issue View
↓
Screening
   │
   ├────────────→ BO / Opportunity Research
   │                 └→ hypothesis
   │                 └→ evidence questions
   │                 └→ targeted validation
   │                 └→ validated BO
   │
   ├────────────→ Market / Competitor Intelligence
   │                 └→ market status
   │                 └→ competitor / group actions
   │                 └→ product / policy / industry developments
   │
   ├────────────→ Company / Internal State Research
   │                 └→ internal products / funds
   │                 └→ historical MRI responses
   │                 └→ plans / internal documents
   │                 └→ other approved internal evidence
   │
   └────────────→ Department Review
                     └→ current activities
                     └→ possible actions / ideas
                     └→ future plans
                     └→ constraints

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

## 4. Information-boundary rule

Parallel execution does not mean unrestricted context sharing.

### BO / Opportunity Research
May use:
- MRI validated issue,
- Screening result,
- general asset-management knowledge,
- external validation evidence.

Must not use during initial BO generation:
- Company State,
- Department Responses,
- internal product availability.

### Company State Research
May use:
- approved internal data and documents,
- historical internal responses,
- department responses when received.

### Market / Competitor Intelligence
May use:
- external market data,
- news,
- competitor / financial-group public information,
- product / industry / policy information.

## 5. Front-pipeline development boundary

The front pipeline remains necessary because downstream work depends on correct issue interpretation.

However:

> Front-pipeline correctness is now sufficient to proceed; it is no longer the primary development focus.

Next AIR work on the front pipeline should be limited to:
1. one v4 orchestration test,
2. one v5 implementation pass based on the result,
3. regression sufficient to verify that the front pipeline is usable.

Do not continue optimizing stage ownership indefinitely before building downstream research capabilities.

## 6. Consequences

### Positive
- aligns development effort with actual analyst workload,
- introduces the missing Market / Competitor Intelligence function,
- preserves rigorous BO logic without overcommitting to Agent count,
- enables practical parallel execution,
- preserves company-blind BO generation,
- keeps the final target as a full MRI response.

### Trade-offs
- orchestration becomes more parallel,
- evidence provenance and source-type tagging become more important,
- downstream integration contract must reconcile external, internal, department, and AI-generated material,
- physical Agent design remains open until runtime evidence is available.

## 7. Rejected overcorrections

The following are explicitly **not** adopted:

- fixed 4-Agent architecture,
- automatic collapse of BO → EQ → Router → Research → Integration into one Agent,
- deletion of Fidelity as a logical function,
- reduction of final output to a simple Issue Brief,
- assumption that human final review makes QC / validation unnecessary,
- use of a simple 6-field department response form as the complete internal schema.

## 8. Development implication

The immediate priority shifts from front-pipeline refinement toward:

```text
BO production logic
+
Company State Research design
+
Market / Competitor Intelligence design
+
Evidence Question / Router
+
IT feasibility
```

while the AIR front pipeline receives only the minimum additional runtime work needed to close the current experiment.
