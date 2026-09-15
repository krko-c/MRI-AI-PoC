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
  --run  AIR Studio 실행 출력을 그대로 저장한 파일. JSON 여러 개가 섞여 있어도 된다.

종료 코드 0 = 인용된 출처가 전부 KB 에 있음, 1 = 없는 출처가 있음.
"""
import argparse, json, os, re, sys
from collections import OrderedDict

PATH_RE = re.compile(r'"source_path"\s*:\s*"([^"]*)"')
SRC_RE  = re.compile(r'"source"\s*:\s*"(mri_[a-z0-9_]+)"')


def load_manifest(kb_dir):
    """{파일명: 소속소스} 와 {소속소스: [파일명…]} 을 만든다."""
    owner, by_source = {}, OrderedDict()
    for entry in sorted(os.listdir(kb_dir)):
        sub = os.path.join(kb_dir, entry)
        if not os.path.isdir(sub):
            continue
        files = sorted(f for f in os.listdir(sub) if not f.startswith(".")
                       and f.lower() != "readme.txt")
        if not files:
            continue
        by_source[entry] = files
        for f in files:
            owner[f] = entry
    return owner, by_source


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

    owner, by_source = load_manifest(args.kb)
    if not owner:
        sys.exit(f"KB 디렉터리에 소스별 하위 폴더가 없다: {args.kb}")

    with open(args.run, encoding="utf-8", errors="replace") as fh:
        citations = collect_citations(fh.read())

    print("KB 에 올라간 파일")
    for src, files in by_source.items():
        print(f"  {src:18} {len(files):3}건")
    print()

    missing, misfiled, ok = [], [], []
    for path, claimed in citations:
        base = os.path.basename(path)
        if base not in owner:
            missing.append((path, claimed))
        elif claimed and owner[base] != claimed:
            misfiled.append((path, claimed, owner[base]))
        else:
            ok.append((path, claimed))

    print(f"인용된 출처 {len(citations)}건 — 일치 {len(ok)} · 소속불일치 {len(misfiled)} · "
          f"KB 에 없음 {len(missing)}")
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

    if missing:
        print("판정: 산출물에 조회되지 않은 출처가 섞여 있다. 그대로 쓸 수 없다.")
        return 1
    print("판정: 인용된 출처가 모두 KB 에 있다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
