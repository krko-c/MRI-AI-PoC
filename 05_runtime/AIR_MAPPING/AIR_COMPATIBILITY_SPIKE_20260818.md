# AIR Compatibility Spike — 2026-08-18

## 1. Compatibility Gates

### GATE 1 — Full MRI Input
**PASS with limitation**
- PDF → KB ingestion 가능
- 한글 parse 가능
- CURRENT_MRI 전체 #1~#7 recall 가능
- page provenance는 `Unknown`

### GATE 2 — Agent → Agent Context
**PASS with warning**
- 후속 Agent가 앞 Agent 결과 문맥을 읽음
- immutable typed object transfer가 아님
- exact JSON/value preservation 보장 안 됨

### GATE 3 — Conditional Routing
**PASS with warning**
- Contains 기반 routing 동작
- whole-output search / validator warning 존재

### GATE 4A — Agent → Knowledge Base
**PASS**
- `kb-6b0fd700` 실제 호출
- CURRENT_MRI 조회 및 downstream 전달 가능

### GATE 4B — Agent → Tool
**PASS**
- input injection / execution / output / downstream 전달 확인

### GATE 5 — Export → Import → Run
**PASS in current AIR environment**
- graph/FLOW/Tool/KB/Conditional/final downstream 복원 확인
- Tool은 `tool_id`, KB는 `index_name` reference 형태
- cross-environment standalone portability **UNVERIFIED**

---

## 2. Operational CURRENT_MRI Transfer Test
CURRENT_MRI #4의 특정 #3 제목이 KB → Agent → Router → Conditional → Final 경로에서 유지됨.

---

## 3. 01→02→03 Runtime Experiments

### 17:50 직렬 FLOW
```text
Supervisor → 01 → 02 → 03
```
- 01 KB 호출 및 #1~#7 retrieval: PASS
- 02가 Stage 01 재수행: FAIL
- 03이 Stage 02 수행: FAIL
- stage ownership / role compliance: FAIL

### Marker-based Stage Contract
- stage 밀림 일부 개선
- marker가 downstream prompt/context 자체에 존재할 수 있어 robust contract로 부적절
- 최종 방식으로 채택하지 않음

### 18:52 Cumulative Payload
좋았던 점:
- `sections.issue_extraction` 등 구조화 가능

실패:
- 01 Agent가 사용자 전체 요청을 따라 Fidelity + Screening까지 스스로 생성
- 01 종료 후 실제 02가 다시 호출됨

결론:
**Payload continuity와 orchestration control은 별도 문제다.**

---

## 4. AIR Sample JSON 재검토 결론
사용자 제공 sample은 Supervisor가 전문 Agent를 직접 호출하고, 결과 수신 여부와 순서를 Supervisor가 통제하는 패턴이 확인됨.

우선 검증 후보:
```text
             → 01_mri_issue_extraction_agent
            /
Supervisor ─→ 02_source_fidelity_validator
            \
             → 03_mri_screening_agent
```

---

## 5. v4 Status
파일: `MRI_01_02_03_v4_SUPERVISOR_ORCHESTRATED.json`

상태:
- generated
- runtime test **PENDING**

PASS로 기록하지 않는다.

### Exit Criteria
1. Supervisor → 01
2. 01 result 수신 후 Supervisor → 02
3. 02 result 수신 후 Supervisor → 03
4. 각 Agent stage ownership 유지
5. 03 5-Lens screening 수행
6. prior sections 유지

---

## 6. Prompt / Regression Findings

### Fidelity
원문 제목의 `대응/점검/진단` 자체를 recommendation leakage로 오판하지 않음.

### Screening Directness
`산업 성장 → 관련 기업 추정 → ETF 가능`은 external investable-universe 검증 전 최대 1점.

### Unsupported Named Entities
MRI/KB에 없는 실제 기업명/상품명을 Screening 2점 근거로 새로 생성 금지.

### Asset Manager Role Boundary
증권사 랩/ISA 계좌 자체, 예금/대출/보험 등은 AM direct product로 취급하지 않음.

---

## 7. Known Limitations
- CURRENT_MRI page provenance unavailable
- Agent context not immutable
- stage ownership orchestration-sensitive
- JSON-only strictness imperfect
- Conditional whole-output Contains
- Export JSON dependency references
- cross-environment portability unverified
- Generalization NOT VERIFIED

## 8. Development Consequence
전체 Logical Architecture는 유지한다.
변경되는 것은 개발 방식이다.

1. Logical Step 설계
2. Prompt/Schema/Regression
3. AIR 최소 Physical Implementation
4. Runtime 문제가 있으면 Agent 수/Topology/Schema 조정
5. Logical Step 하나를 Agent 하나로 미리 고정하지 않음
