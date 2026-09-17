#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⑲ 자기신고를 빼고, 형식 검사를 되살린다.

이번 실행에서 조회 노드가 스물한 번 `"kb_tool_called": true` 를 적었다.
그리고 낸 것은 이렇다.

    06E 정책   「3차 개정상법 시행으로 자기주식을 임직원 보상 재원으로 활용 가능」
               → 정책 KB 전 파일에 `자기주식` 0건 · `개정상법` 0건 · `0.6%` 0건
    06F 뉴스   「은행권: 신한·국민은행: SK하이닉스, 삼성전자 등 …」
               → 기사 문장이 아니라 MRI 원문의 개조식 불릿 그대로
    06C ETF    KODEX 미국S&P500 · KODEX 200 · TIGER 글로벌리츠 · ARIRANG 고배당주
               → 코퍼스에 ARIRANG 0건. KODEX 는 삼성, TIGER 는 미래에셋 브랜드.
                 당사 브랜드는 HANARO(50건). 실제 레코드는 한 줄짜리 카탈로그다 —
                 `구분=ETF | 상품ID=K55232C57764 | 상품명=NH-AmundiHANARO200… | 운용사=NH-Amundi운용`
    06C 경로   `zeroin_etf/kodex_us_sp500.pdf`
               → `zeroin_etf/` 0건 · 「상품설명서」 0건. **경로까지 지어냈다.**

그 넷이 `VERIFIED` 로 올라가 보고서의 「확인 4건 · 파일명 있는 근거 4건」이 됐다.
**보고서에서 가장 단단해 보이는 근거가 전부 날조였다.**

⑰에서 내가 되살린 `retrieval_proof` 가 이것을 막지 못했다. 막을 수 없는 칸이다.
지운 섹션이 이미 그렇게 적고 있었다 —
**「자기 점검 필드는 자기가 지어낸 것을 잡지 못한다. 그래서 형식으로 검사한다.」**
되살려야 했던 것은 자기신고 칸이 아니라 그 다음 문단, 형식 검사였다.

  - 뺀다: `retrieval_proof` 자기신고 칸
  - 남긴다: `RETRIEVAL_NOT_EXECUTED` (부르지 않은 자리를 보이게 하는 상태값)
  - 되살린다: 「레코드가 도구에서 나왔는지 형식으로 검사한다」

    python3 patch_source_check.py
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGETS = ['variant_report_call.json', 'variant_report.json',
           'variant_D_report.json', 'variant_D_on_B_report.json']

OLD_PROOF = """이것을 `NO_RESULT` 나 `SUCCESS` 로 바꾸지 않는다. **바꾸면 그 자리가 영영 안 보인다.**
반대로 실제로 부른 결과에는 레코드마다 이 칸을 단다.

    "retrieval_proof": {"kb_tool_called": true, "source_id": "<네 소스 ID>"}

이 칸은 **불렀다는 사실의 기록이지 정확하다는 보증이 아니다.**
부르지 않고 이 칸을 `true` 로 적는 것이 이 워크플로에서 가장 나쁜 한 줄이다.
"""

NEW_PROOF = """이것을 `NO_RESULT` 나 `SUCCESS` 로 바꾸지 않는다. **바꾸면 그 자리가 영영 안 보인다.**

`retrieval_proof` · `kb_tool_called` · `records_derived_only_from_tool_output` 처럼
**「나는 제대로 했다」고 스스로 적는 칸을 만들지 않는다.**
직전 실행에서 조회 노드가 그 칸을 스물한 번 `true` 로 적고, 도구는 부르지 않았다.
**자기 점검 칸은 자기가 지어낸 것을 잡지 못한다.** 아래 형식 검사가 그 자리를 대신한다.
"""

ANCHOR = '## 8. 도구를 다 부른 다음, JSON 하나를 낸다 — HARD RULE'

SEC_CHECK = """## 8. 레코드가 도구에서 나왔는지 형식으로 검사한다 — HARD RULE

「도구 출력이 아닌 것을 쓰지 마라」는 금지는 이미 위에 있고, 직전 실행에서 지켜지지 않았다.
**그래서 내기 전에 형식으로 검사한다.** 레코드마다 두 가지를 본다.

**1) `answer_excerpt` 가 도구가 돌려준 `answer` 안에 글자 그대로 있는가.**

없으면 그 레코드는 조회 결과가 아니다. 지운다.
직전 실행에서 정책 담당이 낸 세 문장이 이랬다.

    「3차 개정상법 시행(2026.3월)으로 자기주식을 임직원 보상 재원으로 활용 가능」
    「국내 상장사 RSU 도입률 0.6%로 일본·미국·독일(15–65%) 대비 낮아…」

정책 자료원 전 파일에 `자기주식` 도 `개정상법` 도 `0.6%` 도 **한 번도 안 나온다.**
**이 문장들은 이슈 원문에 있던 문장이다.** 자료원에서 온 것이 아니다.
뉴스 담당도 같았다 — 낸 문장이 기사 문장이 아니라 **이슈 원문의 개조식 불릿 그대로**였다.
불렀다면 기사 본문이 왔을 것이다.

**이슈 원문의 사실을 없애라는 뜻이 아니다.** 그것은 07 이 별도 경로로 근거에 싣는다.
네가 조회 레코드로 만들 것이 아닐 뿐이다. **조회하지 않은 것을 조회한 것처럼 내지 않는다.**

**2) `source_path` 가 꼬리 줄에서 옮겨 온 값인가.**

`source_path` 는 **도구가 주는 값이지 네가 쓰는 값이 아니다.**
위 「도구가 돌려주는 것」의 `source_footer` 에서 옮겨 적은 값이면 그대로 낸다.
그렇지 않으면 **도구 출력이 아니다. 그 레코드를 지운다.**

직전 실행에서 제로인 담당이 이렇게 냈다.

    "source_footer": "- Source: KODEX 미국S&P500 상품 설명서 (zeroin_etf/kodex_us_sp500.pdf)"
    "source_path":   "zeroin_etf/kodex_us_sp500.pdf"

자료원에 `zeroin_etf/` 라는 경로도, 「상품 설명서」라는 문서도 **하나도 없다.**
꼬리 줄의 형식만 흉내 낸 것이다. **경로를 지어내면 사람이 확인할 방법이 사라진다.**
비어 있으면 확인할 수 있지만, 지어낸 출처는 **확인된 사실로 보고서에 실린다.**
실제로 그 네 건이 그 보고서에서 가장 단단해 보이는 근거가 됐다.

꼬리가 없으면 `source_path` 를 `null` 로 둔다. **채워 넣지 않는다.**

**3) 내용에도 같은 기준을 적용한다.**

상품명·브랜드·기관명·조문 번호·가입 연령·납입 한도처럼
「알고 있으니 쓸 수 있는」 내용일수록 의심한다. 도구가 그 문장을 돌려주지 않았다면 쓰지 않는다.
직전 실행에서 **당사 상품을 물었는데 다른 회사 브랜드 넷을 냈다.**
자료원을 봤다면 나올 수 없는 답이고, 자료원의 레코드는 그런 모양도 아니다.
**당사 상품의 표기는 자료원이 쓰는 대로만 쓴다. 네가 아는 표기로 바꾸지 않는다.**

"""


def patch(path):
    d = json.load(open(path, encoding='utf-8'))
    hit = 0
    for x in d['MapValue']['FunctionMaps']:
        p = x.get('prompt') or ''
        if 'my_kb_tool' not in p or '형식으로 검사한다' in p:
            continue
        # 절 번호는 판마다 다르다. 제목으로 찾는다.
        m = re.search(r'^## \d+\. 도구를 다 부른 다음.*$', p, re.M)
        assert m, x.get('COL_NAME')
        # ⑰이 없는 판(자기신고 칸이 애초에 없다)에는 그 교체를 건너뛴다
        p = p.replace(OLD_PROOF, NEW_PROOF, 1)
        p = p[:m.start()] + SEC_CHECK + p[m.start():]
        n = [0]
        def repl(m):
            n[0] += 1
            return f"## {n[0]}. {m.group(2)}"
        x['prompt'] = re.sub(r'^## (\d+)\. (.*)$', repl, p, flags=re.M)
        hit += 1
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"{os.path.basename(path):<30} 조회 노드 {hit}개")


if __name__ == '__main__':
    for f in (sys.argv[1:] or [os.path.join(HERE, t) for t in TARGETS]):
        if os.path.exists(f):
            patch(f)
