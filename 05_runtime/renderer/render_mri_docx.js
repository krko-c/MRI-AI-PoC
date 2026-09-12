#!/usr/bin/env node
/**
 * MRI 최종 대응안 → Word(.docx) 변환기
 *
 * 입력 : 10 ISSUE FINAL MRI RESPONSE 노드의 출력 JSON
 * 출력 : 기존 MRI 제출 양식(현황 / 계획)의 .docx
 *
 *   node render_mri_docx.js <input.json> [-o output.docx] [--trace]
 *
 * --trace 를 주면 추적정보(근거·전략 ID, 원문 주제 회수 현황)를 부록으로 덧붙인다.
 * 제출본에는 넣지 않는 것이 기본이므로 기본값은 미포함이다.
 */
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType,
} = require("docx");

const FONT = "맑은 고딕";
const SZ = { title: 26, head: 22, body: 21, small: 19 }; // half-points

// ---------- 입력 ----------
function parseArgs(argv) {
  const a = { input: null, out: null, trace: false };
  for (let i = 2; i < argv.length; i++) {
    const v = argv[i];
    if (v === "-o" || v === "--out") a.out = argv[++i];
    else if (v === "--trace") a.trace = true;
    else if (!a.input) a.input = v;
  }
  return a;
}

function loadReport(file) {
  const raw = JSON.parse(fs.readFileSync(file, "utf8"));
  // 노드 출력이 한 겹 더 감싸여 있는 경우를 허용한다
  const r = raw.final_report_text || raw.final_report ? raw
          : raw.output || raw.result || raw.data || raw;
  if (!r.final_report_text && !r.final_report) {
    throw new Error("final_report_text 도 final_report 도 없습니다. 10번 노드의 출력 JSON이 맞는지 확인하십시오.");
  }
  return r;
}

// ---------- 본문 조립 ----------
/** final_report_text 가 없을 때 A–F 구조에서 본문을 복원한다 (차선책) */
function textFromStructure(r) {
  const f = r.final_report || {};
  const L = [];
  const title = [r.issue_no, r.issue_title].filter(Boolean).join(" ");
  L.push(`<${title || r.issue_id || "MRI 대응안"}>`, "");

  if (f.A_core_judgment) { L.push("□ 핵심 판단", ` ○ ${f.A_core_judgment}`, ""); }

  const domainName = {
    industry_customer: "산업·고객", policy_regulation: "정책·제도",
    financial_competitors: "금융업권·경쟁사",
    asset_management_fund_market: "자산운용·펀드시장", company_status: "당사 현황",
  };
  for (const b of f.B_current_status_and_market_analysis || []) {
    L.push(`□ (현황) ${domainName[b.domain] || b.domain || ""} ${b.headline || ""}`.trim());
    for (const p of b.points || []) {
      if (p.main_point) L.push(` ○ ${p.main_point}`);
      for (const d of p.details || []) L.push(`  - ${d}`);
    }
    L.push("");
  }
  const byBlock = {};
  for (const a of f.E_action_plan || []) {
    const k = a.visible_block || "우선 추진과제";
    (byBlock[k] = byBlock[k] || []).push(a);
  }
  for (const [blk, items] of Object.entries(byBlock)) {
    L.push(`□ (계획) ${blk}`);
    for (const a of items) {
      if (a.action) L.push(` ○ ${a.action}`);
      if (a.dependency) L.push(`  - ${a.dependency}`);
    }
    L.push("");
  }
  if ((f.F_additional_checks || []).length) {
    L.push("□ 추가 확인사항");
    for (const c of f.F_additional_checks) {
      L.push(typeof c === "string" ? ` ○ ${c}` : ` ○ ${c.item || c.statement || JSON.stringify(c)}`);
    }
  }
  return L.join("\n");
}

/** □ / ○ / - 계층 텍스트를 Word 문단으로 변환 */
function bodyParagraphs(text) {
  const out = [];
  const lines = String(text).replace(/\r\n?/g, "\n").split("\n");
  let titleDone = false;

  for (const raw of lines) {
    const line = raw.replace(/\s+$/, "");
    const t = line.trim();

    if (!t) { continue; }

    // <#6 주제명>
    if (!titleDone && /^<.*>$/.test(t)) {
      out.push(new Paragraph({
        spacing: { after: 260 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: "000000", space: 6 } },
        children: [new TextRun({ text: t, bold: true, font: FONT, size: SZ.title })],
      }));
      titleDone = true;
      continue;
    }

    if (t.startsWith("□")) {
      out.push(new Paragraph({
        spacing: { before: 240, after: 80 },
        children: [new TextRun({ text: t, bold: true, font: FONT, size: SZ.head })],
      }));
    } else if (t.startsWith("○")) {
      out.push(new Paragraph({
        spacing: { after: 40 }, indent: { left: 400, hanging: 200 },
        children: [new TextRun({ text: t, font: FONT, size: SZ.body })],
      }));
    } else if (/^[-–·]/.test(t)) {
      out.push(new Paragraph({
        spacing: { after: 40 }, indent: { left: 800, hanging: 200 },
        children: [new TextRun({ text: t, font: FONT, size: SZ.body })],
      }));
    } else {
      // 마커 없는 줄 = 앞 항목의 이어지는 문장
      out.push(new Paragraph({
        spacing: { after: 40 }, indent: { left: 800 },
        children: [new TextRun({ text: t, font: FONT, size: SZ.body })],
      }));
    }
  }
  if (!out.length) throw new Error("본문이 비어 있습니다. final_report_text 를 확인하십시오.");
  return out;
}

// ---------- 부록 ----------
function cell(text, opts = {}) {
  return new TableCell({
    width: { size: opts.w, type: WidthType.DXA },
    shading: opts.head ? { type: ShadingType.CLEAR, fill: "EFEFEF" } : undefined,
    margins: { top: 60, bottom: 60, left: 110, right: 110 },
    children: [new Paragraph({ children: [new TextRun({ text: String(text ?? ""), font: FONT, size: SZ.small, bold: !!opts.head })] })],
  });
}

function traceAppendix(r) {
  const tr = r.traceability || {};
  const n = (x) => (Array.isArray(x) ? x.length : 0);
  const list = (x) => (Array.isArray(x) && x.length ? x.join(", ") : "-");
  const W = [2400, 6600];

  const rows = [
    ["항목", "값"],
    ["이슈", [r.issue_id, r.issue_title].filter(Boolean).join(" ") || "-"],
    ["최종 준비도", r.final_readiness || "-"],
    ["사용 근거 수", n(tr.evidence_ids_used)],
    ["사용 사업기회 수", n(tr.bo_ids_used)],
    ["사용 전략 수", n(tr.strategy_ids_used)],
    ["원문 주제 — 반영", list(tr.must_preserve_themes_covered)],
    ["원문 주제 — 미확보", list(tr.must_preserve_themes_unsupported)],
  ];

  return [
    new Paragraph({ children: [], pageBreakBefore: true }),
    new Paragraph({
      spacing: { after: 140 },
      children: [new TextRun({ text: "[부록] 추적정보", bold: true, font: FONT, size: SZ.head })],
    }),
    new Paragraph({
      spacing: { after: 160 },
      children: [new TextRun({ text: "내부 검수용이며 제출본에는 포함하지 않는다.", font: FONT, size: SZ.small, color: "666666" })],
    }),
    new Table({
      columnWidths: W,
      width: { size: W[0] + W[1], type: WidthType.DXA },
      rows: rows.map((cells, i) =>
        new TableRow({ children: cells.map((c, j) => cell(c, { w: W[j], head: i === 0 })) })),
    }),
  ];
}

// ---------- 실행 ----------
function main() {
  const args = parseArgs(process.argv);
  if (!args.input) {
    console.error("사용법: node render_mri_docx.js <input.json> [-o output.docx] [--trace]");
    process.exit(1);
  }
  const r = loadReport(args.input);
  const text = r.final_report_text && String(r.final_report_text).trim()
    ? r.final_report_text
    : textFromStructure(r);
  if (!r.final_report_text) {
    console.warn("주의: final_report_text 가 없어 A-F 구조에서 본문을 복원했습니다. 문장 다듬기가 필요할 수 있습니다.");
  }

  const children = bodyParagraphs(text);
  if (args.trace) children.push(...traceAppendix(r));

  const doc = new Document({
    styles: { default: { document: { run: { font: FONT, size: SZ.body } } } },
    sections: [{
      properties: { page: { margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
      children,
    }],
  });

  const out = args.out || path.join(
    path.dirname(args.input),
    `MRI_${(r.issue_id || "response").replace(/[^\w.-]/g, "_")}.docx`);

  Packer.toBuffer(doc).then((buf) => {
    fs.writeFileSync(out, buf);
    console.log(`생성: ${out}  (문단 ${children.length}개${args.trace ? " · 추적정보 포함" : ""})`);
  });
}

main();
