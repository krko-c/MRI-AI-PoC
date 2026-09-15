# -*- coding: utf-8 -*-
"""보고서 구성도 생성 — 양식(KOR_BDC) 색·글꼴 사용"""
from PIL import Image, ImageDraw, ImageFont

FD = '/usr/share/fonts/truetype/nanum/'
S = 3                                   # 2배 이상 배율로 그려 인쇄 품질 확보
W = 1700 * S // 2                        # 가로 기준폭
def F(sz, bold=False):
    return ImageFont.truetype(FD + ('NanumBarunGothicBold.ttf' if bold else 'NanumBarunGothic.ttf'), sz * S)

GREEN  = (226, 239, 217)                 # E2EFD9 — 양식 표 음영
GREEN_D= (168, 196, 148)
GRAY   = (242, 242, 242)
LINE   = (60, 60, 60)
INK    = (26, 26, 26)
MUTE   = (95, 95, 95)
WHITE  = (255, 255, 255)

class Canvas:
    def __init__(self, w, h):
        self.im = Image.new('RGB', (w, h), WHITE)
        self.d = ImageDraw.Draw(self.im)
    def box(self, x, y, w, h, fill=WHITE, r=8*S, width=1*S, outline=LINE):
        self.d.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=fill, outline=outline, width=width)
    def text(self, x, y, t, f, fill=INK, anchor='la'):
        self.d.text((x, y), t, font=f, fill=fill, anchor=anchor)
    def arrow(self, cx, y, h=18*S):
        self.d.line([cx, y, cx, y+h-6*S], fill=LINE, width=2*S)
        self.d.polygon([(cx-5*S, y+h-7*S), (cx+5*S, y+h-7*S), (cx, y+h)], fill=LINE)

def cut(d, t, f, maxw):
    if d.textlength(t, font=f) <= maxw: return t
    while t and d.textlength(t+'…', font=f) > maxw: t = t[:-1]
    return t+'…'

# ───────────────────────── 에이전트 1 ─────────────────────────
def agent1(path):
    pad, bh, gap = 14*S, 46*S, 22*S
    steps = [
        ('1단계  이슈 추출',   '리포트에서 이슈 식별 및 본문 전사',    '원문 조회'),
        ('2단계  정합성 확인', '1단계 결과를 원문과 대조 · 7개 항목 판정', '원문 재조회'),
        ('3단계  관점 평가',   '5개 관점 점수 부여 및 분류',           ''),
        ('4단계  문서 작성',   '검토서 및 인계자료 생성',              ''),
    ]
    H = pad*2 + bh*2 + gap*2 + len(steps)*bh + (len(steps))*gap
    c = Canvas(W, H)
    f_lb, f_bd, f_tg = F(13, True), F(13), F(11)
    x, w = pad, W - pad*2
    cx = W // 2
    y = pad
    # 입력
    c.box(x, y, w, bh, fill=GRAY)
    c.text(cx, y+bh//2, 'MRI 리포트 원문', f_lb, anchor='mm')
    y += bh; c.arrow(cx, y+4*S, gap-4*S); y += gap
    # 단계
    lw, tw = int(w*0.26), int(w*0.20)
    for lab, body, tag in steps:
        c.box(x, y, w, bh)
        c.d.rounded_rectangle([x, y, x+lw, y+bh], radius=8*S, fill=GREEN,
                              corners=(True, False, False, True))   # 왼쪽만 둥글게
        c.d.rounded_rectangle([x, y, x+w, y+bh], radius=8*S, outline=LINE, width=1*S)
        c.d.line([x+lw, y, x+lw, y+bh], fill=LINE, width=1*S)
        c.text(x+lw//2, y+bh//2, lab, f_lb, anchor='mm')
        c.text(x+lw+14*S, y+bh//2, cut(c.d, body, f_bd, w-lw-tw-30*S), f_bd, anchor='lm')
        if tag:
            c.d.line([x+w-tw, y, x+w-tw, y+bh], fill=GREEN_D, width=1*S)
            c.text(x+w-tw//2, y+bh//2, tag, f_tg, fill=MUTE, anchor='mm')
        y += bh; c.arrow(cx, y+4*S, gap-4*S); y += gap
    # 출력
    c.box(x, y, w, bh, fill=GRAY)
    c.text(cx, y+bh//2, '담당자 화면   ·   후속 조사 시스템 인계 파일', f_lb, anchor='mm')
    c.im.resize((W//S*2, H//S*2), Image.LANCZOS).save(path)
    print('생성', path, W//S*2, 'x', H//S*2)

# ───────────────────────── 에이전트 2 ─────────────────────────
def agent2(path):
    pad, hh, rh, gap = 14*S, 40*S, 34*S, 22*S
    phases = [
        ('① 조사 설계', '4단계',  ['조사질문 수립 → 조사계획 수립 → 확장탐색 계획 → 조회과제 배분']),
        ('② 자료 조회', '15단계 · 9담당',
         ['1회차   금융위 보도자료 · 뉴스 · 제로인 공모 · 제로인 ETF · 협회통계   →  취합',
          '2회차   제로인 상세 · 협회통계(연계)   →  취합            ※ 1회차 결과 필요',
          '3회차   금융위 보도자료(후속) · 뉴스(후속)   →  취합      ※ 신규신호 확인']),
        ('③ 근거 정리', '1단계',  ['검증상태 부여 · 5개 영역 분류 · 근거번호 부여']),
        ('④ 대응안 작성', '3단계', ['사업기회 도출 → 전략 수립 → 최종 보고서']),
    ]
    bh = 46*S
    H = pad*2 + bh*2 + gap*2 + sum(hh + rh*len(r) for _, _, r in phases) + gap*len(phases)
    c = Canvas(W, H)
    f_ph, f_cnt, f_bd, f_rd = F(14, True), F(11), F(12), F(12, True)
    x, w = pad, W - pad*2
    cx = W // 2
    y = pad
    c.box(x, y, w, bh, fill=GRAY)
    c.text(cx, y+bh//2, '에이전트 1 인계 파일 (이슈 1건)', F(13, True), anchor='mm')
    y += bh; c.arrow(cx, y+4*S, gap-4*S); y += gap
    for name, cnt, rows in phases:
        h = hh + rh*len(rows)
        c.box(x, y, w, h)
        c.d.rounded_rectangle([x, y, x+w, y+hh], radius=8*S, fill=GREEN,
                              corners=(True, True, False, False))    # 위쪽만 둥글게
        c.d.rounded_rectangle([x, y, x+w, y+h], radius=8*S, outline=LINE, width=1*S)
        c.d.line([x, y+hh, x+w, y+hh], fill=LINE, width=1*S)
        c.text(x+18*S, y+hh//2, name, f_ph, anchor='lm')
        c.text(x+w-18*S, y+hh//2, cnt, f_cnt, fill=(70,90,55), anchor='rm')
        yy = y + hh
        for r in rows:
            head = r.split('   ')[0]
            rest = r[len(head):].strip()
            c.text(x+18*S, yy+rh//2, head, f_rd, anchor='lm')
            c.text(x+18*S+c.d.textlength(head, font=f_rd)+14*S, yy+rh//2,
                   cut(c.d, rest, f_bd, w-60*S-c.d.textlength(head, font=f_rd)), f_bd, anchor='lm')
            yy += rh
            if yy < y+h-2*S: c.d.line([x+14*S, yy, x+w-14*S, yy], fill=(225,225,225), width=1*S)
        y += h; c.arrow(cx, y+4*S, gap-4*S); y += gap
    c.box(x, y, w, bh, fill=GRAY)
    c.text(cx, y+bh//2, '담당자 화면   ·   핵심판단 / 현황 / 계획 / 추가확인사항  +  근거', F(13, True), anchor='mm')
    c.im.resize((W//S*2, H//S*2), Image.LANCZOS).save(path)
    print('생성', path, W//S*2, 'x', H//S*2)

import sys, os
d = os.path.dirname(os.path.abspath(__file__))
agent1(os.path.join(d, 'fig_agent1.png'))
agent2(os.path.join(d, 'fig_agent2.png'))

# ─────────────────── 공통 전체 구성 (두 보고서 공용) ───────────────────
def wholemap(path, active):      # active: 1 또는 2
    w, h = W, 150*S
    c = Canvas(w, h)
    f_b, f_s, f_t = F(13, True), F(11), F(10, True)
    pad = 14*S
    items = [('MRI 리포트', None), ('① 이슈 스크리닝', 1), ('② 조사 · 대응안 작성', 2), ('대응안 초안', None)]
    gapx = 30*S
    bw = (w - pad*2 - gapx*3) // 4
    bh = 56*S
    y = 30*S
    for k, (name, idx) in enumerate(items):
        x = pad + k*(bw+gapx)
        on = (idx == active)
        fill = GREEN if on else (GRAY if idx is None else WHITE)
        c.d.rounded_rectangle([x, y, x+bw, y+bh], radius=8*S, fill=fill,
                              outline=(LINE if not on else (90,130,70)), width=(1 if not on else 3)*S)
        c.text(x+bw//2, y+bh//2, name, f_b if on or idx else f_s, anchor='mm')
        if on:
            c.text(x+bw//2, y+bh+16*S, '이 문서', f_t, fill=(90,130,70), anchor='mm')
        if k < 3:
            ax = x+bw+gapx//2
            c.d.line([x+bw+6*S, y+bh//2, ax+6*S, y+bh//2], fill=LINE, width=2*S)
            c.d.polygon([(ax+5*S, y+bh//2-5*S), (ax+5*S, y+bh//2+5*S), (ax+12*S, y+bh//2)], fill=LINE)
    c.text(w-pad, y+bh+16*S, '담당자 검수 후 사용', F(10), fill=MUTE, anchor='rm')
    c.im.resize((w//S*2, h//S*2), Image.LANCZOS).save(path)
    print('생성', path)

wholemap(os.path.join(d, 'fig_map1.png'), 1)
wholemap(os.path.join(d, 'fig_map2.png'), 2)
