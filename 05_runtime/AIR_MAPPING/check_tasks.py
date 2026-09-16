#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
태스크 사전 검사 — 이 질의로 그 KB 에서 답이 나오는가.

조회를 돌리기 전에 「답이 없는 질문」을 가려낸다.
21차에서 태스크 23개 중 13개(56%)가 해당 자료원에 없는 축을 물었고,
잘못된 근거 8건 중 7건이 거기서 나왔다.

모델은 아무 때나 지어내지 않는다. **지어낼 재료가 있을 때만** 지어낸다.

    KB 에도 없고 MRI 에도 없음   → 정직하게 NO_RESULT (21차 5개 태스크가 그랬다)
    KB 엔 없는데 MRI·질문문에 있음 → 전사하고 「KB 검색결과」라고 표기
    KB 엔 없는데 비슷한 표가 있음  → 표 모양을 베껴 창작

앞의 둘은 질의를 고치면 막힌다. 이 도구는 그것을 조회 전에 잡는다.

    python3 check_tasks.py <태스크JSON> [--kb <KB루트>]

태스크 JSON 은 05 또는 06P 출력을 그대로 저장한 파일.
`primary_tasks` · `dependent_tasks` · `retrieval_tasks` · `discovery_tasks` 를 읽는다.
각 태스크에서 `source` 와 `query_terms` 만 본다.

KB 원문과 태스크는 사내 자료다. 커밋하지 않는다. 경로로만 넘긴다.
"""
import os, re, sys, json, unicodedata

DEFAULT_KB = ('/tmp/claude-0/-home-user-MRI-AI-PoC/'
              'a05ec66d-a31b-57d1-8c1d-9e11644d0739/scratchpad/run/kb')
norm = lambda s: re.sub(r'[\s,]+', '', unicodedata.normalize('NFKC', s))

def load_corpus(root):
    """소스(=KB 폴더)별로 전문을 한 덩어리로 합친다."""
    corp = {}
    for src in sorted(os.listdir(root)):
        d = os.path.join(root, src)
        if not os.path.isdir(d): continue
        t = ''
        for dp, _, ns in os.walk(d):
            for n in ns:
                try: t += open(os.path.join(dp, n), encoding='utf-8', errors='ignore').read()
                except Exception: pass
        corp[src] = norm(t)
    return corp

TASK_KEYS = ('primary_tasks', 'dependent_tasks', 'retrieval_tasks',
             'discovery_tasks', 'open_discovery_tasks', 'followup_tasks')

def load_tasks(path):
    o = json.load(open(path, encoding='utf-8'))
    out, seen = [], set()
    def walk(x):
        if isinstance(x, dict):
            for k in TASK_KEYS:
                for t in x.get(k) or []:
                    tid = t.get('task_id')
                    if tid and tid not in seen and t.get('query_terms'):
                        seen.add(tid)
                        out.append((tid, t.get('source', '?'), t['query_terms']))
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(o)
    return out

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    kb = sys.argv[sys.argv.index('--kb')+1] if '--kb' in sys.argv else DEFAULT_KB
    if not args: print(__doc__); sys.exit(2)
    corp = load_corpus(kb)
    if not corp: print(f'✗ KB 없음: {kb}'); sys.exit(2)
    tasks = load_tasks(args[0])
    if not tasks: print('✗ 태스크를 찾지 못했다. 05 또는 06P 출력 JSON 인지 확인'); sys.exit(2)

    print('■ 태스크 질의어가 해당 KB 에 실제로 있는가 — 조회 전 검사')
    print(f'  KB {len(corp)}개 자료원 · 태스크 {len(tasks)}개\n')
    print(f"{'태스크':<8}{'소스':<22}{'적중':<8}{'판정':<12}KB 에 없는 질의어")
    print('-' * 104)
    ok = weak = dead = nokb = 0
    for tid, src, terms in tasks:
        txt = corp.get(src, '')
        hit  = [t for t in terms if norm(t) in txt]
        miss = [t for t in terms if norm(t) not in txt]
        r = len(hit) / max(len(terms), 1)
        if   not txt:  v, nokb = '- KB없음',  nokb + 1
        elif r >= 0.5: v, ok   = '○ 답 있음', ok + 1
        elif hit:      v, weak = '△ 부분',    weak + 1
        else:          v, dead = '✗ 답 없음', dead + 1
        print(f"{tid:<8}{src:<22}{len(hit)}/{len(terms):<6}{v:<12}{' · '.join(miss[:5])}")
    print('-' * 104)
    tot = ok + weak + dead
    print(f"○ 답 있음 {ok} · △ 부분 {weak} · ✗ 답 없음 {dead}"
          + (f" · KB없음 {nokb}" if nokb else "") + f"   (태스크 {tot + nokb}개)")
    bad = dead + weak
    if bad:
        print(f"\n답이 없거나 모자란 질의 {bad}개 / {tot}개 ({bad*100//max(tot,1)}%).")
        print("이 태스크들은 NO_RESULT 를 내거나 지어내거나 둘 중 하나다.")
        print("지어낼 재료(MRI 원문·질문문·비슷한 표)가 있으면 지어낸다.")
        sys.exit(1)
    print('\n모든 태스크가 해당 자료원에서 답할 수 있는 질의다.')

if __name__ == '__main__':
    main()
