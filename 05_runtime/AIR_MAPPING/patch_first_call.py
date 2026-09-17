#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⑰ 첫 호출을 조건 없는 것으로 되돌린다 — 골격화 때 지운 장치의 복원.

16·17·21차에는 조회가 됐다. 17차 로그에는 `Calling tool:` 줄이 하류로 샐 만큼 많았다.
22·23·24차에는 한 줄도 없다. 그 사이에 있었던 일은 하나다 —
10e8f94 「조회 노드 9개 프롬프트 재작성 — 189,093자 -> 38,651자」.

그 커밋이 지운 것 중 호출을 붙들고 있던 장치가 셋이다.

  1. 「배정 태스크 전에 한 번 넓게 부른다」
     조건 없는 첫 호출. 커밋 메시지에 「호출수를 1+N으로 만들어 대조 도구를 흐렸다」고
     적고 지웠다. 그때 문제는 호출수 집계였고, 지금 문제는 호출 0이다.
  2. `retrieval_proof` / `RETRIEVAL_NOT_EXECUTED`
     부르지 않은 것을 SUCCESS 로 못 내게 막던 상태값. ②로 적고 지웠다.
  3. 「실행은 말이 아니라 호출이다」
     `execution_note` 같은 의도 필드 금지 + 출력 직전 마지막 점검.

⑯은 「부르라」는 말을 되살렸다. 24차에도 안 불렀다.
말을 더해서 될 일이 아니다. **판단이 들어갈 자리를 없앤다.**
첫 호출에서 「부를까 말까」를 묻지 않게 하는 것이 ⑰이다.

되돌리는 것은 이 셋뿐이다. 189,093자로 돌아가지 않는다.
⑫(출처미상) · ⑮(장부 대조) · ⑯(호출 복원) · 점검 블록은 그대로 둔다.
21차 판은 조회는 됐지만 13건 중 8건이 날조였다. 그 통제를 버리지 않는다.

    python3 patch_first_call.py            # variant_report.json -> variant_report_call.json
    python3 patch_first_call.py <입력> <출력>
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ── ① 조건 없는 첫 호출 ─────────────────────────────────
ANCHOR = '## 3. 먼저 세고, 센 만큼 부른다 — HARD RULE'

SEC_FIRST = """## 3. 태스크를 보기 전에 한 번 부른다 — HARD RULE

**네 첫 호출에는 조건이 없다.** 태스크를 세기 전에, 무엇을 물을지 고르기 전에,
네 KB 를 한 번 넓게 부른다. 질의어는 태스크의 좁은 검색어가 아니라
이 이슈의 핵심 주제어(`must_preserve_themes` 의 단어들)를 쓴다.

이 호출에는 「부를까 말까」의 판단이 없다. **판단이 들어가면 부르지 않게 된다.**
직전 두 실행에서 조회 노드 전원이 부르기 전에 「부를 필요가 없다」는 결론에 먼저 닿았고,
그래서 한 번도 부르지 않았다. 그 결론에 닿을 기회 자체를 없앤다.

- `matched_task_count` 가 0이어도 이 호출은 한다. 센 다음이 아니라 **세기 전이다.**
- 이 호출은 태스크당 1회 제한과 별개다. **넓은 조회 1회 + 태스크 수만큼.**
- 태스크 검색어로만 물으면 KB 에 있는 다른 자료가 안 보인다.

그 `answer` 에서 **이번 태스크들이 겨냥하지 않은 내용**을 옮겨 적는다.

    "kb_other_points": [
      {"point": "<`answer` 에서 그대로 복사한 문장>", "source_footer": "<꼬리 줄 또는 \\"\\">"}
    ]

- 파일명이 아니라 **문장**이다. 도구가 실제로 돌려준 글에서만 나온다.
- **네가 부르지 않은 답변을 여기 담지 않는다.** 대화에 남아 있는 다른 노드의
  조회 결과는 네 것이 아니다. 이 칸은 **네 도구가 네 질의에 답하면서 딸려 온 것**만 들어간다.
- 쓸지 말지는 네가 아니라 07 이 정한다. 없으면 빈 배열이다.
- 다른 노드가 넣은 항목을 지우거나 고치지 않는다.

7차 실행에서 정책 KB 안에 디폴트옵션 53.3조원·734만명이 들어 있었는데 보고서에 실리지 않았다.
계획이 그 KB 를 빗나가게 물었기 때문이다. **먼저 넓게 부르면 이런 일이 없다.**

## 4. 실행은 말이 아니라 호출이다 — HARD RULE

**「실행합니다」는 실행이 아니다.** 「순차 실행합니다」·「진행합니다」·
「모든 태스크를 완료할 때까지 실행을 계속합니다」도 마찬가지다.
실행은 `Calling tool:` 한 줄이다. 그 줄이 없으면 아무 일도 일어나지 않았다.

이전 실행에서 뉴스 후속 노드가 이렇게 무너졌다.

    "matched_task_count": 13,
    "matched_tasks": [ …13개를 정확히 나열… ],
    "execution_note": "…13개 태스크를 순차 실행합니다. …
                       모든 태스크를 완료할 때까지 실행을 계속합니다."
    "followup_results": []          ← 도구 호출 0회. 차례 종료.

**태스크를 정확히 세고, 정확히 나열하고, 실행하겠다고 쓰고, 부르지 않았다.**
13개 태스크가 그대로 죽었고 뒤 노드들은 전부 미실행을 복창했다.

그래서 셋을 금지한다.

**1) 의도를 적는 필드를 만들지 않는다.**
`execution_note` · `plan` · `next_step` 처럼 「이제 무엇을 하겠다」를 적는 칸을
출력에 만들지 않는다. 그 칸은 하지 않은 일을 한 것처럼 보이게 하는 서식이다.
할 일이 있으면 적지 말고 부른다.

**2) `stage_status` 에 시작을 적지 않는다.**
`EXECUTION_STARTED` 는 쓰지 않는다. **시작은 상태가 아니다.**
네 차례가 끝나는 순간 실행은 끝났거나 안 한 것이고, 그 둘뿐이다.

**3) 부르지 않고 차례를 끝내지 않는다 — 마지막 점검.**
출력을 내기 직전에 확인한다.

    이번 차례에 도구를 한 번도 부르지 않았다
    → 그 차례는 실패다. 출력하지 말고 지금 부른다.

"""

# ── ② 0건이어도 첫 호출은 한다 ──────────────────────────
OLD_ZERO = """`matched_task_count == 0` 이면 여기서 끝이다. 도구를 부르지 않고,
받은 JSON 에 `"stage_status": "NO_APPLICABLE_TASK"` 만 더해 그대로 돌려준다."""

NEW_ZERO = """`matched_task_count == 0` 이면 태스크별 호출은 없다. 위 첫 호출은 이미 했으므로
그 `kb_other_points` 를 담고, 받은 JSON 에 `"stage_status": "NO_APPLICABLE_TASK"` 를
더해 돌려준다."""

# ── ③ 부르지 않은 것을 완수로 내지 못하게 ───────────────
OLD_NOEXEC = """`unresolved_retrieval_needs` 는 **부른 뒤 실패한** 태스크 자리다."""

NEW_NOEXEC = """부르지 않았으면 쓸 수 있는 상태는 하나뿐이다.

    "status": "RETRIEVAL_NOT_EXECUTED",
    "records": [],
    "error_detail": "배정된 태스크였으나 KB 도구를 부르지 않았다."

이것을 `NO_RESULT` 나 `SUCCESS` 로 바꾸지 않는다. **바꾸면 그 자리가 영영 안 보인다.**
반대로 실제로 부른 결과에는 레코드마다 이 칸을 단다.

    "retrieval_proof": {"kb_tool_called": true, "source_id": "<네 소스 ID>"}

이 칸은 **불렀다는 사실의 기록이지 정확하다는 보증이 아니다.**
부르지 않고 이 칸을 `true` 로 적는 것이 이 워크플로에서 가장 나쁜 한 줄이다.

`unresolved_retrieval_needs` 는 **부른 뒤 실패한** 태스크 자리다."""

# ── ④ 10번 노드 — 점수를 축 이름에 맞춰 옮긴다 ──────────
OLD_AXIS = """- 오른쪽 칸에는 **근거 번호만** 쓴다. 설명을 쓰지 않는다.
  근거가 없으면 `없음` 이라고만 쓴다. **말로 메우지 않는다.**"""

NEW_AXIS = """- 오른쪽 칸에는 **근거 번호만** 쓴다. 설명을 쓰지 않는다.
  근거가 없으면 `없음` 이라고만 쓴다. **말로 메우지 않는다.**
- **점수는 축 이름에 붙은 값을 그대로 옮긴다.** 위 나열은 표기 순서일 뿐이다.
  인계 자료에서 축 이름을 찾아 그 값을 쓴다. 순서대로 값만 끌어다 쓰지 않는다.
  직전 실행에서 채널 1점이 0으로, 투자테마 0점이 1로 실렸다. 값이 한 칸 밀린 것이다."""


def renumber(p):
    n = [0]
    def repl(m):
        n[0] += 1
        return f"## {n[0]}. {m.group(2)}"
    return re.sub(r'^## (\d+)\. (.*)$', repl, p, flags=re.M)


def patch(src, dst):
    d = json.load(open(src, encoding='utf-8'))
    ret = axis = 0
    for x in d['MapValue']['FunctionMaps']:
        p = x.get('prompt') or ''
        if 'my_kb_tool' in p and '태스크를 보기 전에 한 번 부른다' not in p:
            assert ANCHOR in p and OLD_ZERO in p and OLD_NOEXEC in p, x.get('COL_NAME')
            p = p.replace(ANCHOR, SEC_FIRST + ANCHOR.replace('## 3.', '## 5.'), 1)
            p = p.replace(OLD_ZERO, NEW_ZERO, 1)
            p = p.replace(OLD_NOEXEC, NEW_NOEXEC, 1)
            x['prompt'] = renumber(p)
            ret += 1
        elif OLD_AXIS in p:
            x['prompt'] = p.replace(OLD_AXIS, NEW_AXIS, 1)
            axis += 1
    json.dump(d, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"{os.path.basename(dst):<30} 조회 노드 {ret}개 · 축순서 {axis}개")


if __name__ == '__main__':
    a = sys.argv[1:]
    patch(a[0] if a else os.path.join(HERE, 'variant_report.json'),
          a[1] if len(a) > 1 else os.path.join(HERE, 'variant_report_call.json'))
