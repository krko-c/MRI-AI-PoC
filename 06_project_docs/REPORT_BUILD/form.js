// 회사 제출 양식 「2. 구현 결과」 — KOR_BDC 사양 적용, 셀 내 다문단 지원
const fs = require('fs'), D = require('docx');
const { Document, Packer, Paragraph, TextRun, AlignmentType, Table, TableRow, TableCell,
        WidthType, ShadingType, BorderStyle } = D;

const F_BODY = '나눔바른고딕 Light', F_TITLE = 'HY견고딕';
const SZ = 26, SZ_T = 32, SCALE = 80;
const PG_W = 11906, PG_H = 16838, MARGIN = 1134;
const TBL_IND = 421, TBL_W = PG_W - MARGIN * 2 - TBL_IND;
const FILL = 'E2EFD9', LINE = 259;
const BD = { style: BorderStyle.SINGLE, size: 4, color: '000000' };

const R = (t, o = {}) => new TextRun({ text: t, font: o.font || F_BODY, size: o.size || SZ,
  scale: SCALE, bold: o.bold, color: o.color });

function runs(text, o = {}) {
  const out = []; let last = 0, m; const re = /(\*\*[^*]+\*\*)/g;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(R(text.slice(last, m.index), o));
    out.push(R(m[0].slice(2, -2), { ...o, bold: true }));
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(R(text.slice(last), o));
  return out.length ? out : [R('', o)];
}

// 줄머리에 따라 들여쓰기: ○ 0 / - 1 / · 2 / ※ 0
const IND = { '○': 0, '-': 200, '·': 400, '※': 0 };
const cellPara = (line, i, n) => {
  const head = line.trim()[0];
  return new Paragraph({
    children: runs(line.trim()),
    alignment: AlignmentType.LEFT,
    indent: { left: IND[head] ?? 0, hanging: IND[head] ? 200 : 0 },
    spacing: { before: i === 0 ? 0 : 40, after: i === n - 1 ? 0 : 0, line: LINE, lineRule: 'auto' },
  });
};

const cell = (text, w, label) => new TableCell({
  width: { size: w, type: WidthType.DXA },
  shading: label ? { type: ShadingType.CLEAR, fill: FILL, color: 'auto' } : undefined,
  margins: { top: 60, bottom: 60, left: 110, right: 110 },
  borders: { top: BD, bottom: BD, left: BD, right: BD },
  verticalAlign: label ? 'center' : 'top',
  children: text.split('\n').map((l, i, a) =>
    label ? new Paragraph({ children: runs(l, { bold: true }), alignment: AlignmentType.CENTER,
                            spacing: { before: 0, after: 0, line: LINE, lineRule: 'auto' } })
          : cellPara(l, i, a.length)),
});

const W0 = 1800, W1 = TBL_W - W0;
const rows = JSON.parse(fs.readFileSync(process.env.SRC || 'form.json', 'utf8'));

const doc = new Document({
  styles: { default: { document: { run: { font: F_BODY, size: SZ } } } },
  sections: [{
    properties: { page: { size: { width: PG_W, height: PG_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } },
    children: [
      new Paragraph({ children: [R('2. 구현 결과', { font: F_TITLE, size: SZ_T, bold: true })],
        alignment: AlignmentType.LEFT, spacing: { before: 0, after: 180, line: LINE, lineRule: 'auto' } }),
      new Table({
        columnWidths: [W0, W1], width: { size: TBL_W, type: WidthType.DXA },
        indent: { size: TBL_IND, type: WidthType.DXA },
        rows: [['구분', '내용'], ...rows].map((r, ri) => new TableRow({
          tableHeader: ri === 0,
          children: [cell(r[0], W0, true), cell(r[1], W1, ri === 0)],
        })),
      }),
    ],
  }],
});
const out = process.env.OUT || '구현 결과.docx';
Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log('생성:', out, b.length, 'bytes'); });
