#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⑳ 상품·통계 소스에는 제도 이름을 넣지 않는다 — 10차에서 통했던 질의어로 되돌린다.

기계 대조로 가장 좋았던 실행은 11차다(인용 13 · 일치 10 · 날조 1).
그 개선은 **7차 수정의 효과**라고 로그에 적혀 있고, 7차 수정 2 가 질의어였다.

10차 당사 조회 질의어:
    ["엔에이치아문디자산운용", "설정액", "순위", "점유율", "운용규모", "자산유형"]
**「퇴직연금」이 아예 없다.** 제도 이름을 빼고 데이터의 축으로 물으니 FreeSIS 가 답했고,
당사 현황이 처음으로 실제 숫자로 찼다 — `공모(ETF포함) 전체 7위 · 점유율 3.37%`.

25차 질의어:
    T05 ["퇴직연금","설정액","운용규모","시장점유율","순위","자산유형"]
    T16 ["엔에이치아문디자산운용","설정액","순위","시장점유율","운용규모"]
T05 는 「퇴직연금」이 첫 단어이고 NO_RESULT. T16 도 NO_RESULT.
제로인 공모(T13)도 「퇴직연금·DC·IRP」를 넣고 NO_RESULT.

05 의 규칙은 「제도 이름은 **넣더라도 단독으로 두지 않는다**」였다.
25차는 그 규칙을 글자 그대로 지켰고, 그래서 넣었고, 실패했다.
**규칙이 통했던 실행보다 느슨했다.** 10차는 넣지 않았다.

    python3 patch_query_axis.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGETS = ['variant_report_call.json', 'variant_report.json',
           'variant_D_report.json', 'variant_D_on_B_report.json',
           'MRI_Agent2_Research_Response_v2.json']

OLD = """- **제도 이름은 넣더라도 단독으로 두지 않는다.** 제도명만으로 이루어진 질의는 만들지 않는다."""

NEW = """- **제도 이름은 넣지 않는다.** 「퇴직연금」·「DC」·「IRP」·「연금저축」을
  상품·통계 소스(ZeroIn 계열, FreeSIS) 태스크의 `query_terms` 에 넣지 않는다.
  **「단독으로 두지 않는다」가 아니라 넣지 않는다.** 한 단어라도 섞이면 질의가 그쪽으로 끌린다.

  기계 대조로 가장 좋았던 실행의 당사 조회 질의어가 이것이었다.

      ["엔에이치아문디자산운용", "설정액", "순위", "점유율", "운용규모", "자산유형"]

  **「퇴직연금」이 하나도 없다.** 그래서 FreeSIS 가 답했고 당사 현황이 실제 숫자로 찼다.
  직전 실행은 `["퇴직연금","설정액","운용규모","시장점유율","순위","자산유형"]` 로 물었고
  NO_RESULT 였다. 같은 자료원, 같은 축, 제도 이름 하나 차이다.

  제도를 다루는 조사 과제라도 마찬가지다. **무엇을 알고 싶은지와 어떻게 물을지는 다른 일이다.**
  제도는 `target` 에 적고, `query_terms` 에는 그 소스의 말만 넣는다."""


def patch(path):
    d = json.load(open(path, encoding='utf-8'))
    hit = 0
    for x in d['MapValue']['FunctionMaps']:
        p = x.get('prompt') or ''
        if OLD not in p:
            continue
        x['prompt'] = p.replace(OLD, NEW, 1)
        hit += 1
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"{os.path.basename(path):<36} 계획 노드 {hit}곳")


if __name__ == '__main__':
    for f in (sys.argv[1:] or [os.path.join(HERE, t) for t in TARGETS]):
        if os.path.exists(f):
            patch(f)
