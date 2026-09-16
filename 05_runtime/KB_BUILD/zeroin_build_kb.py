# -*- coding: utf-8 -*-
"""제로인 원본 엑셀 → AIR Studio 지식베이스 텍스트.

원본 카탈로그(3,093건 · 7파일 · 클래스 단위 나열)는 여덟 번의 실행에서 한 번도
정상 응답한 적이 없다(Bedrock 400). 작동하는 유일한 통계 KB 인 FreeSIS 는
집계·표시(MARKED) 텍스트다. 그 방식으로 다시 만든다.

  - 클래스가 아니라 **펀드(대표클래스)** 를 한 레코드로 한다. 16,374 행 → 2,760 펀드.
  - 나열 대신 **집계**한다. 유형별·운용사별 합계와 순위를 미리 계산해 넣는다.
  - 조사에 실제로 쓰이는 축(연금 세제구분 · TDF · ETF · 당사)을 파일로 나눈다.

단위: 설정액·순자산 억원 · 수익률 % · 증감은 두 시점(2025-12-31 → 2026-07-31) 차.
"""
import openpyxl, os, io, sys
from collections import defaultdict

SRC = 'kb/85063b5f-____/#Uc0c8 #Ud3f4#Ub354/#Uacf5#Ubaa8#Ud380#Ub4dc#U00b7ETF #Uc124#Uc815#Uc561 #Uc99d#Uac10_260731_aipoc.xlsx'
OUT = 'zeroin_new/kb'
NH  = 'NH-Amundi운용'
D1, D2 = '2025-12-31', '2026-07-31'


def load():
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    out = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(min_row=9, values_only=True))
        hdr = [str(c).strip() if c is not None else '' for c in rows[0]]
        data = [r for r in rows[1:] if r[1] not in (None, '', '-')]
        out[ws.title] = ({h: i for i, h in enumerate(hdr) if h}, data)
    wb.close()
    return out


def f(v):
    try:
        x = float(v)
        return x if x == x else None          # NaN 제거
    except (TypeError, ValueError):
        return None


def n(v, nd=2):
    return '' if v is None else ('%.*f' % (nd, v)).rstrip('0').rstrip('.')


def s(v):
    t = '' if v is None else str(v).strip()
    return '' if t in ('None', '-', 'nan') else t.replace('|', '/').replace('\n', ' ')


def pct(a, b):
    return None if not b else (a - b) / b * 100.0


def top(pairs, k=10):
    """[(이름, 값)] → '1:이름=값; 2:…' 상위 k"""
    r = sorted((p for p in pairs if p[1] is not None), key=lambda x: -x[1])[:k]
    return '; '.join('%d:%s=%s' % (i, a, n(b)) for i, (a, b) in enumerate(r, 1))


def rank_share(name, pairs):
    """(순위, 점유율%) — 값이 없으면 ('NA', 0)"""
    r = sorted((p for p in pairs if p[1] is not None), key=lambda x: -x[1])
    tot = sum(v for _, v in r) or None
    for i, (a, b) in enumerate(r, 1):
        if a == name:
            return i, (b / tot * 100.0 if tot else None)
    return 'NA', None


def block(tag, fields):
    """레코드 경계 문자열을 하나로 통일한다.

    이전 KB 는 `[ZEROIN_PUBLIC_CATALOG]` 처럼 종류마다 다른 표지를 쓰고
    청킹은 `[ZEROIN_` 접두로 잡게 해 두었다. 플랫폼이 접두가 아니라 정확한
    문자열을 찾는다면 청킹이 통째로 실패하고 파일 하나가 한 덩어리가 된다.
    그래서 표지는 `[ZEROIN_RECORD]` 하나만 쓰고, 종류는 첫 칸에 적는다.
    """
    body = ' | '.join('%s=%s' % (k, v)
                      for k, v in [('레코드', tag)] + list(fields) if v not in (None, ''))
    return '[ZEROIN_RECORD]\n%s\n[END_ZEROIN_RECORD]\n\n' % body


WARN = ('# 주의: 이 파일은 제로인(ZeroIn) 기준이다. 협회통계(FreeSIS) 와 집계 기준이 달라 '
        '같은 항목의 값이 일치하지 않는다.\n'
        '#       한 문장 안에서 두 자료원의 수치를 섞지 않는다. 출처를 밝히고 따로 쓴다.\n')


def head(title, note):
    return ('# %s\n# Snapshots: %s, %s\n# Units: 설정액·순자산 억원 · 수익률 %% · '
            '증감 = %s 대비 %s\n# %s\n%s\n' % (title, D1, D2, D1, D2, note, WARN))


# ─────────────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUT, exist_ok=True)
    o = load()
    H2, d2 = o['공모펀드_260731']
    H1, d1 = o['공모펀드_251231']
    E2, e2 = o['ETF_260731']
    E1, e1 = o['ETF_251231']

    rep2 = [r for r in d2 if s(r[H2['대표클래스구분']]) == 'Y']
    prev = {s(r[H1['Code']]): r for r in d1}

    def g(r, H, c):          # 안전한 열 접근
        return r[H[c]] if c in H else None

    # ── 1. 소유형별 시장 집계 ───────────────────────────────────────
    byt = defaultdict(list)
    for r in rep2:
        byt[(s(g(r, H2, '대유형명')), s(g(r, H2, '소유형명')))].append(r)

    rows = []
    for (big, small), fs in byt.items():
        if not small:
            continue
        cur = sum(f(g(r, H2, '패밀리 설정액(억원)')) or 0 for r in fs)
        old = 0.0
        for r in fs:
            p = prev.get(s(g(r, H2, 'Code')))
            if p:
                old += f(g(p, H1, '패밀리 설정액(억원)')) or 0
        mgr = defaultdict(float)
        cnt = defaultdict(int)
        for r in fs:
            m = s(g(r, H2, '운용사명'))
            mgr[m] += f(g(r, H2, '패밀리 설정액(억원)')) or 0
            cnt[m] += 1
        rk, sh = rank_share(NH, list(mgr.items()))
        rows.append((cur, block('ZEROIN_TYPE_RECORD', [
            ('대유형', big), ('소유형', small),
            ('펀드수', len(fs)), ('운용사수', len(mgr)),
            ('설정액_2512', n(old)), ('설정액_2607', n(cur)),
            ('증감', n(cur - old)), ('증감률', n(pct(cur, old))),
            ('NH_설정액_2607', n(mgr.get(NH))), ('NH_펀드수', cnt.get(NH, 0)),
            ('NH_순위', rk), ('NH_점유율', n(sh)),
            ('top10_2607', top(list(mgr.items()))),
        ])))
    rows.sort(key=lambda x: -x[0])
    io.open(os.path.join(OUT, 'ZEROIN_TYPE_SUMMARY_MARKED.txt'), 'w', encoding='utf-8').write(
        head('ZEROIN TYPE SUMMARY — 소유형별 공모펀드 시장 집계(ETF 제외)',
             '펀드 = 대표클래스 1건. 순위·점유율은 해당 소유형 안에서 운용사 설정액 합으로 계산.')
        + ''.join(b for _, b in rows))

    # ── 2. 당사 펀드 ────────────────────────────────────────────────
    small_mgr = defaultdict(lambda: defaultdict(float))
    for r in rep2:
        small_mgr[s(g(r, H2, '소유형명'))][s(g(r, H2, '운용사명'))] += f(g(r, H2, '패밀리 설정액(억원)')) or 0

    nh = [r for r in rep2 if s(g(r, H2, '운용사명')) == NH]
    nh.sort(key=lambda r: -(f(g(r, H2, '패밀리 설정액(억원)')) or 0))
    buf = []
    for r in nh:
        cur = f(g(r, H2, '패밀리 설정액(억원)'))
        p = prev.get(s(g(r, H2, 'Code')))
        old = f(g(p, H1, '패밀리 설정액(억원)')) if p else None
        sm = s(g(r, H2, '소유형명'))
        rk, sh = rank_share(NH, list(small_mgr[sm].items()))
        buf.append(block('ZEROIN_NH_FUND_RECORD', [
            ('상품명', s(g(r, H2, 'Name'))), ('펀드코드', s(g(r, H2, 'Code'))),
            ('대유형', s(g(r, H2, '대유형명'))), ('소유형', sm),
            ('운용전략', s(g(r, H2, '운용전략'))), ('테마', s(g(r, H2, '테마'))),
            ('세제구분', s(g(r, H2, '세제상품명칭'))),
            ('퇴직연금', s(g(r, H2, '퇴직연금 세제혜택여부')) or 'N'),
            ('연금저축', s(g(r, H2, '연금저축 세제혜택여부')) or 'N'),
            ('최초설정일', s(g(r, H2, '최초설정일'))[:10]),
            ('설정액_2512', n(old)), ('설정액_2607', n(cur)),
            ('증감', n(None if old is None or cur is None else cur - old)),
            ('증감률', n(None if old is None or cur is None else pct(cur, old))),
            ('순자산_2607', n(f(g(r, H2, '패밀리 순자산(억원)')))),
            ('수익률_1M', n(f(g(r, H2, '수익률 (1개월)')))),
            ('수익률_3M', n(f(g(r, H2, '수익률 (3개월)')))),
            ('수익률_6M', n(f(g(r, H2, '수익률 (6개월)')))),
            ('수익률_1Y', n(f(g(r, H2, '수익률 (1년)')))),
            ('수익률_YTD', n(f(g(r, H2, '수익률 (연초이후)')))),
            ('설정이후수익률', n(f(g(r, H2, '설정이후수익률')))),
            ('소유형내_NH순위', rk), ('소유형내_NH점유율', n(sh)),
        ]))
    io.open(os.path.join(OUT, 'ZEROIN_NH_FUNDS_MARKED.txt'), 'w', encoding='utf-8').write(
        head('ZEROIN NH FUNDS — 엔에이치아문디자산운용(NH-Amundi운용) 공모펀드 전체',
             '대표클래스 기준 %d개. 설정액 내림차순.' % len(nh)) + ''.join(buf))

    # ── 3. 연금 · TDF ──────────────────────────────────────────────
    buf = []
    for label, pick in [
        ('퇴직연금', lambda r: s(g(r, H2, '퇴직연금 세제혜택여부')) == 'Y'),
        ('연금저축', lambda r: s(g(r, H2, '연금저축 세제혜택여부')) == 'Y'),
        ('개인연금', lambda r: s(g(r, H2, '개인연금 세제혜택여부')) == 'Y'),
        ('TDF',      lambda r: 'TDF' in s(g(r, H2, '테마'))),
        ('디딤펀드',  lambda r: '디딤' in s(g(r, H2, '테마'))),
    ]:
        fs = [r for r in rep2 if pick(r)]
        if not fs:
            continue
        mgr, cnt = defaultdict(float), defaultdict(int)
        for r in fs:
            m = s(g(r, H2, '운용사명'))
            mgr[m] += f(g(r, H2, '패밀리 설정액(억원)')) or 0
            cnt[m] += 1
        cur = sum(mgr.values())
        old = 0.0
        for r in fs:
            p = prev.get(s(g(r, H2, 'Code')))
            if p:
                old += f(g(p, H1, '패밀리 설정액(억원)')) or 0
        rk, sh = rank_share(NH, list(mgr.items()))
        sub = defaultdict(float)
        for r in fs:
            sub[s(g(r, H2, '소유형명'))] += f(g(r, H2, '패밀리 설정액(억원)')) or 0
        buf.append(block('ZEROIN_PENSION_SEGMENT_RECORD', [
            ('구분', label), ('펀드수', len(fs)), ('운용사수', len(mgr)),
            ('설정액_2512', n(old)), ('설정액_2607', n(cur)),
            ('증감', n(cur - old)), ('증감률', n(pct(cur, old))),
            ('NH_설정액_2607', n(mgr.get(NH))), ('NH_펀드수', cnt.get(NH, 0)),
            ('NH_순위', rk), ('NH_점유율', n(sh)),
            ('top10_운용사', top(list(mgr.items()))),
            ('top10_소유형', top(list(sub.items()))),
        ]))
        for r in sorted(fs, key=lambda r: -(f(g(r, H2, '패밀리 설정액(억원)')) or 0))[:25]:
            buf.append(block('ZEROIN_PENSION_FUND_RECORD', [
                ('구분', label), ('상품명', s(g(r, H2, 'Name'))),
                ('운용사', s(g(r, H2, '운용사명'))), ('소유형', s(g(r, H2, '소유형명'))),
                ('설정액_2607', n(f(g(r, H2, '패밀리 설정액(억원)')))),
                ('수익률_1Y', n(f(g(r, H2, '수익률 (1년)')))),
                ('수익률_YTD', n(f(g(r, H2, '수익률 (연초이후)')))),
                ('당사여부', 'Y' if s(g(r, H2, '운용사명')) == NH else 'N'),
            ]))
    io.open(os.path.join(OUT, 'ZEROIN_PENSION_TDF_MARKED.txt'), 'w', encoding='utf-8').write(
        head('ZEROIN PENSION & TDF — 연금 세제구분·TDF·디딤펀드',
             '구분별 시장 집계 + 구분별 설정액 상위 25개 펀드.') + ''.join(buf))

    # ── 4. ETF ──────────────────────────────────────────────────────
    eprev = {s(r[E1['Code']]): r for r in e1}
    buf = []
    mgr, cnt = defaultdict(float), defaultdict(int)
    for r in e2:
        m = s(g(r, E2, '운용사명'))
        mgr[m] += f(g(r, E2, '설정액(억원)')) or 0
        cnt[m] += 1
    cur = sum(mgr.values())
    old = sum(f(g(r, E1, '설정액(억원)')) or 0 for r in e1)
    rk, sh = rank_share(NH, list(mgr.items()))
    buf.append(block('ZEROIN_ETF_MARKET_RECORD', [
        ('구분', 'ETF 전체'), ('종목수_2512', len(e1)), ('종목수_2607', len(e2)),
        ('운용사수', len(mgr)),
        ('설정액_2512', n(old)), ('설정액_2607', n(cur)),
        ('증감', n(cur - old)), ('증감률', n(pct(cur, old))),
        ('NH_설정액_2607', n(mgr.get(NH))), ('NH_종목수', cnt.get(NH, 0)),
        ('NH_순위', rk), ('NH_점유율', n(sh)),
        ('top10_운용사', top(list(mgr.items()))),
    ]))
    bys = defaultdict(list)
    for r in e2:
        bys[(s(g(r, E2, '대유형명')), s(g(r, E2, '소유형명')))].append(r)
    for (big, small), fs in sorted(bys.items(),
                                   key=lambda kv: -sum(f(g(r, E2, '설정액(억원)')) or 0 for r in kv[1])):
        m2 = defaultdict(float)
        for r in fs:
            m2[s(g(r, E2, '운용사명'))] += f(g(r, E2, '설정액(억원)')) or 0
        c = sum(m2.values())
        p = sum((f(g(eprev[s(g(r, E2, 'Code'))], E1, '설정액(억원)')) or 0)
                for r in fs if s(g(r, E2, 'Code')) in eprev)
        r_, sh_ = rank_share(NH, list(m2.items()))
        buf.append(block('ZEROIN_ETF_TYPE_RECORD', [
            ('대유형', big), ('소유형', small), ('종목수', len(fs)),
            ('설정액_2512', n(p)), ('설정액_2607', n(c)),
            ('증감', n(c - p)), ('증감률', n(pct(c, p))),
            ('NH_설정액_2607', n(m2.get(NH))), ('NH_순위', r_), ('NH_점유율', n(sh_)),
            ('top5_운용사', top(list(m2.items()), 5)),
        ]))
    for r in sorted([x for x in e2 if s(g(x, E2, '운용사명')) == NH],
                    key=lambda r: -(f(g(r, E2, '설정액(억원)')) or 0)):
        p = eprev.get(s(g(r, E2, 'Code')))
        po = f(g(p, E1, '설정액(억원)')) if p else None
        c = f(g(r, E2, '설정액(억원)'))
        buf.append(block('ZEROIN_NH_ETF_RECORD', [
            ('상품명', s(g(r, E2, 'Name'))), ('종목코드', s(g(r, E2, 'ETF종목코드'))),
            ('대유형', s(g(r, E2, '대유형명'))), ('소유형', s(g(r, E2, '소유형명'))),
            ('운용전략', s(g(r, E2, '운용전략'))),
            ('최초설정일', s(g(r, E2, '최초설정일'))[:10]),
            ('설정액_2512', n(po)), ('설정액_2607', n(c)),
            ('증감', n(None if po is None or c is None else c - po)),
            ('신규여부', 'Y' if p is None else 'N'),
            ('순자산_2607', n(f(g(r, E2, '순자산액(억원)')))),
            ('수익률_1Y', n(f(g(r, E2, '수익률 (1년)')))),
            ('수익률_YTD', n(f(g(r, E2, '수익률 (연초이후)')))),
        ]))
    io.open(os.path.join(OUT, 'ZEROIN_ETF_MARKED.txt'), 'w', encoding='utf-8').write(
        head('ZEROIN ETF — ETF 시장 집계 및 당사 ETF 전 종목',
             'ETF 는 클래스 구분이 없어 종목 1건 = 1레코드.') + ''.join(buf))

    # ── 5. QA ───────────────────────────────────────────────────────
    io.open(os.path.join(OUT, 'ZEROIN_MARKED_QA.txt'), 'w', encoding='utf-8').write(
        """# ZEROIN KB 사용 안내

[ZEROIN_QA_RECORD]
질문=이 자료는 무엇인가
답=제로인(ZeroIn) 공모펀드·ETF 설정액 자료를 집계한 것이다. 기준일 두 시점은
   2025-12-31 과 2026-07-31 이며, 증감은 그 두 시점의 차이다.
   단위는 설정액·순자산 모두 억원, 수익률은 %이다.
[END_ZEROIN_QA_RECORD]

[ZEROIN_QA_RECORD]
질문=펀드 한 건은 무엇을 세는가
답=클래스가 아니라 펀드(대표클래스) 1건이다. 같은 펀드의 A/C/C-e 등 클래스를
   따로 세지 않는다. 설정액은 패밀리 설정액이다.
[END_ZEROIN_QA_RECORD]

[ZEROIN_QA_RECORD]
질문=협회통계와 숫자가 다르다
답=기준이 다르다. 협회통계(FreeSIS)는 협회 신고 기준, 이 자료는 제로인 기준이다.
   예를 들어 당사 공모 설정액은 두 자료원에서 서로 다른 값으로 나온다.
   어느 쪽이 틀린 것이 아니다. 한 문장 안에서 두 값을 섞지 말고,
   어느 자료원의 값인지 밝혀 따로 쓴다.
[END_ZEROIN_QA_RECORD]

[ZEROIN_QA_RECORD]
질문=당사 표기는 무엇인가
답=제로인 자료에서 당사는 `NH-Amundi운용` 으로 적힌다.
   `엔에이치아문디자산운용` 은 협회통계 표기이며 이 자료에는 없다.
[END_ZEROIN_QA_RECORD]

[ZEROIN_QA_RECORD]
질문=퇴직연금·연금저축 상품은 어떻게 구분하는가
답=세제혜택 여부로 구분한다. ZEROIN_PENSION_TDF_MARKED 에 구분별 집계가 있다.
   퇴직연금 473펀드, 연금저축 316펀드, 개인연금 5펀드다.
   TDF 는 테마 기준 202펀드이며 소유형은 대부분 `글로벌라이프싸이클` 이다.
[END_ZEROIN_QA_RECORD]

[ZEROIN_QA_RECORD]
질문=이 자료로 답할 수 없는 것은
답=(1) 보수·수수료율이 없다. (2) 퇴직연금 적립금(사업자 기준) 통계가 아니다.
   이 자료의 「퇴직연금」은 퇴직연금 세제혜택을 받는 펀드의 설정액이지
   퇴직연금 시장 적립금 총액이 아니다. (3) 판매사·채널 정보가 없다.
   (4) 2025-12-31 이전 시계열이 없다.
   위 항목은 자료에 없으므로 추정하지 않고 「확인되지 않음」으로 남긴다.
[END_ZEROIN_QA_RECORD]

[ZEROIN_QA_RECORD]
질문=ETF 시장 합계가 원본 시트의 표기값과 다르다
답=원본 시트가 상단에 적어 둔 「설정액(시장)」은 국내 ETF 기준이고,
   이 자료의 ETF 전체 집계는 해외 ETF 를 포함한 전 종목 합이다.
   당사 설정액은 두 값이 정확히 일치한다.
[END_ZEROIN_QA_RECORD]
""")

    for fn in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, fn)
        t = io.open(p, encoding='utf-8').read()
        print('%-36s %6.1f KB · 레코드 %4d · 최장레코드 %d자'
              % (fn, os.path.getsize(p) / 1024, t.count('[END_'),
                 max(len(x) for x in t.split('\n\n'))))


main()
