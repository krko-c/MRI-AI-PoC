#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KB 원문 대조 — 주장한 사실이 KB 안에 실제로 있는가.

핵심은 「무엇이 맞았는가」가 아니라 **「어디에도 없는 말이 있는가」** 다.

    KB 어느 문서에도 없는 사실 앵커가 하나라도 있으면 그 근거는 날조다.
    그 말이 KB 에서 오지 않았다면, 어디에서 왔겠는가.

첫 판은 「토큰 2개가 한 문서에서 겹치면 실재」로 봤고 21차를 통과시켰다.
「2026년」·「RSU」·「퇴직연금」은 41개 문서에 전부 있다. 흔한 말의 일치는 증거가 아니다.
21차를 손으로 잡은 방식은 반대였다 — 「자기주식」0건 · 「AT WORK」0건 · 「기획재정부」0건.

KB 는 플랫폼이 준 파일이다. 모델이 고쳐 쓸 수 없다.

    python3 verify_claims.py <근거블록.txt> [--kb <KB루트>] [-v]

입력은 10번 노드의 「## 근거」 블록을 그대로 붙여 넣은 파일.
"""
import re, sys, os, bisect, unicodedata
from collections import defaultdict

DEFAULT_KB = ('/tmp/claude-0/-home-user-MRI-AI-PoC/'
              'a05ec66d-a31b-57d1-8c1d-9e11644d0739/scratchpad/run/kb')

# ── KB ─────────────────────────────────────────────────
def norm(s):
    return re.sub(r'[\s,]+', '', unicodedata.normalize('NFKC', s))

def load_kb(root):
    docs = {}
    for dp, _, ns in os.walk(root):
        for n in ns:
            p = os.path.join(dp, n)
            try: t = open(p, encoding='utf-8', errors='ignore').read()
            except Exception: continue
            if t.strip(): docs[os.path.relpath(p, root)] = norm(t)
    return docs

# ── 사실 앵커 ──────────────────────────────────────────
# 앵커는 **원문(띄어쓰기 살린 상태)** 에서 뽑는다. 공백을 먼저 지우면
# 「2026년 9월 기준 신한투자증권」이 「월기준신한투자증권」이 된다.
AMT   = re.compile(r'(?:\d+조\s*)?\d[\d,.]*\s*(?:조원|조|억원|억|만명|개사)')
PCT   = re.compile(r'\d[\d.]*\s*%')
ORG   = re.compile(r'(?<![가-힣])[가-힣A-Za-z]{2,10}'
                   r'(?:증권|은행|자산운용|투자신탁운용|전자|하이닉스)(?![가-힣])'
                   r'|기획재정부|금융위원회|고용노동부|금융감독원')
BRAND = re.compile(r'AT\s*WORK|RSA|ESPP|자기주식|도입률|비과세|과세\s*이연')

UNIT = {'조원':1e12, '조':1e12, '억원':1e8, '억':1e8, '만명':1e4, '개사':1}

def amount(tok):
    """「2조2,811억」·「2.3조원」 → 실수. 복합 단위는 더한다."""
    t = re.sub(r'[\s,]', '', tok); v = 0.0; got = False
    for m in re.finditer(r'(\d+(?:\.\d+)?)(조원|조|억원|억|만명|개사)', t):
        v += float(m.group(1)) * UNIT[m.group(2)]; got = True
    return v if got else None

def kb_amounts(docs):
    """KB 안의 모든 금액. 협회통계는 단위 라벨이 없는 순수 숫자표(억 단위)다."""
    out = set()
    for t in docs.values():
        for m in re.finditer(r'(?:\d+조)?\d[\d.]*(?:조원|조|억원|억|만명)', t):
            a = amount(m.group(0))
            if a: out.add(a)
        for m in re.finditer(r'(?<![\d.])\d{3,7}(?:\.\d+)?(?![\d.])', t):
            try: out.add(float(m.group(0)) * 1e8)
            except ValueError: pass
    return sorted(out)

def amt_ok(a, pool, tol=0.03):
    """±3%. 「2.3조원」과 「2조2,811억」(2.2811조)은 0.8% 차이다."""
    i = bisect.bisect_left(pool, a)
    return any(0 <= j < len(pool) and abs(pool[j]-a) <= a*tol for j in (i-1, i, i+1))

def present(tok, text, numeric):
    """숫자는 부분일치 오탐을 만든다: 「25%」가 「31.25%」에 걸린다."""
    i = 0
    while True:
        i = text.find(tok, i)
        if i < 0: return False
        if not numeric: return True
        b = text[i-1] if i else ''
        a = text[i+len(tok)] if i+len(tok) < len(text) else ''
        if b not in '0123456789.' and not a.isdigit(): return True
        i += 1

def anchors(claim):
    out, seen = [], set()
    for rx, kind in ((AMT, 'amt'), (PCT, 'pct'), (ORG, 'txt'), (BRAND, 'txt')):
        for m in rx.findall(claim):
            t = re.sub(r'\s+', '', m)
            if len(t) >= 2 and t not in seen:
                seen.add(t); out.append((t, kind))
    return out

def support(tok, kind, docs, pool):
    # 금액 풀 대조(±3%)는 조·억 에만 쓴다. 단위 환산이 필요한 것은 그것뿐이다.
    # 「100개사」·「10만명」은 환산 대상이 아니라 글자 그대로 찾아야 한다.
    if kind == 'amt' and re.search(r'조원|조|억원|억', tok):
        a = amount(tok)
        if a and amt_ok(a, pool): return ['<수치>']
        # 환산으로 못 찾아도 글자 그대로 있을 수 있다
    return [p for p, x in docs.items() if present(tok, x, kind in ('pct', 'amt'))]

# ── 입력 ───────────────────────────────────────────────
def parse(path):
    items, cur = [], None
    for line in open(path, encoding='utf-8'):
        m = re.match(r'\s*\*{0,2}\[(E\d+)\]\*{0,2}\s*(.*)', line)
        if m:
            if cur: items.append(cur)
            cur = {'id': m.group(1), 'label': m.group(2).strip(), 'text': ''}
        elif cur is not None and line.lstrip().startswith('>'):
            cur['text'] += ' ' + line.lstrip()[1:].strip()
    if cur: items.append(cur)
    return items

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    kb = sys.argv[sys.argv.index('--kb')+1] if '--kb' in sys.argv else DEFAULT_KB
    verbose = '-v' in sys.argv
    if not args: print(__doc__); sys.exit(2)
    docs = load_kb(kb)
    if not docs: print(f'✗ KB 없음: {kb}'); sys.exit(2)
    pool = kb_amounts(docs)

    print('■ KB 원문 대조 — 모델이 통과시킬 수 없다')
    print(f'  KB {len(docs)}개 문서 · {sum(len(t) for t in docs.values()):,}자 · 금액 {len(pool):,}개')
    print('  규칙: KB 어느 문서에도 없는 사실 앵커가 1개라도 있으면 날조\n')

    items = parse(args[0]); tally = defaultdict(int); ghosts = []
    print(f"{'ID':<5}{'판정':<10}{'앵커':<6}{'미확인':<7}KB 어디에도 없는 말")
    print('-' * 100)
    for it in items:
        toks = anchors(it['text'])
        df = {t: support(t, k, docs, pool) for t, k in toks}
        ghost = [t for t, _ in toks if not df[t]]
        v = 'SKIP' if not toks else ('FAB' if ghost else 'REAL')
        tally[v] += 1; ghosts += ghost
        mark = {'REAL':'○ 실재', 'FAB':'✗ 날조', 'SKIP':'- 앵커없음'}[v]
        if v == 'REAL':
            rare = min((t for t, _ in toks), key=lambda t: len(df[t]))
            detail = f"(최희소 앵커 「{rare}」 {len(df[rare])}곳)"
        else:
            detail = ' · '.join(ghost[:6]) + ('…' if len(ghost) > 6 else '')
        print(f"{it['id']:<5}{mark:<10}{len(toks):<6}{len(ghost):<7}{detail}")
        if verbose:
            for t, k in toks:
                print(f"       {t:<16}[{k}] {len(df[t]):>2}곳 "
                      f"{os.path.basename(df[t][0])[:44] if df[t] else '← 없음'}")
    tot = sum(tally.values())
    print('-' * 100)
    print(f"실재 {tally['REAL']} · 날조 {tally['FAB']} · 앵커없음 {tally['SKIP']}  (근거 {tot}건)")
    if ghosts:
        u = sorted(set(ghosts))
        print(f"\nKB 에 존재하지 않는 말 {len(u)}종:")
        for i in range(0, len(u), 6): print('   ' + ' · '.join(u[i:i+6]))
    if tally['FAB']:
        print(f"\n판정: 날조 {tally['FAB']}건 / {tot}건 "
              f"({tally['FAB']*100//max(tot,1)}%). **그대로 쓸 수 없다.**")
        sys.exit(1)
    print('\n판정: 근거 전량의 사실 앵커가 KB 원문에서 확인됐다.')

if __name__ == '__main__':
    main()
