#!/usr/bin/env python3
"""Mechanical quality checks for a Markdown thesis project.

Checks: word count per chapter against the budget, citation numbering and coverage,
references traced to the literature database, figure/table numbering and in-text mentions,
missing image files, 【待补充】 placeholders, AI-style phrases, and paragraph shape.

Usage:
  python thesis_qc.py <project-dir> [--budget plan/字数分配.json] [--literature a.md b.md ...] [-o qc/质检报告.md]

Exit code 1 when a blocking issue is found (missing citation target, missing image,
reference not traceable to the literature database, or figure/table mention mismatch).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

CJK = r"㐀-䶿一-鿿豈-﫿"
CJK_PUNCT = r"　-〿＀-￯‘-”…—"
RE_COUNT_CJK = re.compile(f"[{CJK}{CJK_PUNCT}]")
RE_COUNT_LATIN = re.compile(r"[A-Za-z0-9]+(?:[.'\-][A-Za-z0-9]+)*")

UNNUMBERED_H1 = re.compile(r"^(摘要|abstract|目录|参考文献|致谢|附录.*|结论|总结与展望)$", re.I)
RE_H = re.compile(r"^(#{1,4})\s+(.+?)\s*#*\s*$")
RE_IMG = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)")
RE_TAB_CAP = re.compile(r"^表\s*[:：]\s*(.+)$")
RE_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
RE_CITE = re.compile(r"\[(\d+(?:\s*[,，\-–~]\s*\d+)*)\]")
RE_PLACEHOLDER = re.compile(r"【待补充[^】]*】")
RE_MENTION = re.compile(r"([图表])\s*(\d+)\s*[-–—.．]\s*(\d+)")

AI_PHRASES = [
    "值得注意的是", "需要指出的是", "需要注意的是", "重要的是", "必须强调的是", "不难发现", "不难看出",
    "首先", "其次", "此外", "另外", "接下来", "总之", "总而言之", "综上所述",
    "随着.{0,12}的(快速|飞速|迅速|蓬勃)发展", "在当今.{0,8}(时代|社会|背景下)", "日益(增长|普及|突出)",
    "赋能", "助力", "至关重要", "显著(提升|提高|增强)", "全方位", "多维度", "深入探讨", "有效(提升|提高|解决)",
    "具有(十分|非常|极其)?重要的(意义|价值)", "起到了?(重要|关键)作用", "奠定了?(坚实|良好)的?基础",
]


CN_DIGITS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def heading_chapter_number(title: str) -> int | None:
    """Chapter number written in the heading: 第4章 / 第四章 / 4 系统设计 / 4. 系统设计. None if absent."""
    m = re.match(r"^第([0-9]+|[一二三四五六七八九十]+)章", title)
    if m:
        s = m.group(1)
        if s.isdigit():
            return int(s)
        if len(s) == 1:
            return CN_DIGITS[s]
        if s.startswith("十"):
            return 10 + CN_DIGITS.get(s[1:], 0)
        return CN_DIGITS[s[0]] * 10 + CN_DIGITS.get(s[2:], 0) if s[1] == "十" else None
    m = re.match(r"^([0-9]{1,2})(?:[.、．]|(?=[^\d.]))", title)
    return int(m.group(1)) if m else None


@dataclass
class Chapter:
    file: Path
    title: str = ""
    number: int | None = None
    words: int = 0
    is_refs: bool = False
    paragraphs: list[tuple[int, str]] = field(default_factory=list)   # (line no, text)
    list_items: int = 0


def count_words(text: str) -> int:
    """Approximates Word's 字数: each CJK character/full-width punctuation counts 1, each Latin word counts 1."""
    text = re.sub(r"`[^`]*`", " x ", text)
    text = re.sub(r"\$[^$]+\$", " x ", text)
    return len(RE_COUNT_CJK.findall(text)) + len(RE_COUNT_LATIN.findall(text))


def expand_cite(body: str) -> list[int]:
    nums: list[int] = []
    for part in re.split(r"[,，]", body):
        part = part.strip()
        rng = re.split(r"\s*[-–~]\s*", part)
        if len(rng) == 2 and rng[0].isdigit() and rng[1].isdigit():
            a, b = int(rng[0]), int(rng[1])
            nums.extend(range(min(a, b), max(a, b) + 1))
        elif part.isdigit():
            nums.append(int(part))
    return nums

def norm_title(s: str) -> str:
    return re.sub(rf"[^0-9a-z{CJK}]", "", s.lower())


def load_literature_titles(files: list[Path]) -> list[str]:
    titles = []
    for f in files:
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = re.match(r"^\s*(?:题名|标题|Title)\s*[:：]\s*(.+)$", line, re.I)
            if m:
                t = norm_title(m.group(1))
                if len(t) >= 6:
                    titles.append(t)
    return titles


class Report:
    def __init__(self) -> None:
        self.blocking: list[str] = []
        self.warnings: list[str] = []
        self.sections: list[str] = []

    def block(self, msg: str) -> None:
        self.blocking.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def chapter_files(project: Path) -> list[Path]:
    d = project / "chapters"
    if not d.is_dir():
        d = project
    return sorted(p for p in d.glob("*.md"))


def scan(files: list[Path], rep: Report):
    chapters: list[Chapter] = []
    figures: list[dict] = []
    tables: list[dict] = []
    cites: list[tuple[int, Path, int]] = []
    refs: dict[int, str] = {}
    placeholders: list[tuple[Path, int, str]] = []
    mentions: list[tuple[str, int, int, Path, int]] = []
    chap_no = 0
    fig_no = tab_no = 0
    cur: Chapter | None = None

    for f in files:
        text = re.sub(r"<!--[\s\S]*?-->", lambda m: "\n" * m.group(0).count("\n"), f.read_text(encoding="utf-8"))
        lines = text.splitlines()
        in_code = in_math = False
        para: list[str] = []
        para_start = 0
        pending_tab: str | None = None

        def flush():
            nonlocal para
            if para and cur is not None and not cur.is_refs:
                cur.paragraphs.append((para_start, "".join(para)))
            para = []

        for i, raw in enumerate(lines, 1):
            line = raw.strip()
            if line.startswith("```"):
                flush()
                in_code = not in_code
                continue
            if in_code:
                continue
            if line.startswith("$$"):
                flush()
                if not (len(line) > 4 and line.endswith("$$")):   # single-line $$…$$ opens and closes at once
                    in_math = not in_math
                continue
            if in_math:
                if line.endswith("$$"):
                    in_math = False
                continue
            m = RE_H.match(line)
            if m:
                flush()
                level, title = len(m.group(1)), m.group(2).strip()
                if level == 1:
                    clean = re.sub(r"\s+", "", title)
                    cur = Chapter(file=f, title=title)
                    if not UNNUMBERED_H1.match(clean):
                        chap_no = heading_chapter_number(clean) or chap_no + 1
                        cur.number = chap_no
                        fig_no = tab_no = 0
                    cur.is_refs = clean == "参考文献"
                    chapters.append(cur)
                elif cur is not None:
                    cur.words += count_words(title)
                continue
            if cur is None:
                cur = Chapter(file=f, title=f.stem)
                chapters.append(cur)
            if not line:
                flush()
                continue

            for ph in RE_PLACEHOLDER.findall(line):
                placeholders.append((f, i, ph))

            if cur.is_refs:
                rm = re.match(r"^(?:[-*+]\s*)?\[?(\d+)[\].)、]\s*(.+)$", line)
                if rm:
                    refs[int(rm.group(1))] = rm.group(2)
                continue

            im = RE_IMG.match(line)
            if im:
                flush()
                fig_no += 1
                label = f"图{cur.number}-{fig_no}" if cur.number else f"图{fig_no}"
                src = (f.parent / im.group(2)).resolve()
                figures.append({"label": label, "caption": im.group(1), "src": src, "file": f, "line": i,
                                "chapter": cur.number, "seq": fig_no})
                continue
            tm = RE_TAB_CAP.match(line)
            if tm:
                flush()
                pending_tab = tm.group(1)
                continue
            if pending_tab and not line.startswith("|"):
                rep.warn(f"{f.name}:{i} “表：{pending_tab}”下方没有表格")
                pending_tab = None
            if line.startswith("|"):
                flush()
                if i < len(lines) and RE_TABLE_SEP.match(lines[i]) and not RE_TABLE_SEP.match(line):
                    tab_no += 1
                    label = f"表{cur.number}-{tab_no}" if cur.number else f"表{tab_no}"
                    tables.append({"label": label, "caption": pending_tab, "file": f, "line": i,
                                   "chapter": cur.number, "seq": tab_no})
                    if not pending_tab:
                        rep.warn(f"{f.name}:{i} 表格缺少标题行（在表格上方写“表：标题”）")
                    pending_tab = None
                cur.words += count_words(re.sub(r"[|:\-]", " ", line))
                continue
            if line.startswith("$$"):
                flush()
                continue

            cur.words += count_words(line)
            for cm in RE_CITE.finditer(line):
                for n in expand_cite(cm.group(1)):
                    cites.append((n, f, i))
            for mm in RE_MENTION.finditer(line):
                mentions.append((mm.group(1), int(mm.group(2)), int(mm.group(3)), f, i))
            if re.match(r"^\s*(?:[-*+]|\d+[.)、])\s+", raw):
                flush()
                cur.list_items += 1
                continue
            if not para:
                para_start = i
            para.append(line)
        flush()
    return chapters, figures, tables, cites, refs, placeholders, mentions

def check_words(chapters: list[Chapter], budget: dict | None, rep: Report) -> None:
    body = [c for c in chapters if not c.is_refs]
    total = sum(c.words for c in body)
    rows = ["| 章节 | 实际字数 | 目标字数 | 偏差 |", "|---|---:|---:|---:|"]
    targets = {}
    if budget:
        for item in budget.get("chapters", []):
            targets[norm_title(item["title"])] = int(item["target"])
    for c in body:
        t = targets.get(norm_title(c.title))
        if t:
            dev = (c.words - t) / t
            rows.append(f"| {c.title} | {c.words} | {t} | {dev:+.0%} |")
            if abs(dev) > 0.15:
                rep.warn(f"字数偏差：{c.title} 实际 {c.words}，目标 {t}（{dev:+.0%}，超过 ±15%）")
        else:
            rows.append(f"| {c.title} | {c.words} | - | - |")
    goal = budget.get("total") if budget else None
    rows.append(f"| **合计** | **{total}** | {goal or '-'} | {f'{(total - goal) / goal:+.0%}' if goal else '-'} |")
    if goal and total < goal * 0.95:
        rep.warn(f"总字数 {total} 低于目标 {goal} 的 95%")
    rep.sections.append("## 字数统计\n\n字数口径接近 Word“字数统计”：汉字和中文标点各计 1，英文单词和数字串各计 1，不含参考文献。\n\n" + "\n".join(rows))


def check_citations(cites, refs, lit_titles, rep: Report) -> None:
    lines = ["## 引用与参考文献", ""]
    cited = sorted({n for n, _, _ in cites})
    missing = sorted({n for n in cited if n not in refs})
    uncited = sorted(n for n in refs if n not in cited)
    lines.append(f"正文引用编号 {len(cited)} 个，参考文献 {len(refs)} 条。")
    for n in missing:
        where = next(f"{f.name}:{ln}" for k, f, ln in cites if k == n)
        rep.block(f"引用 [{n}] 在参考文献中不存在（首次出现于 {where}）")
    if uncited:
        rep.warn(f"参考文献中未被正文引用的条目：{', '.join(f'[{n}]' for n in uncited)}")
    first_seen: list[int] = []
    for n, _, _ in cites:
        if n not in first_seen:
            first_seen.append(n)
    expected = sorted(first_seen)
    if first_seen and first_seen != expected:
        rep.warn("引用编号不是按首次出现顺序递增（GB/T 7714 顺序编码制要求按正文首次引用顺序编号）")
    if refs and sorted(refs) != list(range(1, max(refs) + 1)):
        rep.warn("参考文献编号不连续")
    if lit_titles:
        untraced = []
        for n, entry in sorted(refs.items()):
            key = norm_title(entry)
            if not any(t in key for t in lit_titles):
                untraced.append(n)
        for n in untraced:
            rep.block(f"参考文献 [{n}] 的题名在文献库中找不到，可能不是检索得到的真实文献：{refs[n][:60]}")
        lines.append(f"已与文献库核对：{len(refs) - len(untraced)}/{len(refs)} 条可追溯。")
    else:
        lines.append("未提供文献库（--literature），未核对参考文献来源。")
    rep.sections.append("\n".join(lines))


def check_figures_tables(figures, tables, mentions, rep: Report) -> None:
    lines = ["## 图表", "", "| 编号 | 标题 | 文件 | 状态 |", "|---|---|---|---|"]
    for fg in figures:
        status = "正常" if fg["src"].exists() else "图片缺失"
        if not fg["src"].exists():
            rep.block(f"{fg['label']} 图片文件不存在：{fg['src']}")
        if not fg["caption"]:
            rep.warn(f"{fg['label']} 没有图题（写在 ![图题](路径) 的方括号里）")
        lines.append(f"| {fg['label']} | {fg['caption'] or '（缺）'} | {fg['src'].name} | {status} |")
    for tb in tables:
        lines.append(f"| {tb['label']} | {tb['caption'] or '（缺）'} | - | 正常 |")
    known = {("图", fg["chapter"], fg["seq"]) for fg in figures} | {("表", tb["chapter"], tb["seq"]) for tb in tables}
    mentioned = {(k, c, s) for k, c, s, _, _ in mentions}
    for k, c, s, f, ln in mentions:
        if (k, c, s) not in known:
            rep.block(f"正文提到 {k}{c}-{s}，但该图表不存在（{f.name}:{ln}）")
    for k, c, s in sorted(known, key=lambda x: (x[0], x[1] or 0, x[2])):
        if c and (k, c, s) not in mentioned:
            rep.warn(f"{k}{c}-{s} 在正文中没有被提到（应在图表出现前用“如{k}{c}-{s}所示”引出）")
    lines.append("")
    lines.append(f"共 {len(figures)} 幅图、{len(tables)} 张表。")
    rep.sections.append("\n".join(lines))


def check_style(chapters: list[Chapter], placeholders, rep: Report) -> None:
    lines = ["## 待补充占位", ""]
    if placeholders:
        lines += [f"- {f.name}:{ln} {ph}" for f, ln, ph in placeholders]
        rep.warn(f"还有 {len(placeholders)} 处【待补充】需要用户填写")
    else:
        lines.append("无。")
    rep.sections.append("\n".join(lines))

    hits: dict[str, list[str]] = {}
    short_paras: list[str] = []
    for c in chapters:
        if c.is_refs:
            continue
        for ln, p in c.paragraphs:
            for pat in AI_PHRASES:
                for m in re.finditer(pat, p):
                    hits.setdefault(m.group(0) if "." in pat else pat, []).append(f"{c.file.name}:{ln}")
            sentences = [s for s in re.split(r"[。！？!?]", p) if s.strip()]
            lead_in = re.search(r"(如[图表下]|所示|[:：]\s*$|^式中)", p)   # figure/table/formula/code lead-ins are short by design
            if (len(sentences) <= 1 and count_words(p) < 60 and not lead_in
                    and not c.title.startswith(("摘要", "Abstract", "致谢"))):
                short_paras.append(f"{c.file.name}:{ln}")
        if c.list_items >= 8:
            rep.warn(f"{c.title} 有 {c.list_items} 个列表项，论文正文宜改写为连贯段落")
    lines = ["## 文风检查", "", "以下词句容易让文本显得模板化，出现次数多时建议改写（不是禁用，按语境判断）：", ""]
    if hits:
        for k, locs in sorted(hits.items(), key=lambda kv: -len(kv[1])):
            lines.append(f"- “{k}” × {len(locs)}：{', '.join(locs[:6])}{' …' if len(locs) > 6 else ''}")
    else:
        lines.append("- 未发现。")
    if short_paras:
        lines += ["", f"单句短段落 {len(short_paras)} 个（宜合并或展开）：{', '.join(short_paras[:10])}{' …' if len(short_paras) > 10 else ''}"]
    rep.sections.append("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description="Mechanical QC for a Markdown thesis project.")
    parser.add_argument("project", help="Thesis project folder (reads chapters/*.md)")
    parser.add_argument("--budget", help="Word budget JSON (default: <project>/plan/字数分配.json if present)")
    parser.add_argument("--literature", nargs="*", default=None, help="Literature database .md files with 题名： fields")
    parser.add_argument("-o", "--output", help="Report path (default: <project>/qc/质检报告.md)")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    files = chapter_files(project)
    if not files:
        print(f"error=no chapter markdown found under {project}")
        return 1
    budget_path = Path(args.budget) if args.budget else project / "plan" / "字数分配.json"
    budget = json.loads(budget_path.read_text(encoding="utf-8")) if budget_path.exists() else None
    lit_files = [Path(p) for p in args.literature] if args.literature else sorted((project / "literature").glob("*.md"))
    lit_titles = load_literature_titles(lit_files)

    rep = Report()
    chapters, figures, tables, cites, refs, placeholders, mentions = scan(files, rep)
    check_words(chapters, budget, rep)
    check_citations(cites, refs, lit_titles, rep)
    check_figures_tables(figures, tables, mentions, rep)
    check_style(chapters, placeholders, rep)

    head = ["# 论文质检报告（脚本部分）", "",
            f"检查文件：{len(files)} 个；阻断问题：{len(rep.blocking)} 个；提醒：{len(rep.warnings)} 个。", ""]
    head += ["## 阻断问题（必须先处理）", ""] + ([f"- {m}" for m in rep.blocking] or ["- 无"]) + [""]
    head += ["## 提醒", ""] + ([f"- {m}" for m in rep.warnings] or ["- 无"]) + [""]
    out = Path(args.output) if args.output else project / "qc" / "质检报告.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(head) + "\n" + "\n\n".join(rep.sections) + "\n", encoding="utf-8")

    total = sum(c.words for c in chapters if not c.is_refs)
    print(f"report={out}")
    print(f"total_words={total} chapters={len([c for c in chapters if c.number])} figures={len(figures)} tables={len(tables)} refs={len(refs)}")
    print(f"blocking={len(rep.blocking)} warnings={len(rep.warnings)} placeholders={len(placeholders)}")
    for m in rep.blocking:
        print(f"  BLOCK {m}")
    return 1 if rep.blocking else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
