# Regression Storage Policy

## Purpose

MRI regression cases may contain internal or confidential source material. The Git repository therefore does not require raw MRI documents or raw confidential regression inputs to be committed.

## Git may store
- synthetic regression cases
- de-identified regression cases
- regression criteria
- regression result summaries
- failure-mode descriptions
- rule changes derived from regression

## Git should not store unless explicitly approved
- raw internal MRI PDFs
- confidential internal CSV/Excel exports
- proprietary source documents
- internal customer or business data

## Raw case storage

Raw confidential cases should be kept in an approved internal storage location. The exact storage location is environment-specific and must not be invented here until formally decided.

## Reproducibility record

For each regression result recorded in Git, preserve at least:
- case ID
- scenario description
- expected behavior
- observed failure or pass
- abstract rule tested
- prompt/schema/runtime version
- date
- whether the case is synthetic, de-identified, or confidential-external

## Holdout rule

Cases used to improve the prompt are no longer unseen holdouts.

Do not label generalization as verified unless a genuinely unseen case set passes.
