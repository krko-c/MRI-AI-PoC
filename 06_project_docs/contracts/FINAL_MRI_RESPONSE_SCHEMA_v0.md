# Final MRI Response Schema v0

_Status: PROVISIONAL — Thin End-to-End endpoint_

## 1. Purpose

This is the **structured content contract** for one issue-level MRI response draft.

It is not yet the final formal submission layout.

Its purpose is to give the Thin End-to-End test a concrete endpoint so upstream contracts can be evaluated by actual downstream usefulness.

## 2. Design Principles

- complete enough for the analyst to use directly in the MRI response,
- distinguish source fact / internal fact / department input / AI inference,
- preserve `UNKNOWN != ABSENCE`,
- keep evidence references visible,
- avoid forcing internal analytical detail into the final prose when it adds no value,
- permit concise output when evidence is thin.

## 3. Top-Level Schema

```json
{
  "topic_id": "S03",
  "analysis_as_of_date": "YYYY-MM-DD",
  "issue": {},
  "market_competitor_status": {},
  "company_current_state": {},
  "business_opportunity": {},
  "gap": {},
  "response_strategy": {},
  "department_input": {},
  "constraints_unknowns": [],
  "evidence_summary": [],
  "overall_verification_status": "VERIFIED | PARTIALLY_VERIFIED | INSUFFICIENT_EVIDENCE",
  "draft_response": {
    "current_status": "...",
    "response_direction_and_plan": "..."
  }
}
```

## 4. Issue

```json
{
  "issue_title": "...",
  "issue_summary": "...",
  "mri_implication": "..."
}
```

Purpose:
state what the MRI actually raises and why it matters to an asset manager.

Do not add strategy here.

## 5. Market / Competitor Status

```json
{
  "summary": "...",
  "key_findings": [
    {
      "claim": "...",
      "status": "CONFIRMED | PARTIALLY_CONFIRMED | UNVERIFIED",
      "source_class": "EXTERNAL_MARKET | EXTERNAL_COMPETITOR | EXTERNAL_POLICY",
      "evidence_ids": ["EV-001"]
    }
  ]
}
```

This section may include:
- market structure / flow,
- competitor / peer response,
- product supply / launch,
- financial-group response,
- policy / industry changes.

## 6. Company Current State

```json
{
  "summary": "...",
  "state_items": [
    {
      "claim": "...",
      "status": "CONFIRMED_PRESENT | CONFIRMED_ABSENT | NOT_FOUND | UNKNOWN",
      "source_class": "INTERNAL_SYSTEM | INTERNAL_DOCUMENT",
      "evidence_ids": ["IE-001"]
    }
  ],
  "search_coverage": {
    "product_data": "SEARCHED | NOT_SEARCHED | NOT_AVAILABLE",
    "historical_mri": "SEARCHED | NOT_SEARCHED | NOT_AVAILABLE",
    "internal_documents": "SEARCHED | NOT_SEARCHED | NOT_AVAILABLE"
  }
}
```

## 7. Business Opportunity

This is the **validated / current BO view**, not every internal BO working field.

```json
{
  "opportunity_id": "BO-01",
  "hypothesis": "...",
  "validation_status": "SUPPORTED | PARTIALLY_SUPPORTED | NOT_SUPPORTED | INSUFFICIENT_EVIDENCE",
  "why_it_matters": "...",
  "remaining_key_assumptions": ["..."],
  "evidence_ids": ["EV-001", "EV-002"]
}
```

The Thin E2E will determine whether internal fields such as `hypothesis_chain` need to appear here.

## 8. Gap

```json
{
  "gap_status": "MATERIAL_GAP | PARTIAL_GAP | NO_MATERIAL_GAP | INSUFFICIENT_EVIDENCE",
  "gap_statement": "...",
  "basis": ["..."]
}
```

Gap compares the validated opportunity / market situation with the company's current state.

## 9. Response Strategy

```json
{
  "recommended_direction": "...",
  "actions": [
    {
      "action": "...",
      "time_horizon": "CURRENT | NEAR_TERM | MEDIUM_TERM | TBD",
      "dependency_or_constraint": "..."
    }
  ]
}
```

This is the AI / analyst's own response logic.

It is not required to copy Department proposals.

## 10. Department Input

```json
{
  "response_status": "RECEIVED | PENDING | NOT_REQUIRED",
  "items": [
    {
      "department": "...",
      "input_type": "DEPARTMENT_FACT | DEPARTMENT_PROPOSAL",
      "statement": "...",
      "evidence_id": "DEPT-001"
    }
  ]
}
```

If responses have not arrived, this section can remain PENDING while the AI research continues.

## 11. Constraints / Unknowns

Each material unresolved point:

```json
{
  "unknown_id": "UNK-01",
  "statement": "...",
  "why_it_matters": "...",
  "resolution_needed": "..."
}
```

Do not convert `NOT_FOUND` into confirmed absence.

## 12. Evidence Summary

```json
{
  "evidence_id": "EV-001",
  "source_class": "EXTERNAL_MARKET",
  "source_name": "...",
  "as_of_date": "YYYY-MM-DD",
  "claim_supported": "...",
  "verification_status": "CONFIRMED | PARTIAL | UNVERIFIED"
}
```

The actual evidence store may contain richer provenance than this final view.

## 13. Draft Response

The AI should finish with usable MRI prose:

```json
{
  "current_status": "...",
  "response_direction_and_plan": "..."
}
```

This is intentionally concise and should be derived from the structured sections above.

## 14. Thin E2E Evaluation Questions

After H02 is completed, ask:

1. Which BO internal fields were needed to write this response?
2. Which BO fields were never used?
3. Which market-intel findings mattered?
4. Which Company State fields mattered?
5. Where did absence / unknown status affect wording?
6. Which evidence questions duplicated between Opportunity and Market Intel?
7. What could not be written because data was missing?
8. Was the final `draft_response` sufficiently complete for actual MRI work?
9. Which content should remain internal-only rather than appear in the final response?
10. What must change before this schema becomes v1?
