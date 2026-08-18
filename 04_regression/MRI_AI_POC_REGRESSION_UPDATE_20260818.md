# MRI AI PoC Regression Update — 2026-08-18

## R-20260818-01 Stage Ownership Drift
Failure:
- Fidelity Agent가 Extraction 수행
- Screening Agent가 Fidelity 수행
- 또는 Extraction Agent가 Fidelity + Screening까지 선행 수행

Root cause category: orchestration / context ownership

Required rule:
- Supervisor/Schema/process gate 우선
- downstream Agent가 missing prior stage를 재구축하지 않음

Status: **OPEN — v4 runtime validation pending**

---

## R-20260818-02 Source Title Leakage False Positive
원문 제목의 `대응/점검/진단` 자체를 recommendation leakage로 판정하지 않는다.

Status: **RULE ADDED / runtime regression pending**

---

## R-20260818-03 Growth Industry → ETF Overreach
다음 구조는 최대 1점:
```text
growth industry
→ assume listed beneficiaries
→ assume investable universe
→ ETF/fund possible
```

Status: **RULE ADDED / runtime regression pending**

---

## R-20260818-04 Unsupported Named Entity Injection
External validation 전 실제 기업명/경쟁상품명/시장규모를 새 evidence처럼 만들지 않는다.

Status: **RULE ADDED / runtime regression pending**

---

## R-20260818-05 Asset Manager Role Leakage
Bank/securities native service를 AM direct product lens 근거로 사용하지 않는다.

Direct AM 예:
- fund
- ETF
- private fund
- FoF / allocation
- TDF/TIF
- OCIO / discretionary management
- portfolio solution

Status: **RULE ADDED / runtime regression pending**

---

## R-20260818-06 Cumulative Payload Is Not Sufficient Contract
`metadata.current_agent + sections` 구조는 유용하지만 그 자체로 stage ownership을 보장하지 않는다.

Status: **ACCEPTED DEVELOPMENT RULE**

---

## 01→03 Regression Acceptance Criteria
1. #1~#N top-level issue count/order 유지
2. Extraction에 business/strategy field 없음
3. Fidelity가 외부 reality verification을 주장하지 않음
4. Source title의 대응/점검/진단을 leakage로 오판하지 않음
5. Screening 5 Lens 모두 존재
6. total score 없음
7. 분류 규칙 일치
8. external validation 필요 성장테마를 자동 2점 처리하지 않음
9. unsupported real-world named entities 없음
10. bank/securities native product를 AM direct product로 오인하지 않음
11. prior/next stage ownership 침범 없음

Generalization은 별도 unseen regression 없이는 VERIFIED로 기록하지 않는다.
