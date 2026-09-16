#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D안 전용 검사 — 07 의 인용문이 정말 `raw_answer` 안에 있는지 대조한다.

D안은 조회 노드가 도구 출력을 통째로 넘기게 만든 판이다. 그래서 이 검사가 가능해진다.

    07 이 쓴 모든 verbatim_quotes ⊂ 조회 노드가 담아 온 raw_answer 합집합

이 포함관계는 **기계가 판정한다.** 모델이 「확인했다」고 말할 자리가 없다.
문장이 raw 안에 없으면 그 근거는 조회로 얻은 것이 아니다. 그것뿐이다.

    python3 check_quotes.py <실행결과.json>
    python3 check_quotes.py <실행결과.json> --strict   # 출처미상도 실패로 센다

실행 로그를 통째로 붙여 넣은 텍스트도 받는다. 파일에서 JSON 객체를 찾아 읽는다.
종료코드 0 = 통과, 1 = 인용문이 raw 에 없는 근거가 있음.
"""
import json, re, sys, unicodedata

WS = re.compile(r'\s+')


def norm(s):
    """줄바꿈·공백·전각만 맞춘다. 글자는 건드리지 않는다."""
    return WS.sub(' ', unicodedata.normalize('NFKC', s or '')).strip()


def walk(o):
    """중첩 구조 어디에 있든 dict 를 전부 훑는다."""
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def load(path):
    """JSON 파일이면 그대로, 로그 텍스트면 안에서 JSON 객체를 긁어 모은다."""
    raw = open(path, encoding='utf-8').read()
    try:
        return [json.loads(raw)]
    except Exception:
        pass
    out, i = [], 0
    while True:
        i = raw.find('{', i)
        if i < 0:
            return out
        dec = json.JSONDecoder()
        try:
            obj, j = dec.raw_decode(raw[i:])
            out.append(obj)
            i += j
        except Exception:
            i += 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    strict = '--strict' in sys.argv
    if not args:
        print(__doc__)
        return 2
    docs = load(args[0])
    if not docs:
        print('JSON 을 찾지 못했다:', args[0])
        return 2

    # 1) raw 풀 — 조회 노드가 담아 온 도구 출력 전부
    pool, raws = {}, 0
    for d in docs:
        for o in walk(d):
            if 'raw_answer' in o and isinstance(o.get('raw_answer'), str):
                tid = o.get('task_id') or o.get('id') or f'#{raws}'
                pool[tid] = norm(o['raw_answer'])
                raws += 1
    joined = '\n'.join(pool.values())

    # 2) 근거 — 07 이 만든 evidence item
    items = [o for d in docs for o in walk(d)
             if 'evidence_id' in o and 'verbatim_quotes' in o]

    print(f"raw_answer 레코드 {raws}건 ({len(joined):,}자) · 근거 {len(items)}건\n")
    if raws == 0:
        print('⚠ raw_answer 가 하나도 없다. D안 판으로 돌린 결과가 맞는지 확인하라.')
        return 2

    bad, weak, ok = [], [], 0
    for it in items:
        eid = it.get('evidence_id', '?')
        st = it.get('status', '?')
        qs = [q for q in (it.get('verbatim_quotes') or []) if isinstance(q, str) and q.strip()]
        names = ' / '.join(it.get('source_names') or []) or '(출처칸 비어 있음)'
        claim = norm(it.get('claim'))[:60]

        if not qs:
            (bad if st == 'VERIFIED' else weak).append((eid, st, '인용문 없음', claim, names))
            continue

        miss = [q for q in qs if norm(q) not in joined]
        if miss:
            where = '인용문이 raw 에 없음: ' + norm(miss[0])[:50]
            (bad if st in ('VERIFIED', 'PARTIAL') else weak).append((eid, st, where, claim, names))
            continue

        # 인용은 맞다. 그럼 어느 레코드인지 짚었는가
        tid = it.get('quote_source_task_id')
        if tid and tid not in pool:
            weak.append((eid, st, f'quote_source_task_id 가 없는 레코드: {tid}', claim, names))
            continue
        if '출처미상' in names or not (it.get('source_paths') or []):
            (bad if strict else weak).append((eid, st, '인용은 raw 에 있으나 출처 꼬리 없음', claim, names))
            continue
        ok += 1

    for tag, rows in (('✗ 조회 근거 아님', bad), ('⚠ 확인 불가', weak)):
        if not rows:
            continue
        print(tag)
        for eid, st, why, claim, names in rows:
            print(f"  {eid:<5} {st:<9} {why}")
            print(f"        주장: {claim}")
            print(f"        출처: {names}")
        print()

    print(f"○ 인용·출처 모두 확인 {ok} · ⚠ 확인 불가 {len(weak)} · ✗ 조회 근거 아님 {len(bad)}")
    if bad:
        print("\n✗ 로 표시된 근거는 조회로 얻은 것이 아니다. 보고서에 사실로 실으면 안 된다.")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
