#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""점검 블록을 보고서 앞머리에서 뺀다. 세는 일은 〈검수용〉이 이미 한다.

이 블록은 읽는 사람이 본문을 어디까지 믿을지 먼저 알라고 맨 앞에 뒀다.
그런데 조회가 된 실행에서 자기 실행의 근거 13건을 「전부 미확보」로 적었다.
맨 앞에 있다는 이유로, 틀렸을 때의 피해가 가장 컸다.

〈검수용〉이 같은 목록을 이미 센다 — 근거 건수, 검증상태 분포, 자료원별 건수,
주제어 확보 여부까지. **두 번 세면서 다르게 세는 것이 문제였다.**

잃는 것 하나: 스크리닝 점수와 근거의 축별 대조.
〈검수용〉의 「근거를 확보하지 못한 주제어」가 그 역할을 일부 한다.

    python3 drop_report_block.py            # 변형 전체에서 제거
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGETS = ['variant_report_call.json', 'variant_report.json',
           'variant_D_report.json', 'variant_D_on_B_report.json']

LAYOUT_LINE = '□ 조사 결과 점검         <- 본문보다 먼저 낸다. 규칙은 아래 별도 절\n\n'
HEAD = '## □ 조사 결과 점검 — 세는 블록이다. HARD RULE'


def patch(path):
    d = json.load(open(path, encoding='utf-8'))
    hit = 0
    for x in d['MapValue']['FunctionMaps']:
        p = x.get('prompt') or ''
        if HEAD not in p:
            continue
        i = p.index(HEAD)
        j = next(m.start() for m in re.finditer(r'^## ', p, re.M) if m.start() > i)
        p = p[:i] + p[j:]
        p = p.replace(LAYOUT_LINE, '', 1)
        assert '조사 결과 점검' not in p
        x['prompt'] = p
        hit += 1
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"{os.path.basename(path):<30} 제거 {hit}곳")


if __name__ == '__main__':
    for f in (sys.argv[1:] or [os.path.join(HERE, t) for t in TARGETS]):
        if os.path.exists(f):
            patch(f)
