#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""22차에서 드러난 두 구멍을 막는다. 어느 변형에든 얹는다.

① theme_hint 누수 — 06P
   A안은 06P 가 조사 질문 본문을 아래로 넘기지 못하게 막았다. 그건 됐다.
   그런데 같은 06P 가 `theme_hint` 를 **새로 만들어** 태스크 23건 전부에 붙였다.

       "theme_hint": "주식보상 2.3조원(전년 대비 3배 증가), RSU 도입률 0.6%(성장여력 충분)"

   앞문으로 막은 수치가 뒷문으로 들어갔다. 원인은 프롬프트의
   「Preserve IMMUTABLY」 목록이다. 그 목록에 theme_hint 가 있으니
   모델은 「이 칸은 반드시 있어야 한다」로 읽고 채웠다.
   05 가 주지 않은 칸을 06P 가 만들어 낸 것이다.

   이 구멍은 A 가 만든 것이 아니라 **기준선에 원래 있었다.** B·C·D 에도 있다.

② 장부와 결과의 불일치 — 조회 노드 전체
   22차에 06E(정책 담당)가 장부는 정직하게 2건이라 적고,
   결과 배열에는 21건 전부를 채웠다. 뉴스·제로인·협회통계까지.
   뒤 노드 넷이 그 배열을 그대로 복사했다.

   그래서 세는 규칙을 하나 건다 — 결과에 있는 task_id 는 장부에 있어야 한다.
   판단이 아니라 대조라서 우회하기 어렵다.

    python3 patch_leak_fix.py            # 모든 변형에 제자리 적용
    python3 patch_leak_fix.py <파일>      # 한 파일만
"""
import json, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))

TARGETS = ['MRI_Agent2_Research_Response_v2.json',
           'variant_A_2plus3.json', 'variant_B_prune.json', 'variant_C_all.json',
           'variant_D_raw.json', 'variant_D_on_B.json',
           'variant_D_report.json', 'variant_D_on_B_report.json', 'variant_report.json']

# ── ① 06P ────────────────────────────────────────────────
OLD_LIST = """- related_rq_ids
- theme_hint
- seed_theme
- discovery_mode"""
NEW_LIST = """- related_rq_ids
- discovery_mode"""

P_RULE = """

## 없는 칸을 만들지 않는다 — HARD RULE

위 목록은 **상류가 준 칸을 그대로 넘기라**는 뜻이지,
**그 칸을 채워 내라**는 뜻이 아니다. 상류가 주지 않은 칸은 없는 채로 넘긴다.

특히 다음 두 칸은 **어떤 경우에도 네가 만들지 않는다.**

    theme_hint · seed_theme

직전 실행에서 이 칸이 이렇게 채워졌다.

    "theme_hint": "주식보상 2.3조원(전년 대비 3배 증가), RSU 도입률 0.6%(성장여력 충분)"

**05 는 이 칸을 주지 않았다. 네가 이슈의 주제 목록에서 만들어 붙였다.**
그리고 그것이 조회 태스크 23건 전부에 실려 조회 담당 전원에게 전달됐다.

그 문장은 이슈 원문의 수치다. 조회 결과가 없을 때, 그 수치가 조회 결과 자리에 옮겨 적힌다.
**조회 담당이 이슈의 수치를 미리 알고 있으면 그것을 찾아낸 것처럼 적는다.**

조회 태스크가 들고 가는 것은 이것뿐이다 —
`task_id` · `source` · `search_mode` · `query_terms` · `target` · `related_rq_ids` ·
`depends_on` · `result_limit_hint` · `discovery_mode` · `allows_emergent_theme`

`query_terms` 와 `target` 에도 **이슈 원문의 수치를 새로 끼워 넣지 않는다.**
05 가 적어 보낸 그대로만 넘긴다. 무엇을 찾는지는 적되, 답이 무엇인지는 적지 않는다.
"""

# ── ② 조회 노드 ──────────────────────────────────────────
R_RULE = """

## 장부에 없는 결과를 내지 않는다 — HARD RULE

네가 결과 배열에 더한 레코드의 `task_id` 는 **전부 `executed_task_ids` 안에 있어야 한다.**

내기 전에 대조한다. 판단이 아니라 세는 일이다.

1. 결과 배열에서 네가 더한 레코드의 `task_id` 를 모은다.
2. `executed_task_ids` 와 맞춰 본다.
3. **장부에 없는 task_id 의 레코드는 지운다.** 예외가 없다.

직전 실행에서 정책 담당이 장부에는 정직하게 두 건을 적고,
결과 배열에는 **스물한 건을 채웠다.** 뉴스·제로인·협회통계 결과까지 전부.
그리고 뒤 노드 넷이 그 배열을 글자 하나 바꾸지 않고 복사했다.

- 다른 소스의 태스크는 **네 도구로 부를 수 없다.** 부를 수 없으면 결과도 쓸 수 없다.
- 앞 노드가 남긴 배열에 다른 소스의 레코드가 들어 있어도 **네가 더한 것이 아니면 그대로 둔다.**
  받은 것은 옮기고, 만드는 것은 네 것만 만든다. 이 둘을 헷갈리지 않는다.
- 입력에 없던 레코드를 네가 만들었다면, 그 근거는 도구 출력이어야 한다.
  **도구를 부르지 않고 만든 레코드는 조회 결과가 아니다.**
"""


def patch(path):
    d = json.load(open(path, encoding='utf-8'))
    fm = d['MapValue']['FunctionMaps']
    hit_p = hit_r = 0

    for x in fm:
        col = x.get('COL_NAME') or ''
        p = x.get('prompt') or ''
        if col.startswith('06P') and 'theme_hint' in p and '없는 칸을 만들지 않는다' not in p:
            assert OLD_LIST in p, '06P 목록 형태가 다르다'
            x['prompt'] = p.replace(OLD_LIST, NEW_LIST, 1) + P_RULE
            hit_p += 1
        elif 'my_kb_tool' in p and '장부에 없는 결과를 내지 않는다' not in p:
            x['prompt'] = p + R_RULE
            hit_r += 1

    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"{os.path.basename(path):<32} 06P {hit_p} · 조회 노드 {hit_r}")


def main():
    files = sys.argv[1:] or [os.path.join(HERE, f) for f in TARGETS]
    for f in files:
        if os.path.exists(f):
            patch(f)


if __name__ == '__main__':
    main()
