/**
 * md2docx_thesis.js — Build a Chinese undergraduate thesis .docx from Markdown chapter files.
 *
 * Usage:
 *   node scripts/md2docx_thesis.js <chapters-dir | a.md b.md ...> -o 论文.docx [--format format.json] [--no-toc]
 *
 * A directory is read as all *.md files sorted by file name (00-摘要.md, 01-绪论.md, ... 90-参考文献.md, 91-致谢.md).
 * Markdown conventions: ../../thesis-body-cn/references/markdown-conventions.md
 *
 * Formatting defaults (override with --format JSON, see FORMAT_DEFAULTS):
 *   - A4, 2.5 cm margins, 宋体小四 body, 黑体 headings, Times New Roman for Latin text
 *   - 1.5 line spacing, 2-character first-line indent
 *   - Figures numbered 图章-序 below the image, tables 表章-序 above a three-line table, formulas (章-序)
 *   - [n] citations rendered as superscript, 【待补充：…】 placeholders highlighted
 *   - TOC field inserted before the first chapter (Word updates it on open)
 *
 * Dependencies: run `npm install` once in docx-editor-cn/ (docx, temml, fast-xml-parser).
 */

'use strict';

const fs   = require('fs');
const path = require('path');

const {
  Document, Packer, Paragraph, TextRun, Math: DocxMath, MathRun,
  Table, TableRow, TableCell, Header, Footer, PageNumber,
  AlignmentType, LineRuleType, HeadingLevel, BorderStyle, WidthType,
  VerticalAlign, TableOfContents, ImageRun, ShadingType,
} = require('docx');

// Yellow background for 【待补充】 (run shading; w:highlight emits w:highlightCs, which fails schema validation)
const PLACEHOLDER_SHADING = { type: ShadingType.CLEAR, color: 'auto', fill: 'FFFF00' };

const temml = require('temml');
const { mathmlToDocxChildren } = require('./mathml-to-docx');

// ─────────────────────────────────────────────────────────────────────────────
// Format settings (sizes in pt, margins in cm)
// ─────────────────────────────────────────────────────────────────────────────

const FORMAT_DEFAULTS = {
  marginsCm:   { top: 2.5, bottom: 2.5, left: 2.5, right: 2.5 },
  bodyFont:    'SimSun',            // 宋体
  headingFont: 'SimHei',            // 黑体
  latinFont:   'Times New Roman',
  bodySize: 12, h1Size: 16, h2Size: 14, h3Size: 12,   // 小四 / 三号 / 四号 / 小四
  captionSize: 10.5, tableSize: 10.5, refSize: 10.5, codeSize: 9,
  lineSpacing: 1.5,                 // multiple (1.5) or fixed value such as "20pt"
  header: '',                       // 页眉文字, e.g. "XX大学本科毕业论文"
  toc: true,
};

const UNNUMBERED_H1 = /^(摘\s*要|abstract|目\s*录|参考文献|致\s*谢|附\s*录.*|结\s*论|总结与展望)$/i;
const FRONT_MATTER_H1 = /^(摘\s*要|abstract)$/i;

const PT   = v => Math.round(v * 2);              // half-points
const CM   = v => Math.round(v * 567);            // DXA
const CMPX = v => Math.round(v * 37.795);         // pixels at 96 dpi

function parseArgs(argv) {
  const args = { inputs: [], output: 'thesis.docx', format: null, toc: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-o' || a === '--output') args.output = argv[++i];
    else if (a === '--format') args.format = argv[++i];
    else if (a === '--no-toc') args.toc = false;
    else if (a === '-h' || a === '--help') { args.help = true; }
    else args.inputs.push(a);
  }
  return args;
}

function loadFormat(file) {
  const fmt = JSON.parse(JSON.stringify(FORMAT_DEFAULTS));
  if (!file) return fmt;
  const user = JSON.parse(fs.readFileSync(file, 'utf8'));
  for (const [k, v] of Object.entries(user)) {
    if (v && typeof v === 'object' && !Array.isArray(v)) fmt[k] = { ...fmt[k], ...v };
    else fmt[k] = v;
  }
  return fmt;
}

function collectInputs(inputs) {
  const files = [];
  for (const p of inputs) {
    const st = fs.statSync(p);
    if (st.isDirectory()) {
      fs.readdirSync(p).filter(f => f.toLowerCase().endsWith('.md')).sort()
        .forEach(f => files.push(path.join(p, f)));
    } else files.push(p);
  }
  return files;
}

// ─────────────────────────────────────────────────────────────────────────────
// Markdown → block list
// ─────────────────────────────────────────────────────────────────────────────

const RE_HEADING = /^(#{1,4})\s+(.+?)\s*#*\s*$/;
const RE_IMAGE   = /^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)\s*(?:\{([^}]*)\})?\s*$/;
const RE_TABLE_CAPTION = /^表\s*[:：]\s*(.+)$/;
const RE_TABLE_ROW = /^\s*\|.*\|\s*$/;
const RE_TABLE_SEP = /^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$/;
const RE_LIST    = /^\s*(?:([-*+])|(\d+)[.)、])\s+(.+)$/;

function splitRow(line) {
  return line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim());
}

function parseMarkdown(text, baseDir) {
  const lines = text.replace(/\r\n?/g, '\n').replace(/<!--[\s\S]*?-->/g, '').split('\n');
  const blocks = [];
  let para = [];
  let pendingTableCaption = null;

  const flush = () => {
    if (para.length) blocks.push({ type: 'para', text: para.join('') });
    para = [];
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    let m;

    if (!trimmed) { flush(); continue; }

    // A 表：caption not followed by a table is kept as ordinary text
    if (pendingTableCaption && !RE_TABLE_CAPTION.test(trimmed)
        && !(RE_TABLE_ROW.test(line) && i + 1 < lines.length && RE_TABLE_SEP.test(lines[i + 1]))) {
      blocks.push({ type: 'para', text: `表：${pendingTableCaption}` });
      pendingTableCaption = null;
    }

    if (trimmed.startsWith('```')) {
      flush();
      const code = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith('```')) code.push(lines[i++]);
      blocks.push({ type: 'code', lines: code });
      continue;
    }

    if (trimmed.startsWith('$$')) {
      flush();
      let body = trimmed.slice(2);
      if (body.trim().endsWith('$$') && body.trim().length > 2) {
        body = body.trim().slice(0, -2);
      } else {
        const acc = [body];
        i++;
        while (i < lines.length && !lines[i].includes('$$')) acc.push(lines[i++]);
        if (i < lines.length) acc.push(lines[i].split('$$')[0]);
        body = acc.join(' ');
      }
      blocks.push({ type: 'formula', latex: body.trim() });
      continue;
    }

    if ((m = trimmed.match(RE_HEADING))) {
      flush();
      blocks.push({ type: 'heading', level: m[1].length, text: m[2].trim() });
      continue;
    }

    if ((m = trimmed.match(RE_IMAGE))) {
      flush();
      const attrs = {};
      (m[3] || '').split(/\s+/).filter(Boolean).forEach(kv => {
        const [k, v] = kv.split('=');
        if (k && v) attrs[k.trim()] = v.trim();
      });
      blocks.push({ type: 'image', caption: m[1].trim(), src: path.resolve(baseDir, m[2]), attrs });
      continue;
    }

    if ((m = trimmed.match(RE_TABLE_CAPTION))) {
      flush();
      pendingTableCaption = m[1].trim();
      continue;
    }

    if (RE_TABLE_ROW.test(line) && i + 1 < lines.length && RE_TABLE_SEP.test(lines[i + 1])) {
      flush();
      const headers = splitRow(line);
      const rows = [];
      i += 2;
      while (i < lines.length && RE_TABLE_ROW.test(lines[i])) rows.push(splitRow(lines[i++]));
      i--;
      blocks.push({ type: 'table', caption: pendingTableCaption, headers, rows });
      pendingTableCaption = null;
      continue;
    }

    if ((m = line.match(RE_LIST))) {
      flush();
      blocks.push({ type: 'list', ordered: !!m[2], index: m[2], text: m[3].trim() });
      continue;
    }

    if (trimmed.startsWith('>')) {
      flush();
      blocks.push({ type: 'para', text: trimmed.replace(/^>\s?/, '') });
      continue;
    }

    // Chinese paragraphs: join soft-wrapped lines without spaces; keep a space between Latin words
    if (para.length && /[A-Za-z0-9,.;:]$/.test(para[para.length - 1]) && /^[A-Za-z0-9]/.test(trimmed)) para.push(' ');
    para.push(trimmed);
  }
  flush();
  if (pendingTableCaption) blocks.push({ type: 'para', text: `表：${pendingTableCaption}` });
  return blocks;
}

// ─────────────────────────────────────────────────────────────────────────────
// Inline content: **bold**, `code`, $math$, [n] citations, 【待补充：…】 placeholders
// ─────────────────────────────────────────────────────────────────────────────

const RE_INLINE = /\*\*([^*]+)\*\*|`([^`]+)`|\$([^$]+)\$|(\[\d+(?:\s*[,，\-–~]\s*\d+)*\])|(【待补充[^】]*】)/g;

function mathRuns(latex, display) {
  try {
    const ml = temml.renderToString(latex, { displayMode: display, throwOnError: false });
    const kids = mathmlToDocxChildren(ml);
    if (kids && kids.length) return new DocxMath({ children: kids });
  } catch (_) { /* fall through to plain text */ }
  return new DocxMath({ children: [new MathRun(latex)] });
}

function inlineRuns(text, opts = {}) {
  const base = opts.run || {};
  const runs = [];
  let last = 0;
  let m;
  RE_INLINE.lastIndex = 0;
  while ((m = RE_INLINE.exec(text)) !== null) {
    if (m.index > last) runs.push(new TextRun({ ...base, text: text.slice(last, m.index) }));
    if (m[1] !== undefined) runs.push(new TextRun({ ...base, text: m[1], bold: true }));
    else if (m[2] !== undefined) runs.push(new TextRun({ ...base, text: m[2], font: CTX.fmt.latinFont }));
    else if (m[3] !== undefined) runs.push(mathRuns(m[3], false));
    else if (m[4] !== undefined) {
      runs.push(new TextRun({ ...base, text: m[4], superScript: !opts.noSuperscript }));
    } else if (m[5] !== undefined) {
      runs.push(new TextRun({ ...base, text: m[5], shading: PLACEHOLDER_SHADING }));
      CTX.stats.placeholders.push(m[5]);
    }
    last = m.index + m[0].length;
  }
  if (last < text.length) runs.push(new TextRun({ ...base, text: text.slice(last) }));
  return runs;
}

// ─────────────────────────────────────────────────────────────────────────────
// Image size probing (PNG / JPEG / GIF / BMP) — keeps the aspect ratio
// ─────────────────────────────────────────────────────────────────────────────

function imageInfo(buf, file) {
  const ext = path.extname(file).toLowerCase();
  if (buf.length > 24 && buf.readUInt32BE(0) === 0x89504e47) {
    return { type: 'png', w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
  }
  if (buf[0] === 0xff && buf[1] === 0xd8) {
    let off = 2;
    while (off < buf.length) {
      if (buf[off] !== 0xff) { off++; continue; }
      const marker = buf[off + 1];
      const len = buf.readUInt16BE(off + 2);
      if (marker >= 0xc0 && marker <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(marker)) {
        return { type: 'jpg', h: buf.readUInt16BE(off + 5), w: buf.readUInt16BE(off + 7) };
      }
      off += 2 + len;
    }
  }
  if (buf.toString('ascii', 0, 3) === 'GIF') return { type: 'gif', w: buf.readUInt16LE(6), h: buf.readUInt16LE(8) };
  if (buf.toString('ascii', 0, 2) === 'BM') return { type: 'bmp', w: buf.readInt32LE(18), h: Math.abs(buf.readInt32LE(22)) };
  throw new Error(`Unsupported image format (use PNG or JPG): ${file}${ext === '.svg' ? ' — convert SVG to PNG first' : ''}`);
}

// ─────────────────────────────────────────────────────────────────────────────
// Block rendering
// ─────────────────────────────────────────────────────────────────────────────

const CTX = {
  fmt: null, chapter: 0, fig: 0, tab: 0, eq: 0, inReferences: false, tocInserted: false,
  stats: { chapters: 0, figures: 0, tables: 0, formulas: 0, placeholders: [], missingImages: [] },
};

const THICK = { style: BorderStyle.SINGLE, size: 12, color: '000000' };
const THIN  = { style: BorderStyle.SINGLE, size: 6,  color: '000000' };
const NONE  = { style: BorderStyle.NONE,   size: 0,  color: 'FFFFFF' };

function contentWidth() {
  return 11906 - CM(CTX.fmt.marginsCm.left) - CM(CTX.fmt.marginsCm.right);
}

function chapterLabel() { return CTX.chapter > 0 ? `${CTX.chapter}-` : ''; }

function caption(kind, text) {
  const n = kind === '图' ? ++CTX.fig : ++CTX.tab;
  const label = `${kind}${chapterLabel()}${n}`;
  return {
    label,
    para: new Paragraph({
      style: 'Caption',
      keepNext: kind === '表',
      children: [new TextRun(`${label}  ${text}`)],
    }),
  };
}

// Chapter number written in the heading (第4章 / 第四章 / "4 系统设计"); null → count sequentially.
// Keeps 图4-1 correct while only some chapters are drafted. Mirrors heading_chapter_number() in thesis_qc.py.
const CN_DIGITS = { 一: 1, 二: 2, 三: 3, 四: 4, 五: 5, 六: 6, 七: 7, 八: 8, 九: 9, 十: 10 };
function headingChapterNumber(t) {
  let m = t.match(/^第([0-9]+|[一二三四五六七八九十]+)章/);
  if (m) {
    const s = m[1];
    if (/^\d+$/.test(s)) return parseInt(s, 10);
    if (s.length === 1) return CN_DIGITS[s];
    if (s[0] === '十') return 10 + (CN_DIGITS[s.slice(1)] || 0);
    if (s[1] === '十') return CN_DIGITS[s[0]] * 10 + (CN_DIGITS[s.slice(2)] || 0);
    return null;
  }
  m = t.match(/^([0-9]{1,2})(?:[.、．]|(?=[^\d.]))/);
  return m ? parseInt(m[1], 10) : null;
}

function headingBlock(b, out) {
  const text = b.text;
  if (b.level === 1) {
    const unnumbered = UNNUMBERED_H1.test(text.replace(/\s+/g, ''));
    if (!unnumbered && !FRONT_MATTER_H1.test(text) && CTX.fmt.toc && !CTX.tocInserted) {
      out.push(new Paragraph({ style: 'TocTitle', pageBreakBefore: true, children: [new TextRun('目　录')] }));
      out.push(new TableOfContents('目录', { hyperlink: true, headingStyleRange: '1-3' }));
      CTX.tocInserted = true;
    }
    if (!unnumbered) {
      CTX.chapter = headingChapterNumber(text.replace(/\s+/g, '')) || CTX.chapter + 1;
      CTX.stats.chapters++; CTX.fig = 0; CTX.tab = 0; CTX.eq = 0;
    }
    CTX.inReferences = /^参考文献$/.test(text.replace(/\s+/g, ''));
    out.push(new Paragraph({
      heading: HeadingLevel.HEADING_1,
      pageBreakBefore: out.length > 0,
      children: [new TextRun(text)],
    }));
    return;
  }
  const level = { 2: HeadingLevel.HEADING_2, 3: HeadingLevel.HEADING_3, 4: HeadingLevel.HEADING_4 }[b.level];
  out.push(new Paragraph({ heading: level, children: [new TextRun(text)] }));
}

function paraBlock(b, out) {
  if (CTX.inReferences) {
    out.push(new Paragraph({ style: 'Reference', children: inlineRuns(b.text, { noSuperscript: true }) }));
    return;
  }
  if (/^(关键词|关键字|Key\s*words)\s*[:：]/i.test(b.text)) {
    const [, label, rest] = b.text.match(/^([^:：]+[:：])\s*(.*)$/);
    out.push(new Paragraph({
      style: 'Normal', indent: { firstLine: 0 },
      children: [new TextRun({ text: label.endsWith(':') ? label + ' ' : label, bold: true }), ...inlineRuns(rest)],
    }));
    return;
  }
  out.push(new Paragraph({ style: 'Normal', children: inlineRuns(b.text) }));
}

function listBlock(b, out) {
  if (CTX.inReferences) {
    const label = b.ordered ? `[${b.index}] ` : '';
    out.push(new Paragraph({ style: 'Reference', children: inlineRuns(label + b.text, { noSuperscript: true }) }));
    return;
  }
  const prefix = b.ordered ? `（${b.index}）` : '';
  out.push(new Paragraph({ style: 'Normal', children: inlineRuns(prefix + b.text) }));
}

function imageBlock(b, out) {
  CTX.stats.figures++;
  const cap = caption('图', b.caption || '未命名图');
  if (!fs.existsSync(b.src)) {
    const note = `【待补充：${cap.label} ${b.caption}，图片文件缺失 ${path.basename(b.src)}】`;
    CTX.stats.missingImages.push(`${cap.label} ${b.src}`);
    CTX.stats.placeholders.push(note);
    // Bordered single-cell table as the placeholder box (paragraph borders serialize in a schema-invalid order)
    const boxW = Math.round(contentWidth() * 0.6);
    out.push(new Table({
      width: { size: boxW, type: WidthType.DXA }, columnWidths: [boxW], alignment: AlignmentType.CENTER,
      rows: [new TableRow({ children: [new TableCell({
        width: { size: boxW, type: WidthType.DXA },
        borders: { top: THIN, bottom: THIN, left: THIN, right: THIN },
        shading: PLACEHOLDER_SHADING, verticalAlign: VerticalAlign.CENTER,
        margins: { top: 600, bottom: 600, left: 120, right: 120 },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, indent: { firstLine: 0 }, keepNext: true,
          children: [new TextRun({ text: note })] })],
      })] })],
    }));
    out.push(cap.para);
    return;
  }
  const buf = fs.readFileSync(b.src);
  const info = imageInfo(buf, b.src);
  const maxW = CMPX(contentWidth() / 567);
  let w = b.attrs.width ? CMPX(parseFloat(b.attrs.width)) : Math.min(info.w, Math.round(maxW * 0.85));
  w = Math.min(w, maxW);
  const h = Math.round(w * info.h / info.w);
  out.push(new Paragraph({
    alignment: AlignmentType.CENTER, indent: { firstLine: 0 }, keepNext: true,
    spacing: { line: 240, lineRule: LineRuleType.AUTO, before: 120 },
    children: [new ImageRun({
      type: info.type, data: buf, transformation: { width: w, height: h },
      altText: { title: b.caption, description: b.caption, name: path.basename(b.src) },
    })],
  }));
  out.push(cap.para);
}

function tableBlock(b, out) {
  CTX.stats.tables++;
  const cap = caption('表', b.caption || '未命名表');
  out.push(cap.para);
  const n = b.headers.length;
  const total = contentWidth();
  // Column widths proportional to the longest cell text, with a floor per column
  const lens = b.headers.map((h, i) => Math.max(h.length, ...b.rows.map(r => (r[i] || '').length), 2));
  const sum = lens.reduce((a, c) => a + c, 0);
  const widths = lens.map(l => Math.max(Math.round(total * l / sum), 900));
  widths[n - 1] += total - widths.reduce((a, c) => a + c, 0);

  const cell = (text, w, borders, bold) => new TableCell({
    width: { size: w, type: WidthType.DXA },
    borders,
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({
      style: 'TableText',
      children: inlineRuns(text, { run: bold ? { bold: true } : {}, noSuperscript: false }),
    })],
  });
  const header = new TableRow({
    tableHeader: true,
    children: b.headers.map((h, i) => cell(h, widths[i], { top: THICK, bottom: THIN, left: NONE, right: NONE }, true)),
  });
  const rows = b.rows.map((r, ri) => new TableRow({
    cantSplit: true,
    children: b.headers.map((_, i) => cell(r[i] || '', widths[i], {
      top: NONE, bottom: ri === b.rows.length - 1 ? THICK : NONE, left: NONE, right: NONE,
    }, false)),
  }));
  out.push(new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    borders: { top: NONE, bottom: NONE, left: NONE, right: NONE, insideHorizontal: NONE, insideVertical: NONE },
    rows: [header, ...rows],
  }));
  out.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
}

function formulaBlock(b, out) {
  CTX.stats.formulas++;
  const num = `（${chapterLabel()}${++CTX.eq}）`;
  const total = contentWidth();
  const side = 1134;
  const noB = { top: NONE, bottom: NONE, left: NONE, right: NONE };
  const c = (w, children, align) => new TableCell({
    width: { size: w, type: WidthType.DXA }, borders: noB, verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({ alignment: align, indent: { firstLine: 0 }, children })],
  });
  out.push(new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: [side, total - 2 * side, side],
    borders: { ...noB, insideHorizontal: NONE, insideVertical: NONE },
    rows: [new TableRow({ children: [
      c(side, [], AlignmentType.LEFT),
      c(total - 2 * side, [mathRuns(b.latex, true)], AlignmentType.CENTER),
      c(side, [new TextRun(num)], AlignmentType.RIGHT),
    ] })],
  }));
}

function codeBlock(b, out) {
  b.lines.forEach((l, i) => out.push(new Paragraph({
    style: 'Code',
    keepNext: i < b.lines.length - 1,
    children: [new TextRun(l.replace(/\t/g, '    ') || ' ')],
  })));
}

function render(blocks) {
  const out = [];
  for (const b of blocks) {
    if (b.type === 'heading') headingBlock(b, out);
    else if (b.type === 'para') paraBlock(b, out);
    else if (b.type === 'list') listBlock(b, out);
    else if (b.type === 'image') imageBlock(b, out);
    else if (b.type === 'table') tableBlock(b, out);
    else if (b.type === 'formula') formulaBlock(b, out);
    else if (b.type === 'code') codeBlock(b, out);
  }
  return out;
}

// ─────────────────────────────────────────────────────────────────────────────
// Styles
// ─────────────────────────────────────────────────────────────────────────────

function lineSpacing(v) {
  if (typeof v === 'string' && /pt$/.test(v)) return { line: Math.round(parseFloat(v) * 20), lineRule: LineRuleType.EXACT };
  return { line: Math.round(Number(v) * 240), lineRule: LineRuleType.AUTO };
}

function buildStyles(f) {
  const font = east => ({ ascii: f.latinFont, hAnsi: f.latinFont, eastAsia: east, cs: f.latinFont });
  // Headings go through default.headingN so they replace docx's built-in (blue) Heading styles
  // instead of being emitted a second time with the same styleId.
  const heading = (size, align, before, after, outline) => ({
    run: { font: font(f.headingFont), size: PT(size), bold: true, color: '000000' },
    paragraph: {
      alignment: align, indent: { firstLine: 0 }, keepNext: true, keepLines: true,
      spacing: { before, after, line: 240, lineRule: LineRuleType.AUTO }, outlineLevel: outline,
    },
  });
  return {
    default: {
      document: {
        run: { font: font(f.bodyFont), size: PT(f.bodySize) },
        paragraph: { spacing: lineSpacing(f.lineSpacing), indent: { firstLine: PT(f.bodySize) * 20 }, alignment: AlignmentType.JUSTIFIED },
      },
      heading1: heading(f.h1Size, AlignmentType.CENTER, 240, 240, 0),
      heading2: heading(f.h2Size, AlignmentType.LEFT, 240, 120, 1),
      heading3: heading(f.h3Size, AlignmentType.LEFT, 120, 60, 2),
      heading4: heading(f.bodySize, AlignmentType.LEFT, 60, 60, 3),
    },
    paragraphStyles: [
      // Explicit Normal so body text shows as 正文 in Word and basedOn: 'Normal' resolves
      { id: 'Normal', name: 'Normal', quickFormat: true,
        run: { font: font(f.bodyFont), size: PT(f.bodySize) },
        paragraph: { spacing: lineSpacing(f.lineSpacing), indent: { firstLine: PT(f.bodySize) * 20 }, alignment: AlignmentType.JUSTIFIED } },
      { id: 'TocTitle', name: 'TOC Title', basedOn: 'Normal', next: 'Normal',
        run: { font: font(f.headingFont), size: PT(f.h1Size), bold: true },
        paragraph: { alignment: AlignmentType.CENTER, indent: { firstLine: 0 }, spacing: { before: 240, after: 240 } } },
      { id: 'Caption', name: 'Caption', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: font(f.bodyFont), size: PT(f.captionSize), color: '000000' },
        paragraph: { alignment: AlignmentType.CENTER, indent: { firstLine: 0 },
          spacing: { before: 60, after: 120, line: 240, lineRule: LineRuleType.AUTO } } },
      { id: 'TableText', name: 'Table Text', basedOn: 'Normal',
        run: { size: PT(f.tableSize) },
        paragraph: { alignment: AlignmentType.CENTER, indent: { firstLine: 0 },
          spacing: { line: 240, lineRule: LineRuleType.AUTO } } },
      { id: 'Reference', name: 'Reference', basedOn: 'Normal',
        run: { size: PT(f.refSize) },
        paragraph: { alignment: AlignmentType.LEFT, indent: { left: 420, hanging: 420, firstLine: 0 },
          spacing: { line: 300, lineRule: LineRuleType.AUTO } } },
      { id: 'Code', name: 'Code', basedOn: 'Normal',
        run: { font: { ascii: 'Consolas', hAnsi: 'Consolas', eastAsia: f.bodyFont }, size: PT(f.codeSize) },
        paragraph: { alignment: AlignmentType.LEFT, indent: { firstLine: 0, left: 240 },
          spacing: { line: 240, lineRule: LineRuleType.AUTO } } },
    ],
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────────────────────────────────────

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.inputs.length) {
    console.log('Usage: node md2docx_thesis.js <chapters-dir | files...> -o out.docx [--format format.json] [--no-toc]');
    process.exit(args.help ? 0 : 1);
  }
  CTX.fmt = loadFormat(args.format);
  if (args.toc === false) CTX.fmt.toc = false;

  const files = collectInputs(args.inputs);
  if (!files.length) throw new Error('No Markdown files found');
  const blocks = [];
  for (const f of files) blocks.push(...parseMarkdown(fs.readFileSync(f, 'utf8'), path.dirname(f)));
  const children = render(blocks);

  const f = CTX.fmt;
  const pageNum = new Footer({ children: [new Paragraph({
    alignment: AlignmentType.CENTER, indent: { firstLine: 0 },
    children: [new TextRun({ children: [PageNumber.CURRENT], size: PT(10.5) })],
  })] });
  const headers = f.header ? { default: new Header({ children: [new Paragraph({
    alignment: AlignmentType.CENTER, indent: { firstLine: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '000000', space: 1 } },
    children: [new TextRun({ text: f.header, size: PT(10.5) })],
  })] }) } : undefined;

  const doc = new Document({
    features: { updateFields: true },
    styles: buildStyles(f),
    sections: [{
      properties: { page: {
        size: { width: 11906, height: 16838 },
        margin: { top: CM(f.marginsCm.top), bottom: CM(f.marginsCm.bottom),
                  left: CM(f.marginsCm.left), right: CM(f.marginsCm.right) },
      } },
      headers,
      footers: { default: pageNum },
      children,
    }],
  });

  Packer.toBuffer(doc).then(buf => {
    const out = path.resolve(args.output);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, buf);
    const s = CTX.stats;
    console.log(`written=${out}`);
    console.log(`files=${files.length} chapters=${s.chapters} figures=${s.figures} tables=${s.tables} formulas=${s.formulas}`);
    console.log(`placeholders=${s.placeholders.length}`);
    s.placeholders.forEach(p => console.log(`  ${p}`));
    if (s.missingImages.length) console.log(`missing_images=${s.missingImages.join('; ')}`);
  }).catch(err => { console.error('Error building document:', err.message); process.exit(1); });
}

main();
