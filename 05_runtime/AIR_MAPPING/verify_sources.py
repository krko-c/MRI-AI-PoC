#!/usr/bin/env python3
"""출처 대조 — 산출물이 인용한 파일이 KB 에 실제로 있는지 기계적으로 확인한다.

프롬프트 규칙으로는 출처의 진위를 보장할 수 없다는 것이 5차 실행에서 확인되었다.
`source_path` 가 `documents/upload/kb-` 로 시작해야 한다는 규칙을 넣자,
지어낸 레코드가 그 형식을 갖추고 나왔다. 판별 기준을 프롬프트에 적는 한
그 기준은 모델이 생산할 수 있는 문자열이다.

이 스크립트는 모델 출력을 보지 않는다. KB 에 올린 파일 목록과 대조할 뿐이다.

사용법
    python verify_sources.py --kb <KB패키지_디렉터리> --run <실행출력.txt>

  --kb   소스별 하위 폴더(mri_policy/ mri_news/ …)에 업로드한 파일이 들어 있는 디렉터리.
         AIR Studio 에 올린 것과 같은 묶음이어야 한다.
         폴더를 주지 않은 소스의 인용은 "판정 불가"로 따로 센다 — 없다고 단정하지 않는다.
  --run  AIR Studio 실행 출력을 그대로 저장한 파일. JSON 여러 개가 섞여 있어도 된다.

종료 코드 0 = 인용된 출처가 전부 KB 에 있음, 1 = 없는 출처가 있음.
"""
import argparse, json, os, re, sys
from collections import OrderedDict

PATH_RE = re.compile(r'"source_path"\s*:\s*"([^"]*)"')
SRC_RE  = re.compile(r'"source"\s*:\s*"(mri_[a-z0-9_]+)"')
KBID_RE = re.compile(r'documents/upload/kb-([0-9a-f]+)/')


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
        if not files:
            continue
        source, _, kbid = entry.partition("@")
        by_source[source] = files
        if kbid:
            by_kbid[kbid] = source
        for f in files:
            owner[f] = source
    return owner, by_source, by_kbid


def collect_citations(run_text):
    """인용된 (경로, 직전에 선언된 source) 쌍을 등장 순서대로 모은다."""
    out, seen = [], set()
    for m in PATH_RE.finditer(run_text):
        path = m.group(1)
        before = run_text[:m.start()]
        srcs = SRC_RE.findall(before)
        claimed = srcs[-1] if srcs else None
        key = (path, claimed)
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", required=True)
    ap.add_argument("--run", required=True)
    args = ap.parse_args()

    owner, by_source, by_kbid = load_manifest(args.kb)
    if not owner:
        sys.exit(f"KB 디렉터리에 소스별 하위 폴더가 없다: {args.kb}")

    with open(args.run, encoding="utf-8", errors="replace") as fh:
        citations = collect_citations(fh.read())

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

    if missing:
        print("판정: 산출물에 조회되지 않은 출처가 섞여 있다. 그대로 쓸 수 없다.")
        return 1
    print("판정: 인용된 출처가 모두 KB 에 있다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
