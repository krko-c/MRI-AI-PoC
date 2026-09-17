#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""㉑ 자료 카드의 구획을 구분한다 + 묶인 항목을 쪼개지 않는다.

27차는 날조가 없었다. 인용한 파일이 전부 실재하고 수치도 원문과 맞는다.
그러나 네 가지가 변형됐다.

  1. 해석을 사실로 바꿨다
     원문 [ASSET-MANAGEMENT IMPLICATION]
       「RSU·성과주식 수령 이후의 분산투자, 세금·현금화, 장기자산배분,
         연금전환 등 임직원 대상 자산관리 니즈가 구조적으로 커질 수 있다」
     산출물  「RSU 수령 이후 구조적 자산관리 니즈가 발생한다」
     **「커질 수 있다」가 「발생한다」가 됐다.** 전망이 사실이 됐다.

  2. 출처를 다른 파일로 적었다
     위 문장은 08 파일에서 왔는데 20 파일이라고 적었다.
     담당자가 20 파일을 열면 그 문장이 없다.

  3. 조사 목적 메모를 사실로 썼다
     원문 [RESEARCH USE] 「…B2B 자산관리 모델을 확인」(무엇을 볼지 적은 메모)
     산출물 본문에 그대로 사실처럼 실렸다.

  4. 묶인 항목을 쪼갰다
     원문 「5대 서비스는 …, 임직원 자산관리·금융교육, 커넥트 포럼, 퇴직연금」
     산출물 「5대 핵심 서비스는 (1)… (3) 임직원 자산관리, (4) 임직원 금융교육,
             (5) 커넥트 포럼, (6) 퇴직연금이다」
     **「5대」라고 쓰고 여섯을 나열했다.** 자체 모순이다.

⑲가 「없는 것을 만들지 마라」를 막았다면, 이것은 「있는 것을 바꾸지 마라」다.

    python3 patch_card_section.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGETS = ['variant_report_call.json', 'variant_report.json',
           'variant_D_report.json', 'variant_D_on_B_report.json',
           'MRI_Agent2_Research_Response_v2.json']

OLD = """**3) 내용에도 같은 기준을 적용한다.**"""

NEW = """**3) 자료 카드의 어느 구획에서 온 문장인지 본다.**

이 자료원의 문서는 구획으로 나뉘어 있다. **구획마다 성격이 다르다.**

    [KEY EVIDENCE]                  보도가 전한 사실.        ← 여기서만 근거를 만든다
    [ASSET-MANAGEMENT IMPLICATION]  자산운용 관점의 풀이.    ← 해석이다
    [RESEARCH USE]                  왜 이 자료를 넣었는지.   ← 메모다
    [SEARCH KEYWORDS]               색인용 낱말.

**해석과 메모는 사실이 아니다. 근거로 쓰지 않는다.**
직전 실행에서 해석 구획의 「…자산관리 니즈가 구조적으로 **커질 수 있다**」를
「구조적 자산관리 니즈가 **발생한다**」로 바꿔 냈다. 전망이 사실이 됐다.

- **「~할 수 있다」·「~전망」·「~가능성」을 「~한다」로 바꾸지 않는다.**
- 조사 목적을 적은 메모를 본문 사실로 옮기지 않는다.
- 해석을 쓰고 싶으면 그대로 두고 `status` 를 올리지 않는다.

**4) 묶여 있는 것을 쪼개지 않고, 나뉜 것을 합치지 않는다.**

직전 실행에서 원문 「**5대** 서비스는 주식보상제도 컨설팅, 법인 여유자금 운용,
**임직원 자산관리·금융교육**, 커넥트 포럼, 퇴직연금」을 받아
「임직원 자산관리」와 「임직원 금융교육」 **둘로 나눠 여섯 개**로 냈다.
그러면서 앞에는 「5대」라고 그대로 적었다. **자체 모순이다.**

항목 수·순서·묶음을 도구가 준 그대로 낸다. 읽기 좋게 고치지 않는다.

**5) 출처는 그 문장이 나온 조회의 꼬리다.**

한 차례에 여러 번 부르면 결과가 섞인다. **레코드마다 그 문장이 나온 조회의
꼬리 줄을 붙인다.** 다른 조회의 꼬리를 가져다 붙이지 않는다.
직전 실행에서 한 파일에서 온 문장에 **다른 파일 이름**이 붙었다.
그 파일을 열면 그 문장이 없다. **없는 출처를 만든 것과 같은 결과다.**

**6) 내용에도 같은 기준을 적용한다.**"""


def patch(path):
    d = json.load(open(path, encoding='utf-8'))
    hit = 0
    for x in d['MapValue']['FunctionMaps']:
        p = x.get('prompt') or ''
        if OLD not in p or '자료 카드의 어느 구획' in p:
            continue
        x['prompt'] = p.replace(OLD, NEW, 1)
        hit += 1
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"{os.path.basename(path):<36} 조회 노드 {hit}개")


if __name__ == '__main__':
    for f in (sys.argv[1:] or [os.path.join(HERE, t) for t in TARGETS]):
        if os.path.exists(f):
            patch(f)
