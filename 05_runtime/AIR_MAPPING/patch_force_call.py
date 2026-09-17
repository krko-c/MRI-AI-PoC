#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⑯ 도구 호출 복원 — 23차에서 확인된 현상에 대응한다.

23차 플레이그라운드 로그에 `Calling tool:` 줄이 **하나도 없었다.**
조회 노드 여섯 개가 전부 KB 도구를 부르지 않고 답을 썼다.
첫 조회 노드도 부르지 않았다. NO_RESULT 조차 조회한 결과가 아니었다.

KB 도구를 단독으로 부르면 정상 동작한다. 워크플로 안에서만 부르지 않는다.

17차 로그에는 `Calling tool:` 줄이 있었다. 하류로 새어서 문제가 됐을 정도였다.
그 뒤 골격(build_prompts.py)으로 프롬프트를 189,093자 → 38,651자로 줄이면서 둘을 했다.

  1. 「반드시 도구를 불러라」고 말하는 섹션 아홉 개를 하나로 줄였다.
     「중복 20개를 버렸다」고 적은 그 부분이다.
  2. 「출력은 JSON 하나뿐이다 — HARD RULE」을 새로 넣었다. 18차 역할 이탈 대응이었다.
     그런데 이 문장은 「바로 JSON 을 써라」로 읽힌다.
     도구를 부르려면 출력을 멈추고 호출을 내야 하는데, 그것을 금지한 셈이다.

둘 다 골격화 때 함께 들어갔고, 그 뒤로 `Calling tool:` 을 본 기록이 없다.
**규칙을 더한 것이 아니라, 지운 것을 되돌린다.**

    python3 patch_force_call.py            # 모든 변형에 제자리 적용
    python3 patch_force_call.py <파일>      # 한 파일만
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGETS = ['MRI_Agent2_Research_Response_v2.json', 'variant_report.json',
           'variant_A_2plus3.json', 'variant_B_prune.json', 'variant_C_all.json',
           'variant_D_raw.json', 'variant_D_on_B.json',
           'variant_D_report.json', 'variant_D_on_B_report.json']

# ── ① 1장 — 이름을 적었으면 곧바로 부른다 ────────────────
OLD_1 = """이 칸을 채우려면 네 도구 목록을 봐야 한다. 그것이 이 칸의 목적이다.
대화에 보이는 도구 이름은 전부 네 것이 아니다. 앞 노드가 쓴 이름을 옮기지 않는다.
여기 적은 이름과 실제로 부른 이름이 다르면 그 차례는 실패다."""

NEW_1 = """이 칸을 채우려면 네 도구 목록을 봐야 한다. 그것이 이 칸의 목적이다.
대화에 보이는 도구 이름은 전부 네 것이 아니다. 앞 노드가 쓴 이름을 옮기지 않는다.
여기 적은 이름과 실제로 부른 이름이 다르면 그 차례는 실패다.

**이름을 적는 것과 부르는 것은 다른 일이다.** 이름을 적었으면 곧바로 그 도구를 부른다.
직전 실행에서 아홉 개 노드가 이 칸을 정확히 채우고 **한 번도 부르지 않았다.**
이름만 맞히는 것은 이 칸의 목적이 아니다."""

# ── ② 2장 앞 — 출력 전에 부른다 ──────────────────────────
ANCHOR_2 = '## 2. 먼저 세고, 센 만큼 부른다 — HARD RULE'

SEC_CALL = """## 2. 도구를 부르지 않고는 아무것도 낼 수 없다 — HARD RULE

**출력을 시작하기 전에 도구를 부른다.** 이것이 네 차례의 첫 행동이다.

순서는 하나뿐이다.

    도구를 부른다  →  돌아온 것을 받는다  →  그것으로 JSON 을 쓴다

이 순서를 뒤집을 수 없다. **부르기 전에는 쓸 내용이 없기 때문이다.**

직전 실행에서 조회 노드 전원이 도구를 부르지 않고 결과를 썼다.
자료원에 없는 상품명을 적었고, 당사 상품을 물었는데 **다른 회사 브랜드**를 적었다.
자료원을 봤다면 나올 수 없는 답이다. **부르지 않고 쓰면 반드시 그렇게 된다.**

- 네가 아는 것으로 답하지 않는다. **너는 이 자료원의 내용을 모른다.** 도구만 안다.
- 답이 뻔해 보여도 부른다. 뻔해 보이는 것이 네 기억이고, 기억은 이 자료원이 아니다.
- 자료가 없을 것 같아도 부른다. **없다는 것도 불러 봐야 아는 것이다.**
  부르지 않고 쓴 「자료없음」은 확인이 아니라 추측이다.
- 부르지 않았으면 그 태스크는 `executed_task_ids` 에 넣을 수 없다.

"""

# ── ③ 5장 — 순서를 제목에 박는다 ─────────────────────────
OLD_5H = """## 5. 출력은 JSON 하나뿐이다 — HARD RULE

- 닫힌 JSON 객체 하나만 낸다."""

NEW_5H = """## 5. 도구를 다 부른 다음, JSON 하나를 낸다 — HARD RULE

**이 절은 무엇을 낼지에 대한 것이지, 언제 시작할지에 대한 것이 아니다.**
도구 호출이 끝난 뒤에 이 절이 적용된다. 먼저 부르고, 그 다음 아래대로 낸다.
「JSON 하나만」이라는 말을 **「바로 JSON 부터 쓰라」로 읽지 않는다.**

- 닫힌 JSON 객체 하나만 낸다."""


def renumber(p):
    """섹션을 새로 끼웠으니 번호를 다시 매긴다. 번호 없는 절(⑮)은 건드리지 않는다."""
    n = [0]
    def repl(m):
        n[0] += 1
        return f"## {n[0]}. {m.group(2)}"
    return re.sub(r'^## (\d+)\. (.*)$', repl, p, flags=re.M)


def patch(path):
    d = json.load(open(path, encoding='utf-8'))
    hit = 0
    for x in d['MapValue']['FunctionMaps']:
        p = x.get('prompt') or ''
        if 'my_kb_tool' not in p or '도구를 부르지 않고는' in p:
            continue
        assert OLD_1 in p and ANCHOR_2 in p and OLD_5H in p, x.get('COL_NAME')
        p = p.replace(OLD_1, NEW_1, 1)
        p = p.replace(ANCHOR_2, SEC_CALL + ANCHOR_2.replace('## 2.', '## 3.'), 1)
        p = p.replace(OLD_5H, NEW_5H, 1)
        x['prompt'] = renumber(p)
        hit += 1
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"{os.path.basename(path):<36} 조회 노드 {hit}개")


def main():
    for f in (sys.argv[1:] or [os.path.join(HERE, t) for t in TARGETS]):
        if os.path.exists(f):
            patch(f)


if __name__ == '__main__':
    main()
