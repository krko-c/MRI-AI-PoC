# MRI AI PoC Development Checkpoint — 2026-08-18

## Current Git baseline

Previous checkpoint commit:
`d59b9cc` — `docs: checkpoint AIR runtime and roadmap 2026-08-18`

This file is a living current-status summary. Historical states remain in Git history.

## Decisions added after d59b9cc

### 1. Fidelity Correction Contract

Raw Stage 01 output is preserved:
`issue_extraction = raw source-derived output`

Stage 02 owns:
`validated_issue_view`

Statuses:
`PASS | CORRECTABLE | FAIL`

Flow:
```text
PASS
→ validated_issue_view
→ Screening

CORRECTABLE
→ minimum correction
→ validated_issue_view
→ Screening

FAIL
→ no Screening
→ retry / VALIDATION_BLOCKED
```

03 Screening must use `validated_issue_view`, not raw `issue_extraction`.

### 2. Deterministic Validation Flow

LLM self-check is diagnostic only.

Structural conditions should be enforced deterministically where feasible:
- issue array
- duplicate topic_id
- stage ownership fields
- five screening lenses
- score range
- no total score
- deterministic classification consistency

Semantic validation remains LLM-based.

Retry:
- one retry only
- second Stage 01 structural fail → WORKFLOW_ERROR
- second Fidelity FAIL → VALIDATION_BLOCKED

`errors[]` is now active.

### 3. analysis_as_of_date Ownership

Owner:
`Workflow Start`

CURRENT:
- workflow execution date if user did not provide one.

HISTORICAL_REPLAY:
- required input.

Downstream Agents / Tools inherit but do not mutate.

### 4. BO Explosion Control

Per MRI issue:
- default 1–3 BOs
- hard max 4

Do not create a separate BO only because `opportunity_scope` differs.

Evidence Questions:
`Generate → Normalize → Deduplicate / Merge → Router`

## AIR status

### v4
File:
`MRI_01_02_03_v4_SUPERVISOR_ORCHESTRATED.json`

Purpose:
- validate Supervisor-managed stage ownership.

Status:
`GENERATED / RUNTIME TEST PENDING`

Do not mark PASS yet.

### v5
Will be created only after v4 runtime result.

Target:
- validated_issue_view
- PASS/CORRECTABLE/FAIL
- blocking / retry
- deterministic structural gate
- active errors[]
- analysis_as_of_date

## Canonical Prompt status

Do not promote v4 directly into a new Canonical Prompt Pack yet.

Current stance:
`AIR candidate rules = pending runtime validation`

After runtime stabilization:
- create next Canonical Prompt Pack version,
- update canonical pointer,
- reconcile stale downstream/role flags.

## Immediate next logical work

`BO H02 regression → BO production prompt v1 → Evidence Question normalization/dedup → Validation Router`

## Parallel work

Send lightweight IT feasibility questions before the full data-spec request.

Check:
- ZeroIn historical as-of
- requested-period setup change
- FreeSIS historical replay
- AIR-callable interface
- News full text
- Policy full text + status/effective date

## Current state labels

- Architecture: substantially defined
- Front Logical Contract: r4 defined
- AIR front physical orchestration: in progress
- v4 Supervisor orchestration: runtime pending
- deterministic gate: logical design defined / implementation pending
- BO Hypothesis: in development
- Evidence Question: in development
- Dataset request: pending router/spec
- IT feasibility: ready to start in parallel
- Generalization: NOT VERIFIED
