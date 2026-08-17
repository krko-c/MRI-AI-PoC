# MRI AI PoC — DEVELOPMENT ROADMAP

**VERSION:** v20260818

---

# CURRENT POSITION

Completed / Stabilized:

00 Architecture Contract v2
01 MRI Issue Extraction
02 Source/Fidelity Validator
03 MRI Screening
04 News Search Planner
05 External Evidence Source Router
06 Policy / Legal Retrieval Planner

Draft:

07 External Evidence Extractor

Current Next:

08 ZeroIn Retrieval / Candidate Finder

---

# PHASE 1 — MRI UNDERSTANDING

00 Architecture Contract
01 Extraction
02 Source/Fidelity Validator
03 Screening

STATUS:
Logical design stabilized.

---

# PHASE 2 — EXTERNAL EVIDENCE RETRIEVAL

04 News Search Planner
05 Source Router
06 Policy / Legal Retrieval Planner

STATUS:
Final Candidate.

NEXT:

08 ZeroIn Retrieval / Candidate Finder v1.0

09 FreeSIS Retrieval Planner v1.0

10 Unified External Retrieval Contract

Then:

IT Data Request Specification
IT Feasibility Check
Physical Schema Mapping

---

# PHASE 3 — EXTERNAL EVIDENCE NORMALIZATION

07 External Evidence Extractor

현재 v1.0 Draft를
Retrieval Layer 완성 후 다시 검토.

Then:

Regression Test
→ Final Candidate

11 External Evidence Integrator

---

# PHASE 4 — BUSINESS OPPORTUNITY

12 Business Opportunity Agent v2

Principle:

Company-blind

Input:

- MRI
- Screening
- Integrated External Evidence
- General AM knowledge

Do not use:

- NH-Amundi products
- NH-Amundi DB
- Current capability
- Internal history

Expected Business Scope:

- GENERAL_ASSET_MANAGER
- FULL_SERVICE_ASSET_MANAGER
- FINANCIAL_GROUP_ASSET_MANAGER

Role Types:

- DIRECT
- PARTNER_DEPENDENT
- ADJACENT

---

# PHASE 5 — COMPANY STATE

13 Product RAG

14 Fund Universe

15 Quant DB / TB_EARNING

16 Internal History

17 Integrated Current State

Rules:

RAG no hit ≠ absence

Missing data ≠ capability gap

Past plan ≠ current execution

Only verified Current State facts.

---

# PHASE 6 — DECISION

18 Gap Analysis

Gap Status:

- KNOWN_DEFICIENCY
- UNKNOWN
- NO_MATERIAL_GAP

UNKNOWN을 Gap으로 처리하지 않는다.


19 Strategy

Strategy Types:

- CONTINUE
- VERIFY_FIRST
- ACTIVATE
- NEW_INITIATIVE
- MONITOR


20 Final Response

21 Quality Check

---

# PHASE 7 — RUNTIME IMPLEMENTATION

AIR Mapping

PDF
→ Parser
→ Chunker
→ Knowledge Base / Pipeline
→ Retrieval
→ Agents
→ Final Response

Then:

E2E Test

Historical Replay Test

Unseen MRI Generalization Test

---

# IMMEDIATE NEXT TASK

08_ZEROIN_RETRIEVAL_CANDIDATE_FINDER_v1.0

Core flow:

MRI Issue
→ Search Concepts
→ Broad ZeroIn Candidate Retrieval
→ Candidate Relevance Assessment
→ Confirmed Relevant Product Set
→ AUM / Flow / New Launch Analysis

Important:

Fund Name Match ≠ Theme Confirmation

PENSION_YN ≠ Senior Theme Confirmation

Unknown Metadata ≠ Irrelevant

Candidate status:

- RELEVANT
- POSSIBLY_RELEVANT
- NOT_RELEVANT

POSSIBLY_RELEVANT cannot be used as definitive market evidence.

---

# END
