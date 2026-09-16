#!/usr/bin/env python3
"""출처 대조 — 산출물이 인용한 파일이 KB 에 실제로 있는지 기계적으로 확인한다.

프롬프트 규칙으로는 출처의 진위를 보장할 수 없다는 것이 5차 실행에서 확인되었다.
`source_path` 가 `documents/upload/kb-` 로 시작해야 한다는 규칙을 넣자,
지어낸 레코드가 그 형식을 갖추고 나왔다. 판별 기준을 프롬프트에 적는 한
그 기준은 모델이 생산할 수 있는 문자열이다.

이 스크립트는 모델 출력을 보지 않는다. KB 에 올린 파일 목록과 대조할 뿐이다.

12차 실행에서 「KB 에 없음」이 처음으로 0 이 되었다. 그런데 조회는 한 번도 없었다.
파일명을 아예 쓰지 않으면 이 검사를 통과한다는 뜻이다. 그래서 두 가지를 더 센다.

  - **파일명 비율.** 인용이 「<자료원> 검색결과」로만 채워지면 대조할 것이 없다.
    12차는 15건 중 2건(13%)만 파일명이 있었다.
  - **도구 호출 대조.** 실행 로그의 `Calling tool:` 줄을 세어, SUCCESS 를 낸 소스가
    실제로 도구를 불렀는지 본다. **로그는 플랫폼이 쓴다. 모델이 통과시킬 수 없다.**
    12차 06F 는 `stage_note` 에 "총 15회 KB 호출"이라 적었고 로그의 호출 줄은 0 개였다.

사용법
    python verify_sources.py --kb <KB패키지_디렉터리> --run <실행출력.txt>

  --kb   소스별 하위 폴더(mri_policy/ mri_news/ …)에 업로드한 파일이 들어 있는 디렉터리.
         AIR Studio 에 올린 것과 같은 묶음이어야 한다.
         폴더를 주지 않은 소스의 인용은 "판정 불가"로 따로 센다 — 없다고 단정하지 않는다.
  --run  AIR Studio 실행 출력을 그대로 저장한 파일. JSON 여러 개가 섞여 있어도 된다.
         `Calling tool:` 줄이 포함된 전체 로그면 도구 호출 대조까지 함께 한다.
  --log  도구 호출 줄이 다른 파일에 있을 때만 쓴다. 생략하면 --run 을 쓴다.

종료 코드 0 = 세 검사를 모두 통과, 1 = 하나라도 걸림.
"""
import argparse, json, os, re, sys
from collections import OrderedDict

# 07 은 `source_paths` 를, 조회 노드는 `source_path` 를 쓴다. 둘 다 읽는다.
# 복수형을 놓치는 바람에 13차 실행이 「인용 0건」으로 통과했다.
PATH_RE  = re.compile(r'"source_path"\s*:\s*"([^"]*)"')
PATHS_RE = re.compile(r'"source_paths"\s*:\s*\[([^\]]*)\]')
SRC_RE  = re.compile(r'"source"\s*:\s*"(mri_[a-z0-9_]+)"')
KBID_RE = re.compile(r'documents/upload/kb-([0-9a-f]+)/')

# 화면 근거 절 한 줄:  **[E02]** 확인 · `08_주식보상_….txt`
EVID_RE  = re.compile(r'\[(E\d+)\][^\n`]*?·\s*`([^`\n]+)`')
NAMES_RE = re.compile(r'"source_names"\s*:\s*\[([^\]]*)\]')
# 플랫폼이 찍는 실제 도구 호출.  Calling tool: knowledge_base_search_kb_94eaa5b2
CALL_RE  = re.compile(r'^\s*Calling tool:\s*knowledge_base_search_kb_([0-9a-f]+)', re.M)
# 노드가 스스로 적은 실행 신고
TASKID_RE = re.compile(r'"task_id"\s*:\s*"([^"]+)"')
SRCF_RE   = re.compile(r'"source"\s*:\s*"(mri_[a-z0-9_]+)"')
STAT_RE   = re.compile(r'"status"\s*:\s*"([A-Z_]+)"')
FILE_EXT  = ('.txt', '.pdf', '.xlsx', '.csv', '.md', '.docx')


def load_manifest(kb_dir):
    """{파일명: 소속소스} · {소속소스: [파일명…]} · {kb ID: 소속소스} 를 만든다.

    폴더 이름을 `mri_news@94eaa5b2` 처럼 적으면 그 KB ID 를 함께 읽는다.
    그러면 인용된 경로의 `kb-XXXXXXXX` 조각으로 판정할 수 있다 —
    모델이 스스로 어느 KB 를 읽었다고 적은 값이므로 주장 소스보다 정확하다.
    """
    owner, by_source, by_kbid = {}, OrderedDict(), {}
    for entry in sorted(os.listdir(kb_dir)):
        sub = os.path.join(kb_dir, entry)
        if not os.path.isdir(sub):
            continue
        files = sorted(f for f in os.listdir(sub) if not f.startswith(".")
                       and f.lower() != "readme.txt")
        source, _, kbid = entry.partition("@")
        # 빈 폴더도 이름만으로 KB ID ↔ 소스 대응을 등록한다.
        # 파일 목록을 아직 못 받은 소스라도 도구 호출은 소스에 연결해서 세야 한다.
        if kbid:
            by_kbid[kbid] = source
        if not files:
            continue
        by_source[source] = files
        for f in files:
            owner[f] = source
    return owner, by_source, by_kbid


def collect_citations(run_text):
    """인용된 (경로, 직전에 선언된 source) 쌍을 등장 순서대로 모은다."""
    out, seen = [], set()
    hits = [(m.start(), m.group(1)) for m in PATH_RE.finditer(run_text)]
    for m in PATHS_RE.finditer(run_text):
        for raw in m.group(1).split(','):
            raw = raw.strip().strip('"')
            if raw:
                hits.append((m.start(), raw))
    for pos, path in sorted(hits):
        srcs = SRC_RE.findall(run_text[:pos])
        claimed = srcs[-1] if srcs else None
        key = (path, claimed)
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def collect_labels(run_text):
    """산출물이 출처 자리에 적은 **모든** 표기를 모은다.

    `source_path` 만 보면 파일명을 안 쓴 실행은 검사할 것이 없어 자동으로 통과한다.
    화면 근거 절의 표기와 `source_names` 까지 함께 세어야 그 상태가 드러난다.
    """
    labels = []
    for eid, label in EVID_RE.findall(run_text):
        labels.append(label.strip())
    if not labels:                       # 근거 절이 없으면 JSON 쪽에서 긁는다
        for blob in NAMES_RE.findall(run_text):
            labels += [x.strip().strip('"') for x in blob.split(',') if x.strip().strip('" ')]
    return labels


def classify_label(label, owner):
    base = os.path.basename(label)
    if base in owner or label.lower().endswith(FILE_EXT):
        return "파일명"
    if "MRI" in label and "원문" in label:
        return "MRI원문"
    if "검색결과" in label:
        return "자료원표기"
    if "미확인" in label or not label:
        return "출처미확인"
    return "기타"


def collect_declared(run_text):
    """노드가 스스로 적은 태스크 결과를 소스별로 모은다.

    결과는 수집 노드(06R1·06R2·06R3·06X)가 그대로 다시 실으므로 같은 태스크가
    여러 번 나온다. `task_id` 기준으로 마지막 것만 남긴다.
    """
    seg, last = TASKID_RE.split(run_text), {}
    # split 결과: [앞부분, id1, 본문1, id2, 본문2, …]
    for i in range(1, len(seg) - 1, 2):
        tid, body = seg[i], seg[i + 1][:900]
        src = SRCF_RE.search(body)
        st = STAT_RE.search(body)
        if src:
            last[tid] = (src.group(1), st.group(1) if st else "?")
    per = {}
    for tid, (src, st) in last.items():
        d = per.setdefault(src, {"tasks": 0, "SUCCESS": 0, "other": 0})
        d["tasks"] += 1
        if st == "SUCCESS":
            d["SUCCESS"] += 1
        else:
            d["other"] += 1
    return per


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--log", help="도구 호출 줄이 다른 파일에 있을 때만")
    args = ap.parse_args()

    owner, by_source, by_kbid = load_manifest(args.kb)
    if not owner:
        sys.exit(f"KB 디렉터리에 소스별 하위 폴더가 없다: {args.kb}")

    with open(args.run, encoding="utf-8", errors="replace") as fh:
        run_text = fh.read()
    citations = collect_citations(run_text)
    if args.log:
        with open(args.log, encoding="utf-8", errors="replace") as fh:
            log_text = fh.read()
    else:
        log_text = run_text

    print("KB 에 올라간 파일")
    for src, files in by_source.items():
        print(f"  {src:18} {len(files):3}건")
    print()

    missing, misfiled, ok, unjudged = [], [], [], []
    for path, claimed in citations:
        base = os.path.basename(path)
        if base in owner:
            if claimed and owner[base] != claimed:
                misfiled.append((path, claimed, owner[base]))
            else:
                ok.append((path, claimed))
        elif KBID_RE.search(path) and KBID_RE.search(path).group(1) in by_kbid:
            # 경로가 가리키는 KB 의 파일 목록은 갖고 있다. 그 목록에 없으면 없는 것이다.
            missing.append((path, claimed))
        elif claimed and claimed not in by_source:
            # 그 소스의 파일 목록을 받지 못했다. 없다고 말할 수 없다.
            unjudged.append((path, claimed))
        else:
            missing.append((path, claimed))

    print(f"인용된 출처 {len(citations)}건 — 일치 {len(ok)} · 소속불일치 {len(misfiled)} · "
          f"KB 에 없음 {len(missing)} · 판정불가 {len(unjudged)}")
    print()

    if missing:
        print("■ KB 에 없는 출처 — 조회로 나올 수 없는 값이다")
        for path, claimed in missing:
            print(f"    {path}   (주장 소스: {claimed or '미상'})")
        print()
    if misfiled:
        print("△ 파일은 있으나 다른 소스 소속 — 배선 또는 표기 확인 필요")
        for path, claimed, real in misfiled:
            print(f"    {os.path.basename(path)}   주장 {claimed} / 실제 {real}")
        print()

    if unjudged:
        print("? 판정 불가 — 이 소스의 파일 목록을 --kb 에 주지 않았다")
        for path, claimed in unjudged:
            print(f"    {path}   (주장 소스: {claimed})")
        print("    이 항목들은 없다는 뜻이 아니다. 해당 소스 폴더를 --kb 에 넣고 다시 돌린다.")
        print()

    # ── 검사 2. 파일명 비율 ─────────────────────────────────────────
    labels = collect_labels(run_text)
    buckets = {}
    for lab in labels:
        buckets.setdefault(classify_label(lab, owner), []).append(lab)
    named = len(buckets.get("파일명", []))
    total = len(labels)
    ratio = (named / total * 100.0) if total else 0.0

    print("■ 파일명 비율 — 대조할 수 있는 인용이 얼마나 되는가")
    if not total:
        print("    인용 표기를 찾지 못했다. 근거 절이 없는 출력이다.")
    else:
        for k in ("파일명", "MRI원문", "자료원표기", "출처미확인", "기타"):
            if buckets.get(k):
                print(f"    {k:8} {len(buckets[k]):3}건   {buckets[k][0][:46]}")
        print(f"    → 파일명 {named}/{total} = {ratio:.0f}%")
        print("    자료원 표기만 남으면 대조할 것이 없어 이 검사는 자동으로 통과한다.")
        print("    조회가 실제로 됐다면 꼬리 줄이 붙은 인용이 섞여 나온다.")
    print()

    # ── 검사 3. 도구 호출 대조 ──────────────────────────────────────
    calls = {}
    for kbid in CALL_RE.findall(log_text):
        calls[kbid] = calls.get(kbid, 0) + 1
    declared = collect_declared(run_text)
    by_source_calls = {}
    for kbid, n in calls.items():
        by_source_calls[by_kbid.get(kbid, f"kb-{kbid}(목록없음)")] = n

    print("■ 도구 호출 대조 — 로그는 플랫폼이 쓴다. 모델이 통과시킬 수 없다.")
    # 노드가 실행된 흔적(Thinking:/Done:/Routing)이 있는데 호출 줄이 0 이면
    # 그것은 「로그를 안 준 것」이 아니라 **한 번도 부르지 않은 것**이다.
    ran = bool(re.search(r'^\s*(Done:|Thinking:|Routing )', log_text, re.M))
    if not calls and not ran:
        print("    실행 흔적도 호출 줄도 없다. 전체 로그를 --run 또는 --log 로 주면")
        print("    이 검사를 한다. 이번에는 건너뛴다.")
        lied = []
    else:
        if not calls:
            print("    ✗ 노드는 실행됐는데 `Calling tool:` 줄이 0 개다.")
            print("      이 실행에서 지식베이스 도구는 한 번도 호출되지 않았다.")
            print("      SUCCESS 를 낸 레코드는 전부 조회 결과가 아니다.")
        lied = []
        srcs = sorted(set(list(declared.keys()) + list(by_source_calls.keys())))
        print(f"    {'소스':22} {'실제 호출':>9} {'신고 태스크':>10} {'SUCCESS':>9}")
        for src in srcs:
            n = by_source_calls.get(src, 0)
            d = declared.get(src, {"tasks": 0, "SUCCESS": 0})
            mark = ""
            if d["SUCCESS"] > 0 and n == 0:
                mark = "  ✗ 호출 없이 SUCCESS"
                lied.append((src, d["SUCCESS"]))
            print(f"    {src:22} {n:>9} {d['tasks']:>10} {d['SUCCESS']:>9}{mark}")
        if lied:
            print()
            print("    ✗ 표시된 소스는 도구를 한 번도 부르지 않고 SUCCESS 를 냈다.")
            print("      그 레코드의 내용은 조회 결과가 아니다. 상류 입력을 옮겨 적은 것이다.")
    print()

    # ── 판정 ────────────────────────────────────────────────────────
    fail = []
    if missing:
        fail.append(f"KB 에 없는 출처 {len(missing)}건")
    if total and ratio < 30.0:
        fail.append(f"파일명 비율 {ratio:.0f}%")
    if lied:
        fail.append(f"호출 없이 SUCCESS 를 낸 소스 {len(lied)}개")

    if fail:
        print("판정: " + " · ".join(fail) + ". 그대로 쓸 수 없다.")
        return 1
    print("판정: 세 검사를 모두 통과했다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
