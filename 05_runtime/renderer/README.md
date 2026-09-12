# MRI 최종 대응안 → Word 변환기

10번 노드(`10 ISSUE FINAL MRI RESPONSE`)의 출력 JSON을 기존 MRI 제출 양식의 `.docx`로 변환한다.
AIR Studio 채팅창의 결과를 담당자가 그대로 열어 수정·제출할 수 있게 하는 것이 목적이다.

같은 변환 규칙으로 **두 가지 버전**이 있다.

| | 파일 | 필요 환경 |
|---|---|---|
| **브라우저판** | `mri_docx_tool.html` | 없음. 파일을 더블클릭하면 끝 |
| 명령줄판 | `render_mri_docx.js` | Node.js + `npm install` |

**담당자에게 배포할 때는 브라우저판을 쓴다.** Python·Node 설치가 보안상 막힌 PC에서도
동작하고, 외부 라이브러리를 전혀 불러오지 않아 인터넷이 끊겨 있어도 된다.
입력한 내용은 브라우저 안에서만 처리되며 어디로도 전송되지 않는다.

## 브라우저판 사용

1. `mri_docx_tool.html` 을 더블클릭해 연다 (Chrome, Edge 등)
2. AIR Studio 채팅창 맨 아래 코드블록의 `{` 부터 마지막 `}` 까지 복사해 왼쪽 칸에 붙여넣는다
3. 오른쪽 미리보기로 내용을 확인하고 **Word 파일로 저장** 을 누른다

파일 저장이 막힌 PC라면 **서식 그대로 복사** 를 눌러 한글이나 Word에 바로 붙여넣는다.
굵기와 들여쓰기가 유지된다.

`.docx` 는 실제로는 ZIP 이므로, 브라우저판은 ZIP 생성과 OOXML 작성을 자체 구현했다.
외부 CDN을 쓰지 않는 이유다.

## 명령줄판 설치

```bash
cd 05_runtime/renderer
npm install          # docx 패키지만 필요
```

## 명령줄판 사용

```bash
# 제출본 (기본)
node render_mri_docx.js result.json -o 주제별_자회사_의견.docx

# 내부 검수용 — 추적정보 부록 포함
node render_mri_docx.js result.json --trace -o 검수용.docx

# 샘플로 동작 확인
npm run sample
```

`result.json` 은 10번 노드가 반환한 JSON을 그대로 저장한 파일이다.
한 겹 감싸여 있어도(`output` / `result` / `data`) 자동으로 벗겨낸다.

## 변환 규칙

본문은 `final_report_text` 를 그대로 옮긴다. 요약하거나 문장을 고치지 않는다.

| 원문 표기 | Word 서식 |
|---|---|
| `<#번호 주제명>` | 굵게 13pt + 아래 실선 |
| `□ 대제목` | 굵게 11pt, 위 여백 |
| `○ 주요 항목` | 들여쓰기 400, 내어쓰기 200 |
| `- 세부 항목` | 들여쓰기 800, 내어쓰기 200 |
| 마커 없는 줄 | 앞 항목의 이어지는 문장으로 처리 |

글꼴은 맑은 고딕, 여백은 상하좌우 2cm.

`final_report_text` 가 없으면 `final_report` 의 A–F 구조에서 본문을 복원하고 경고를 출력한다.
이 경로는 차선책이며 문장 다듬기가 필요하다. 정상 동작이라면 `final_report_text` 가 항상 있어야 한다.

## `--trace` 부록

새 페이지에 표로 덧붙인다. 제출본에는 넣지 않는 것이 기본이다.

- 최종 준비도
- 사용된 근거 / 사업기회 / 전략 개수
- 원문 핵심 주제 — 반영된 것과 확보하지 못한 것

원문 주제 회수 현황은 "원문을 축소하지 않았다"를 보이는 자료이므로 내부 검수와 PoC 시연에 쓴다.

## 한글(HWP) 변환

Word로 만든 뒤 한글에서 열어 HWP로 저장한다. HWP를 직접 생성하는 것보다 안정적이다.

## 확인 상태

- 명령줄판: 샘플 입력으로 생성 확인, OOXML 스키마 검증 통과(문단 52개).
- 브라우저판: Chromium으로 실제 페이지를 띄워 변환시킨 `.docx` 가
  ZIP 무결성·OOXML 스키마 검증 통과(문단 51개). JS 오류 없음. 400px 폭에서 가로 스크롤 없음.
  - 검증 과정에서 `w:pPr` 자식 요소 순서 위반을 발견해 수정했다.
    순서는 `pageBreakBefore -> pBdr -> spacing -> ind` 로 스키마가 강제한다.
- **이 개발 환경에서는 LibreOffice가 동작하지 않아 시각적 렌더링 확인은 하지 못했다.**
  Word에서 한 번 열어 확인할 것.

## 파일

```
mri_docx_tool.html              브라우저판 — 설치 없이 더블클릭
render_mri_docx.js              명령줄판
package.json                    명령줄판 의존성 (docx)
sample/sample_output_10.json    양식 확인용 샘플 입력 — 실제 수치·기업명 없음
```
