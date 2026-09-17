#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""㉒ 도구 이름을 돌려 쓰지 않는다 + 꼬리 줄의 변형을 받는다.

28차에서 정책 담당이 **처음으로 제대로 조회했다.**
이슈 원문에 없는 사실이 자료원에서 새로 나왔다 —
「개정 상법 제341조의4」 「매년 주주총회 승인」 「5천만원 이하 과태료」 「2026.3.6 시행」.
전부 업로드된 보도자료 원문에 있고, 이슈 원문에는 하나도 없다.

그런데 그 다음 노드가 무너졌다. 자기 도구가 목록에 없자
**옆 노드들의 도구 이름을 차례로 돌려 가며 시도했다.**

    kb_94eaa5b2 → kb_d1d6e7f1 → kb_c210cfea → kb_a2569d17 → kb_cf938211

이 다섯은 뉴스·제로인공모·제로인ETF·제로인상세·협회통계 담당의 도구다.
그리고 스스로 「KB_TOOL_NAME_CIRCULAR_REFERENCE」라는 이름을 붙이고
**자기 것이 아닌 태스크까지 스물두 개를 한꺼번에 포기했다.**

14차의 「옆 노드 도구를 부른다」가 다른 모양으로 돌아온 것이다.
한 번 실패한 것은 한 번 실패로 적으면 된다. 돌려 쓰지 않고, 남의 몫을 포기하지 않는다.

함께: 꼬리 줄이 여러 줄로 오거나 경로가 따로 오는 형태를 받지 못해
파일명이 왔는데도 `source_path` 가 비었다.

    python3 patch_no_tool_roulette.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGETS = ['variant_report_call.json', 'variant_report.json',
           'variant_D_report.json', 'variant_D_on_B_report.json',
           'MRI_Agent2_Research_Response_v2.json']

OLD = """## 11. 도구가 실패하면"""

NEW = """## 11. 도구 이름을 돌려 쓰지 않는다 — HARD RULE

**네 도구 목록에 네 이름이 없으면, 거기서 끝이다.**
다른 이름을 시도하지 않는다. 목록에 있는 아무 이름이나 대신 부르지 않는다.

직전 실행에서 한 노드가 자기 이름을 못 찾자 다섯 개를 차례로 돌려 가며 시도했다.

    kb_94eaa5b2 → kb_d1d6e7f1 → kb_c210cfea → kb_a2569d17 → kb_cf938211

**그 다섯은 다른 조회 담당들의 도구다.** 남의 자료원을 부른 것이고,
어느 자료원에서 나온 사실인지 구분할 수 없게 만든다.

이럴 때 할 일은 하나뿐이다.

    "status": "RETRIEVAL_ERROR",
    "error_detail": "<my_kb_tool 에 적은 이름> 이 내 도구 목록에 없다"

**그리고 네 태스크만 그렇게 표시한다.**
직전 실행에서 그 노드가 자기 것이 아닌 태스크까지 **스물두 개를 한꺼번에 포기했다.**
뒤 노드들이 아직 부르지 않은 것까지 「실행 불가」로 적었다.

- **남의 소스 태스크를 실패로 표시하지 않는다.** 그것은 그 담당이 부를 몫이다
- **워크플로 전체를 중단시키는 판단을 하지 않는다.** 너는 한 자료원의 담당이다
- 「시스템 오류」·「재실행 필요」 같은 진단을 쓰지 않는다. 사실만 적는다

## 12. 도구가 실패하면"""

OLD_FOOT = """- `source_path` 는 꼬리의 괄호 안 경로에 파일명을 붙인 값이다. 꼬리가 없으면 `null`."""

NEW_FOOT = """- `source_path` 는 꼬리의 괄호 안 경로에 파일명을 붙인 값이다. 꼬리가 없으면 `null`.
  **꼬리의 모양은 한 가지가 아니다.** 아래 형태가 모두 온다. 모두 받는다.

      - Source: 파일명.txt (documents/upload/kb-xxxxxxxx/)     ← 한 줄에 함께
      - 파일명1.pdf
      - 파일명2.pdf
      - 경로: documents/upload/kb-xxxxxxxx/                     ← 경로가 따로

  **경로가 따로 오면 그 경로를 각 파일명에 붙인다.** 파일명이 여럿이면
  레코드마다 그 사실이 나온 파일 하나를 고른다. 고를 수 없으면 둘 다 적는다.
  **파일명이 왔는데 `source_path` 를 비우지 않는다.** 그것은 확인할 수 있는 것을
  확인할 수 없게 만드는 일이다."""


def patch(path):
    d = json.load(open(path, encoding='utf-8'))
    a = b = 0
    for x in d['MapValue']['FunctionMaps']:
        p = x.get('prompt') or ''
        if 'my_kb_tool' not in p:
            continue
        if OLD in p and '도구 이름을 돌려 쓰지 않는다' not in p:
            p = p.replace(OLD, NEW, 1); a += 1
        if OLD_FOOT in p and '꼬리의 모양은 한 가지가 아니다' not in p:
            p = p.replace(OLD_FOOT, NEW_FOOT, 1); b += 1
        x['prompt'] = p
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"{os.path.basename(path):<36} 순회금지 {a} · 꼬리변형 {b}")


if __name__ == '__main__':
    for f in (sys.argv[1:] or [os.path.join(HERE, t) for t in TARGETS]):
        if os.path.exists(f):
            patch(f)
