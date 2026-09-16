#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D안 — 조회 노드를 「검색기」로 격하한 변형 JSON 을 만든다.

지금까지 날조가 나온 자리는 늘 같았다. **조회 노드가 도구 출력에서 사실을 뽑는 칸.**
`fact` · `answer_excerpt` 를 채우는 순간 노드는 「쓰는 일」을 하게 되고,
도구가 답을 안 줬을 때도 그 칸은 비지 않았다. 앞 노드의 출력이 본보기로 남아 있어서다.

D안은 그 칸을 없앤다.

  조회 노드 9개  도구 출력 `answer` 를 통째로 `raw_answer` 에 옮겨 담기만 한다.
                 사실을 뽑지 않는다. 고르지 않는다. 판단하지 않는다.
  07             근거를 만들 때 인용문이 어느 `raw_answer` 안에 실제로 있는지 대조한다.
                 못 찾으면 그 근거는 조회 근거가 아니다.

부수 효과가 하나 더 있다. `kb_other_points` 가 필요 없어진다.
배정 태스크가 빗나가게 물었어도 KB 가 돌려준 진짜 자료는 `raw_answer` 안에 그대로 있고,
그것을 쓸지는 07 이 정한다. (7차에 정책 KB 의 디폴트옵션 자료를 아무도 읽지 않았던 경로다.)

대가는 분량이다. 23태스크 × 도구 출력 전문이 07 까지 흘러간다.
그래서 B안(가지치기)과 겹쳐 쓰는 판을 같이 낸다.

    python3 make_variant_d.py
      -> variant_D_raw.json    기준선 + D
      -> variant_D_on_B.json   B(가지치기) + D
"""
import json, os, sys
import build_prompts as B

HERE = os.path.dirname(os.path.abspath(__file__))


def nodes_by_prefix(d, pre):
    return [x for x in d['MapValue']['FunctionMaps']
            if (x.get('COL_NAME') or '').startswith(pre)]


# ══════════════════════════════════════════════════════════
# 1) 조회 노드 — 골격을 raw 모드로 다시 찍는다
# ══════════════════════════════════════════════════════════
def patch_retrieval(d):
    hit = 0
    for x in d['MapValue']['FunctionMaps']:
        col = x.get('COL_NAME') or ''
        key = col.split()[0] if col else ''
        if key not in B.NODES:
            continue
        if 'my_kb_tool' not in (x.get('prompt') or ''):
            continue
        p = B.build(key, raw=True)
        assert 'raw_answer' in p and 'answer_excerpt' in p  # 후자는 "만들지 않는다" 목록
        x['prompt'] = p
        hit += 1
    return hit


# ══════════════════════════════════════════════════════════
# 2) 수집 노드 — raw_answer 를 줄이지 않는다
# ══════════════════════════════════════════════════════════
OLD_COLLECT = """레코드의 `answer_excerpt` 와 `source_footer` 도 **글자 하나 바꾸지 않고** 넘긴다.
둘 다 조회 노드가 도구 출력에서 옮겨 적은 값이고, 이 워크플로가 출처를 확인하는 유일한 근거다.
`source_footer` 가 `""` 인 레코드를 버리거나 경로를 채워 넣지 않는다."""

NEW_COLLECT = """레코드의 `raw_answer` 와 `source_footer` 는 **글자 하나 바꾸지 않고** 넘긴다.
`raw_answer` 는 KB 도구가 돌려준 글 전문이다. 이 워크플로가 조회를 확인하는 유일한 근거다.

- **요약하지 않는다. 자르지 않는다. 합치지 않는다.** 길다고 줄이면 그만큼 근거가 사라진다.
- 여러 레코드의 `raw_answer` 를 하나로 붙이지 않는다. 레코드 하나가 호출 하나다.
- `raw_answer` 에서 사실을 뽑아 `fact` · `summary` 같은 칸을 **여기서 만들지 않는다.**
  그 일은 07 이 하고, 07 은 `raw_answer` 안에 있는 문장만 쓸 수 있다.
- `source_footer` 가 `""` 인 레코드를 버리거나 경로를 채워 넣지 않는다.

분량 때문에 무엇을 줄여야 한다면 `collector_note` 를 줄인다. `raw_answer` 는 마지막까지 남긴다."""


def patch_collectors(d):
    hit = 0
    for x in d['MapValue']['FunctionMaps']:
        p = x.get('prompt') or ''
        if OLD_COLLECT in p:
            x['prompt'] = p.replace(OLD_COLLECT, NEW_COLLECT)
            hit += 1
    return hit


# ══════════════════════════════════════════════════════════
# 3) 07 — 인용문을 raw_answer 에 대조한다
# ══════════════════════════════════════════════════════════
OLD_Q = "**`verbatim_quotes`** — 레코드의 `answer_excerpt` 를 **그대로** 옮긴다. 1–2개."
NEW_Q = "**`verbatim_quotes`** — 레코드의 `raw_answer` 안에 **실제로 있는 문장**을 그대로 잘라 온다. 1–2개."

ANCHOR = "추론의 출발점이 된 사실의 인용을 넣는다."

D_SECTION = """

## 인용은 `raw_answer` 안에서만 나온다 — HARD RULE

이 판에서 조회 노드는 사실을 뽑지 않는다. **도구가 돌려준 글을 통째로 `raw_answer` 에 담아 온다.**
사실을 뽑는 일은 여기, 07 이 한다. 그래서 규칙이 하나 생긴다.

**네가 쓰는 모든 인용문은 어느 레코드의 `raw_answer` 안에 글자 그대로 있어야 한다.**

근거마다 두 칸을 더 채운다.

    "quote_source_task_id": "<인용문이 나온 레코드의 task_id>",
    "quote_verified_in_raw": true

절차는 셋뿐이다.

1. 쓰려는 사실이 어느 `raw_answer` 에 있는지 찾는다.
2. 그 문장을 **복사해** `verbatim_quotes` 에 넣는다. 다듬지 않는다. 숫자·기간·단위를 바꾸지 않는다.
3. 그 레코드의 `task_id` 를 `quote_source_task_id` 에 적는다.

**어느 `raw_answer` 에서도 그 문장을 찾지 못하면 그 근거는 조회 근거가 아니다.**
- MRI 원문에 있으면 「MRI 원문을 근거로 쓰는 길」 규칙대로 `PARTIAL` 로 싣는다.
- MRI 원문에도 없으면 **그 근거를 만들지 않는다.** `data_gaps` 에 적는다.
- `VERIFIED` 는 `quote_verified_in_raw: true` 인 근거에만 붙는다. 예외가 없다.

기억으로 문장을 복원하지 않는다. 「대충 이런 내용이었다」로 인용을 쓰지 않는다.
**찾아서 복사하는 것과 떠올려 적는 것은 다른 일이다. 찾아서 복사한다.**

## 태스크가 겨냥하지 않은 자료 — `raw_answer` 가 이미 담고 있다

이 판에는 `kb_other_points` 가 따로 오지 않는다. 필요가 없어서다.
조회 노드가 도구 출력을 통째로 넘기므로, **배정 태스크가 빗나가게 물었어도
KB 가 실제로 돌려준 자료는 `raw_answer` 안에 그대로 있다.**

그러니 `raw_answer` 를 태스크가 물은 것만 보고 읽지 않는다. **글 전체를 읽는다.**
- 이슈와 관련 있는 문장이 있으면 근거로 만든다. `supporting_task_ids` 는 그 레코드의 task_id 를 쓰고,
  `limitations` 에 "배정 태스크가 겨냥하지 않은 자료"라고 적는다.
- **당사(OWN_COMPANY) 회사명이 나오는 문장은 반드시 근거로 만든다.** 담당자가 가장 먼저 보는 칸이다.

7차 실행에서 정책 KB 의 디폴트옵션 자료가 이 경로로 들어왔어야 했다.
계획은 그 KB 에 상법을 물었고, 노드는 답을 지어냈고, **KB 안의 진짜 자료는 아무도 읽지 않았다.**
이 판에서는 그 자료가 `raw_answer` 안에 들어 있다. 읽는 것은 네 몫이다.

`kb_other_points` 가 들어오면 예전 형식이다. 그때는 종전 규칙대로 다룬다.
"""

OLD_SCHEMA = '      "verbatim_quotes":[],'
NEW_SCHEMA = ('      "verbatim_quotes":[],\n'
              '      "quote_source_task_id":null,\n'
              '      "quote_verified_in_raw":false,')

OLD_IN = "- kb_other_points — 조회 노드가 자기 KB 를 넓게 부른 뒤, 배정 태스크가 겨냥하지 않아 옮겨 적어 둔 문장"
NEW_IN = "- retrieval 레코드의 `raw_answer` — KB 도구가 돌려준 글 전문 (이 판의 유일한 조회 근거)"


def patch_07(d):
    n = nodes_by_prefix(d, '07 ')[0]
    p = n['prompt']
    for old, new in ((OLD_Q, NEW_Q), (OLD_IN, NEW_IN), (OLD_SCHEMA, NEW_SCHEMA)):
        assert old in p, old[:40]
        p = p.replace(old, new, 1)
    assert ANCHOR in p
    i = p.index(ANCHOR) + len(ANCHOR)
    p = p[:i] + D_SECTION + p[i:]
    n['prompt'] = p
    return len(p)


def build_variant(src, dst):
    d = json.load(open(os.path.join(HERE, src), encoding='utf-8'))
    r = patch_retrieval(d)
    c = patch_collectors(d)
    s = patch_07(d)
    out = os.path.join(HERE, dst)
    json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    tot = sum(len(x.get('prompt') or '') for x in d['MapValue']['FunctionMaps'])
    print(f"{dst:<22} 조회 {r}  수집 {c}  07 {s:,}자  |  "
          f"노드 {len(d['MapValue']['FunctionMaps'])} · 엣지 {len(d['MapValue']['JoinMaps'])} · "
          f"프롬프트 합계 {tot:,}자")
    return d


def main():
    build_variant('MRI_Agent2_Research_Response_v2.json', 'variant_D_raw.json')
    if os.path.exists(os.path.join(HERE, 'variant_B_prune.json')):
        build_variant('variant_B_prune.json', 'variant_D_on_B.json')


if __name__ == '__main__':
    main()
