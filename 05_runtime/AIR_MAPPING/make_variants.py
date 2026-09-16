#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""내일 시험할 변형 JSON 을 만든다.

  A  2번 + 3번   조회 구간에 RQ 텍스트를 안 보냄 + 구조 고정 자료원 컬럼 명시
  B  5번         의존·후속·확장탐색 폐지 (노드 8개 삭제, 체인 단축)
  C  A + B       합본

기준선은 현재 JSON(⑫ 적용본). 각 변형은 기준선에서 갈라진다.
"""
import json, copy, re, sys, os

SRC = 'MRI_Agent2_Research_Response_v2.json'
base = json.load(open(SRC, encoding='utf-8'))

def node(d, pre):
    return [x for x in d['MapValue']['FunctionMaps'] if (x.get('COL_NAME') or '').startswith(pre)][0]

# ══════════════════════════════════════════════════════════
# 2번 — 06P 가 조회 구간으로 RQ 텍스트를 넘기지 않는다
# ══════════════════════════════════════════════════════════
def fix2(d):
    n = node(d, '06P'); p = n['prompt']
    old = '  "research_questions":[],'
    new = '  "research_questions":[],        // rq_id · category 만. 아래 규칙을 보라'
    assert old in p
    p = p.replace(old, new)
    p += """

## 조사 질문의 본문을 아래로 넘기지 않는다 — HARD RULE

`research_questions` 의 각 항목은 **두 칸만** 낸다.

    { "rq_id": "S06-RQ01", "category": "POLICY" }

`question` · `decision_use` · `source_theme_links` 를 **싣지 않는다.**

이 뒤의 어떤 노드도 질문 본문을 쓰지 않는다. 07·08·09·10 은 `rq_id` 로만 참조한다.
그런데 질문 본문에는 이슈 원문의 수치가 들어 있다.

    "RSU 도입률이 현재 0.6%에서 선진국 수준(15-65%)으로 …"

**아무도 쓰지 않는 문장이 조회 담당 전원에게 전달되고 있었다.**
조회 결과가 없을 때 그 문장이 조회 결과 자리에 옮겨 적혔다.

쓰지 않는 것은 나르지 않는다.
"""
    n['prompt'] = p
    return '06P: RQ 본문 차단'

# ══════════════════════════════════════════════════════════
# 3번 — 05 에 구조 고정 자료원의 컬럼만 명시
#        (정책·뉴스는 매번 내용이 바뀌므로 넣지 않는다)
# ══════════════════════════════════════════════════════════
SPEC = """

## 자료원이 가진 축 — HARD RULE

아래 두 자료원은 **집계표·상품 데이터베이스**라 구조가 고정돼 있다.
여기 없는 축으로 물으면 답이 없다. 그 질의는 만들지 않는다.

### mri_freesis (협회통계)

    시장 구분   공모(ETF포함) · 공모(ETF제외) · ETF만 · 설정규모(공사모전체)
    자산 유형   전체 · 주식 · 주식혼합 · 채권 · 채권혼합 · 재간접 · 단기금융 ·
                파생형 · 부동산 · 특별자산 · 실물 · 투자계약 · 혼합자산
    값          두 시점 잔액 · 증감 · 증감률 · **순위** · **점유율** · 월별 시계열
    대상        주요 자산운용사

### mri_zeroin_public · mri_zeroin_public2 · mri_zeroin_etf (제로인)

    상품 축     상품명 · 상품ID · 구분(공모/ETF) · 대유형 · 소유형 · 세제구분
    값          설정액 · 순자산 · 기간별 수익률
    대상        운용사별 개별 펀드

**이 자료원들에 없는 축** — 퇴직연금 · DC · DB · IRP · TDF · 디폴트옵션 ·
제도 이름 일반. 제도는 상품 분류가 아니다.

- 「퇴직연금 시장 운용사별 순위」 → 답이 없다. 만들지 않는다
- 「공모 전체 기준 회사별 운용규모·순위·점유율」 → 답이 있다. 이렇게 묻는다

제도 이름으로 묻고 싶으면 **정책·뉴스 자료원**에 묻는다.
정책·뉴스는 매 실행 내용이 달라지므로 여기에 축을 적지 않는다.
그 두 자료원은 주제어로 묻고, 없으면 「자료없음」으로 받는다.

답할 수 없는 항목은 과제로 만들지 말고 `unresearchable_company_items` 와
같은 방식으로 사유를 적어 남긴다. **묻지 않은 것이 지어낸 것보다 낫다.**
"""

def fix3(d):
    n = node(d, '05 ')
    n['prompt'] = n['prompt'] + SPEC
    return '05: 자료원 축 명세'

# ══════════════════════════════════════════════════════════
# 5번 — 의존·후속·확장탐색 폐지
# ══════════════════════════════════════════════════════════
DROP = ['05D', '06X', '06D2', '06E2', '06F2', '06R2', '06S', '06T']

def fix5(d):
    fm = d['MapValue']['FunctionMaps']; jm = d['MapValue']['JoinMaps']
    ids = {}
    for x in fm:
        c = x.get('COL_NAME') or ''
        for p in DROP + ['06B', '06D ', '06R1']:
            if c.startswith(p): ids.setdefault(p.strip(), x['PK_ID'])
    drop = {ids[p] for p in [q.strip() for q in DROP] if p in ids}

    # 1) 삭제 노드를 건너뛰도록 엣지를 잇는다
    nxt = {}
    for e in jm:
        nxt.setdefault(e['FK_START_MAP_ID'], []).append(e)
    def skip(t):
        seen = set()
        while t in drop and t not in seen:
            seen.add(t)
            outs = [e['FK_END_MAP_ID'] for e in nxt.get(t, [])
                    if e['FK_END_MAP_ID'] not in drop or e['FK_END_MAP_ID'] in drop]
            outs = [o for o in (e['FK_END_MAP_ID'] for e in nxt.get(t, []))]
            outs = [o for o in outs if o != t]
            if not outs: return None
            nonkb = [o for o in outs
                     if next((y.get('node_type') for y in fm if y['PK_ID'] == o), '') != 'KNOWLEDGBASE']
            t = nonkb[0] if nonkb else outs[0]
        return t
    new = []
    for e in jm:
        if e['FK_START_MAP_ID'] in drop: continue
        t = skip(e['FK_END_MAP_ID'])
        if t is None: continue
        e = dict(e); e['FK_END_MAP_ID'] = t
        new.append(e)
    # 중복 제거
    seen, ded = set(), []
    for e in new:
        k = (e['FK_START_MAP_ID'], e['FK_END_MAP_ID'])
        if k in seen: continue
        seen.add(k); ded.append(e)
    d['MapValue']['JoinMaps'] = ded
    d['MapValue']['FunctionMaps'] = [x for x in fm if x['PK_ID'] not in drop]

    # 2) 06B 를 의존 조회 → 1차 조회로
    b = node(d, '06B')
    b['prompt'] = b['prompt'].replace('resolved_dependent_tasks', 'primary_tasks')
    b['prompt'] += """

## 이 노드는 1차 조회다 — HARD RULE

의존 과제 구조를 폐지했다. 네 과제는 `primary_tasks` 에 있고 `depends_on` 이 없다.
앞 조회의 결과를 기다리지 않는다. 네 질의만으로 부른다.
"""
    # 3) 05 가 의존 과제·확장탐색을 만들지 않게
    p5 = node(d, '05 ')
    p5['prompt'] += """

## 의존 과제를 만들지 않는다 — HARD RULE

모든 조회 과제는 `depends_on: null` 이다. 앞 과제의 결과를 기다리는 과제를 만들지 않는다.

당사 펀드의 설정액·수익률은 상품 식별자를 미리 알지 않아도
「<회사 표기> · 설정액 · 수익률」만으로 조회된다.
직전 설계에서 이 과제 하나에 의존을 걸어 여덟 차례 실행되지 않았다.

확장 탐색 과제(`D` 로 시작)도 만들지 않는다. 직전 실행에서 전량 자료없음이었다.
"""
    # 4) 06P 가 의존 분류를 하지 않게
    pp = node(d, '06P')
    pp['prompt'] = pp['prompt'].replace(
        'Classify:\n- primary_tasks = executable immediately\n'
        '- dependent_tasks = unresolved depends_on / placeholders',
        'All tasks are primary. `dependent_tasks` is always [].')
    # 5) 06B 를 수집 노드 앞으로 — 조회는 수집보다 먼저다
    #    06D → 06R1 → 06B → 06R3   ⇒   06D → 06B → 06R1 → 06R3
    jm = d['MapValue']['JoinMaps']
    bid = node(d, '06B')['PK_ID']; did = node(d, '06D ')['PK_ID']
    r1 = node(d, '06R1')['PK_ID'];  r3 = node(d, '06R3')['PK_ID']
    def setedge(a, b):
        for e in jm:
            if e['FK_START_MAP_ID'] == a and e['FK_END_MAP_ID'] not in kbids:
                e['FK_END_MAP_ID'] = b; return
    kbids = {x['PK_ID'] for x in d['MapValue']['FunctionMaps']
             if x.get('node_type') == 'KNOWLEDGBASE'}
    setedge(did, bid)    # 06D → 06B
    setedge(bid, r1)     # 06B → 06R1
    setedge(r1,  r3)     # 06R1 → 06R3
    return f'노드 {len(drop)}개 삭제 · 06B 를 1차 조회로 · 조회를 수집 앞으로'

# ══════════════════════════════════════════════════════════
def build(name, fixes, out):
    d = copy.deepcopy(base)
    log = [f(d) for f in fixes]
    fm = d['MapValue']['FunctionMaps']; jm = d['MapValue']['JoinMaps']
    ids = {x['PK_ID'] for x in fm}
    bad = [e for e in jm if e['FK_START_MAP_ID'] not in ids or e['FK_END_MAP_ID'] not in ids]
    assert not bad, f'끊긴 엣지 {len(bad)}개'
    json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    kb = sum(1 for x in fm if x.get('node_type') == 'KNOWLEDGBASE')
    print(f"{name:<22} 노드 {len(fm):>2} (처리 {len(fm)-kb}·KB {kb}) · 엣지 {len(jm):>2} · "
          f"{sum(len(x.get('prompt') or '') for x in fm):>6}자  → {out}")
    for l in log: print(f"                       · {l}")

build('A안 (2+3)',   [fix2, fix3],       'variant_A_2plus3.json')
build('B안 (5)',     [fix5],             'variant_B_prune.json')
build('C안 (2+3+5)', [fix2, fix3, fix5], 'variant_C_all.json')
