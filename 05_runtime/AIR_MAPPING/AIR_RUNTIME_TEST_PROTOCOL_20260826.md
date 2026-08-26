# AIR RUNTIME TEST PROTOCOL
Version: 2026-08-26
Applies to: MRI_WORKFLOW_v5_20260826_DRAFT.json

## Principle
AIR JSON is maintained continuously together with prompt/spec changes.
Every meaningful runtime update should be imported into AIR Studio and smoke-tested.

Do not equate:
IMPORT PASS = CONTENT QUALITY PASS = PRODUCTION READY.

## Test levels for every version

### T1. Import / Graph Restore
PASS when:
- JSON imports without schema error.
- Supervisor, Responder, Output, 01/02/03, KB, placeholders, Strategy, Final nodes appear.
- FLOW/HAS links are restored.
- KB `kb-6b0fd700` remains linked to the intended existing stages.

### T2. Supervisor Routing / Ownership
PASS when:
- Supervisor calls stages in the intended order.
- Each stage writes only its owned section.
- Earlier sections are preserved.
- analysis_as_of_date is preserved.
- Specialist natural-language summaries are not substituted for cumulative JSON.

### T3. Draft Placeholder Safety
Expected current behavior:
- External Research = NOT_YET_IMPLEMENTED / DATA_GAP
- Company Current State = NOT_YET_IMPLEMENTED / DATA_GAP
- Department Review = NOT_YET_IMPLEMENTED / DATA_GAP

PASS when:
- No placeholder invents facts.
- Strategy does not silently turn DATA_GAP into factual evidence.
- Final does not hide insufficient upstream strategy/research quality.

### T4. Final Preservation
PASS when:
- Responder does not rewrite final facts, numbers, strategy priorities, or final_report_text.
- This specifically guards against the prior v4 failure where the final responder/supervisor changed content.

### T5. Functional Quality
NOT EXPECTED TO PASS YET.
Run only after real research/current-state/department inputs are connected.

Future quality test must check:
- Current Status depth
- Strategy breadth/diversity
- Core/Adjacent/Exploratory generation
- Quick Win/Core/Expansion/New Bet portfolio
- concrete product/service/marketing/group ideas
- actual Action Plan rather than unfinished research tasks
- factual integrity

## Test log convention
For every runtime JSON version, record:
- Date
- JSON filename
- AIR environment
- Import PASS/FAIL
- Routing PASS/FAIL
- Section ownership PASS/FAIL
- Placeholder safety PASS/FAIL
- Final preservation PASS/FAIL
- Functional-quality status
- Failure details
- Next change

Recommended file:
`05_runtime/AIR_MAPPING/AIR_RUNTIME_TEST_LOG.md`
