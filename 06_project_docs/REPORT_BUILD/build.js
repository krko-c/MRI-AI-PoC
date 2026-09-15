// KOR_BDC 양식 사양 그대로 적용
const fs = require('fs'), path = require('path'), D = require('docx');
const { Document, Packer, Paragraph, TextRun, AlignmentType, Table, TableRow, TableCell,
        WidthType, ShadingType, BorderStyle, Footer, PageNumber, UnderlineType, ImageRun } = D;

// ── 양식에서 추출한 값 ──────────────────────────────
const F_BODY = '나눔바른고딕 Light';   // 본문
const F_TITLE = 'HY견고딕';            // 제목
const SZ_BODY = 26;                    // 13pt
const SZ_TITLE = 32;                   // 16pt
const SCALE = 80;                      // 장평 80%
const PG_W = 11906, PG_H = 16838, MARGIN = 1134;
const CONTENT_W = PG_W - MARGIN * 2;   // 9638
const TBL_IND = 421;
const TBL_W = CONTENT_W - TBL_IND;     // 9217
const FILL_HEAD = 'E2EFD9';            // 라벨 셀 음영
const LINE = 259;                      // 줄간격(auto)
// 개요 수준별 들여쓰기 (양식 numbering.xml)
const LV = { h: { l: 400, h: 400 }, a: { l: 800, h: 400 }, b: { l: 1200, h: 400 }, c: { l: 1600, h: 400 } };

const R = (text, o = {}) => new TextRun({
  text, font: o.font || F_BODY, size: o.size || SZ_BODY, scale: SCALE,
  bold: o.bold, underline: o.underline, color: o.color,
});

function runs(text, o = {}) {
  const out = [], re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(R(text.slice(last, m.index), o));
    const t = m[0];
    out.push(t.startsWith('**') ? R(t.slice(2, -2), { ...o, bold: true }) : R(t.slice(1, -1), o));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(R(text.slice(last), o));
  return out.length ? out : [R('', o)];
}

const para = (text, o = {}) => new Paragraph({
  children: runs(text, o),
  alignment: o.alignment || AlignmentType.BOTH,
  indent: o.indent,
  spacing: { before: o.before ?? 0, after: o.after ?? 60, line: LINE, lineRule: 'auto' },
});

// ── 표 ─────────────────────────────────────────────
const BD = { style: BorderStyle.SINGLE, size: 4, color: '000000' };
function cell(text, w, head) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: head ? { type: ShadingType.CLEAR, fill: FILL_HEAD, color: 'auto' } : undefined,
    margins: { top: 40, bottom: 40, left: 100, right: 100 },
    borders: { top: BD, bottom: BD, left: BD, right: BD },
    children: [new Paragraph({
      children: runs(text, {}),
      alignment: head ? AlignmentType.CENTER : AlignmentType.LEFT,
      spacing: { before: 0, after: 0, line: 240, lineRule: 'auto' },
    })],
  });
}
const vlen = (s) => [...s.replace(/\*\*|`/g, '')].reduce((a, c) => a + (c.charCodeAt(0) > 0x2000 ? 2 : 1), 0);
function mkTable(rows) {
  const n = rows[0].length;
  // 열별 최대 표시길이로 폭 배분 (최소 5% · 최대 45%)
  const raw = [];
  for (let c = 0; c < n; c++) raw.push(Math.max(...rows.map(r => vlen(r[c] || ''))));
  // 길이를 완만하게 반영(제곱근) 후 비율 5~45%로 제한하고 재정규화
  let p = raw.map(v => Math.sqrt(Math.max(v, 1)));
  let s0 = p.reduce((a, b) => a + b, 0);
  p = p.map(v => Math.min(0.45, Math.max(0.05, v / s0)));
  const s1 = p.reduce((a, b) => a + b, 0);
  let w = p.map(v => Math.floor(v / s1 * TBL_W));
  w[n - 1] = TBL_W - w.slice(0, n - 1).reduce((a, b) => a + b, 0);
  return new Table({
    columnWidths: w,
    width: { size: TBL_W, type: WidthType.DXA },
    indent: { size: TBL_IND, type: WidthType.DXA },
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      children: r.map((c, ci) => cell(c, w[ci], ri === 0 || (n === 2 && ci === 0))),
    })),
  });
}

// ── 도형(표 기반 박스) ────────────────────────────
const FILL_BOX = 'E2EFD9', FILL_IO = 'F2F2F2', FILL_W = 'FFFFFF';
function dcell(t, w, o = {}) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA },
    columnSpan: o.span,
    shading: { type: ShadingType.CLEAR, fill: o.fill || FILL_W, color: 'auto' },
    margins: { top: 70, bottom: 70, left: 120, right: 120 },
    borders: { top: BD, bottom: BD, left: BD, right: BD },
    verticalAlign: 'center',
    children: [new Paragraph({
      children: runs(t, { bold: o.bold, size: o.size || SZ_BODY }),
      alignment: o.align || AlignmentType.LEFT,
      spacing: { before: 0, after: 0, line: 240, lineRule: 'auto' },
    })],
  });
}
function dtable(rows) {          // rows: [[{t,w,...}]]
  // 격자는 열이 가장 많은 행 기준. 열이 적은 행은 마지막 셀을 병합한다.
  const base = rows.reduce((a, r) => (r.length > a.length ? r : a), rows[0]);
  const ws = base.map(c => c.w);
  const n = ws.length;
  return new Table({
    columnWidths: ws, width: { size: TBL_W, type: WidthType.DXA },
    indent: { size: TBL_IND, type: WidthType.DXA },
    rows: rows.map(r => new TableRow({
      children: r.map((c, ci) => {
        const last = ci === r.length - 1;
        const span = last && r.length < n ? n - r.length + 1 : undefined;
        const w = span ? ws.slice(ci).reduce((a, b) => a + b, 0) : ws[ci];
        return dcell(c.t, w, Object.assign({}, c, { span }));
      }),
    })),
  });
}
const arrow = () => new Paragraph({
  children: [R('▼', { size: 24 })], alignment: AlignmentType.CENTER,
  spacing: { before: 40, after: 40, line: 200, lineRule: 'auto' },
});
function buildFlow(lines) {
  const out = []; let buf = [];
  const flush = () => { if (buf.length) { out.push(dtable(buf)); buf = []; } };
  for (const raw of lines) {
    const L = raw.trim();
    if (!L) continue;
    if (L === 'v') { flush(); out.push(arrow()); continue; }
    let m;
    if ((m = L.match(/^=\s+(.*)$/))) {                       // 입력·출력 박스
      flush();
      out.push(dtable([[{ t: m[1], w: TBL_W, fill: FILL_IO, bold: true, align: AlignmentType.CENTER }]]));
      continue;
    }
    if ((m = L.match(/^#\s+(.*)$/))) {                       // 국면 머리행
      const p = m[1].split('|').map(x => x.trim());
      const w1 = Math.round(TBL_W * 0.62);
      buf.push([{ t: p[0], w: w1, fill: FILL_BOX, bold: true },
                { t: p[1] || '', w: TBL_W - w1, fill: FILL_BOX, bold: true, align: AlignmentType.CENTER }]);
      continue;
    }
    if ((m = L.match(/^\.\s+(.*)$/))) {                      // 국면 내용행
      buf.push([{ t: m[1], w: TBL_W }]);
      continue;
    }
    if ((m = L.match(/^>\s+(.*)$/))) {                       // 단계 박스
      const p = m[1].split('|').map(x => x.trim());
      if (p.length >= 3) {
        const a = Math.round(TBL_W * 0.24), c = Math.round(TBL_W * 0.20);
        buf.push([{ t: p[0], w: a, fill: FILL_BOX, bold: true, align: AlignmentType.CENTER },
                  { t: p[1], w: TBL_W - a - c },
                  { t: p[2], w: c, align: AlignmentType.CENTER, size: 22 }]);
      } else {
        const a = Math.round(TBL_W * 0.28);
        buf.push([{ t: p[0], w: a, fill: FILL_BOX, bold: true, align: AlignmentType.CENTER },
                  { t: p[1] || '', w: TBL_W - a }]);
      }
      continue;
    }
  }
  flush();
  return out;
}

const codeBlock = (lines) => lines.map((l, i) => new Paragraph({
  children: [new TextRun({ text: l || ' ', font: 'Consolas', size: 15 })],
  alignment: AlignmentType.LEFT,
  indent: { left: TBL_IND },
  spacing: { before: i === 0 ? 80 : 0, after: i === lines.length - 1 ? 120 : 0, line: 220, lineRule: 'auto' },
}));

// ── 파싱 ───────────────────────────────────────────
const md = fs.readFileSync(path.join(__dirname, process.env.MD || 'agent1.md'), 'utf8').split('\n');
const body = [];
let i = 0, titleDone = false, m;

while (i < md.length) {
  const line = md[i];

  if ((m = line.match(/^!fig\s+(\S+)\s*$/))) {
    const p = path.join(__dirname, m[1]);
    const b = fs.readFileSync(p);
    const iw = b.readUInt32BE(16), ih = b.readUInt32BE(20);   // PNG 헤더
    const W_PX = Math.round(CONTENT_W / 1440 * 96);           // 본문폭(px @96dpi)
    body.push(new Paragraph({
      children: [new ImageRun({ type: 'png', data: b,
        transformation: { width: W_PX, height: Math.round(W_PX * ih / iw) } })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 120, after: 160 },
    }));
    i++; continue;
  }

  if (/^:::flow\s*$/.test(line)) {
    const buf = []; i++;
    while (i < md.length && !/^:::\s*$/.test(md[i])) { buf.push(md[i]); i++; }
    i++;
    body.push(...buildFlow(buf));
    body.push(new Paragraph({ children: [R('', { size: 10 })], spacing: { after: 140 } }));
    continue;
  }

  if (/^```/.test(line)) {
    const buf = []; i++;
    while (i < md.length && !/^```/.test(md[i])) { buf.push(md[i]); i++; }
    i++; body.push(...codeBlock(buf)); continue;
  }

  if (/^\|/.test(line) && i + 1 < md.length && /^\|[\s:|-]+\|$/.test(md[i + 1])) {
    const rows = [];
    while (i < md.length && /^\|/.test(md[i])) {
      if (!/^\|[\s:|-]+\|$/.test(md[i])) rows.push(md[i].replace(/^\||\|$/g, '').split('|').map(s => s.trim()));
      i++;
    }
    body.push(mkTable(rows));
    body.push(new Paragraph({ children: [R('', { size: 10 })], spacing: { after: 100 } }));
    continue;
  }

  if (/^---\s*$/.test(line)) { i++; continue; }

  if ((m = line.match(/^#\s+(.*)$/))) {           // 문서 제목
    titleDone = true;
    body.push(new Paragraph({
      children: [R(m[1], { font: F_TITLE, size: SZ_TITLE, bold: true, underline: { type: UnderlineType.SINGLE } })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 120, line: LINE, lineRule: 'auto' },
    }));
    i++; continue;
  }

  if ((m = line.match(/^@\s+(.*)$/))) {           // 부제·날짜 (가운데)
    body.push(new Paragraph({
      children: runs(m[1]), alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 300, line: LINE, lineRule: 'auto' },
    }));
    i++; continue;
  }

  if ((m = line.match(/^##\s+(.*)$/))) {          // 장 (Ⅰ. Ⅱ. …)
    body.push(new Paragraph({
      children: [R(m[1], { font: F_TITLE, size: 28, bold: true })],
      alignment: AlignmentType.LEFT,
      spacing: { before: 400, after: 140, line: LINE, lineRule: 'auto' },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '000000', space: 4 } },
    }));
    i++; continue;
  }

  if ((m = line.match(/^###\s+(.*)$/))) {         // 절 (1. 2. …) — 양식의 대제목 수준
    body.push(new Paragraph({
      children: runs(m[1], { bold: true }),
      alignment: AlignmentType.LEFT,
      indent: { left: LV.h.l, hanging: LV.h.h },
      spacing: { before: 240, after: 70, line: LINE, lineRule: 'auto' },
    }));
    i++; continue;
  }

  if (/^>\s?/.test(line)) {
    const buf = [];
    while (i < md.length && /^>\s?/.test(md[i])) { buf.push(md[i].replace(/^>\s?/, '')); i++; }
    buf.filter(s => s.trim()).forEach(t => body.push(para(t, { indent: { left: LV.c.l } })));
    continue;
  }

  // 개요 수준: ○ / - / ·  (양식 numbering 들여쓰기 그대로)
  if ((m = line.match(/^(\s*)([○\-·※])\s+(.*)$/))) {
    const lead = m[1].length, mk = m[2], txt = m[3];
    let lv = LV.a, mark = '○ ';
    if (mk === '-') { lv = LV.b; mark = '- '; }
    else if (mk === '·') { lv = LV.c; mark = '· '; }
    else if (mk === '※') { lv = { l: 0, h: 0 }; mark = '※ '; }
    body.push(new Paragraph({
      children: [R(mark), ...runs(txt)],
      alignment: AlignmentType.BOTH,
      indent: { left: lv.l, hanging: lv.h },
      spacing: { before: mk === '○' ? 80 : 10, after: 20, line: LINE, lineRule: 'auto' },
    }));
    i++; continue;
  }

  if (line.trim() === '') { i++; continue; }
  body.push(para(line, { indent: { left: LV.a.l } }));
  i++;
}

const doc = new Document({
  creator: 'NH-Amundi', title: 'MRI 이슈 스크리닝 AI 구축 결과',
  styles: { default: { document: { run: { font: F_BODY, size: SZ_BODY }, paragraph: { alignment: AlignmentType.BOTH } } } },
  sections: [{
    properties: { page: { size: { width: PG_W, height: PG_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN, header: 0, footer: 0 } } },
    footers: { default: new Footer({ children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], font: F_BODY, size: SZ_BODY, scale: SCALE })],
    })] }) },
    children: body,
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(__dirname, process.env.OUT || 'MRI 이슈 스크리닝 AI 구축 결과.docx');
  fs.writeFileSync(out, buf);
  console.log('생성:', path.basename(out), buf.length, 'bytes');
});
