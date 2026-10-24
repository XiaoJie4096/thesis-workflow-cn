---
name: thesis-qc-cn
description: Quality-check a drafted Chinese undergraduate thesis before submission. Use when the user asks for 论文质检, 检查论文, 字数统计, 引用检查, 图表编号检查, 查重前检查, 降AI痕迹, 模拟盲审, 仇人盲审, 导师审阅, or wants to know what is still missing. Runs a mechanical checker over chapters/*.md, then a role-based review, and loops fixes with the user.
---

# Thesis QC CN

## Core Positioning

QC has two layers. The script catches what can be checked mechanically. The agent review catches what needs judgment. Neither replaces the supervisor or the school's plagiarism/AIGC detection; say so when reporting.

## Layer 1: Mechanical Check

```bash
python modules/thesis-qc-cn/scripts/thesis_qc.py <论文项目> [--budget plan/字数分配.json] [--literature literature/题录摘要.md]
```

Defaults: reads `chapters/*.md`, `plan/字数分配.json` if present, and `literature/*.md`. Writes `qc/质检报告.md`. Exit code 1 means blocking issues exist.

It checks:

| Item | Blocking |
|---|---|
| Citation `[n]` with no matching reference entry | Yes |
| Reference that cannot be traced to a literature record title | Yes |
| Figure file missing | Yes |
| Text mentions 图N-M / 表N-M that does not exist | Yes |
| Word count per chapter vs. budget (±15%), total < 95% | No |
| Uncited references, numbering not in first-appearance order, gaps in reference numbers | No |
| Figures/tables never mentioned in text, tables without caption | No |
| `【待补充：…】` placeholders still present | No (must be zero before submission) |
| Template-like phrases, single-sentence paragraphs, list-heavy chapters | No |

Word counting: CJK characters and punctuation plus Latin words, excluding Markdown syntax, code, formulas, tables, captions. Expect a few percent difference from Word's count.

## Layer 2: Review

Read the whole thesis and review it in these roles, one pass each. Use `references/review-rubric.md` for the checklist and output format. For 系统设计与实现、算法模型改进、工程设计, the 指导老师 also checks the chapter skeleton against the type template in `../../references/paper-types/`, and the 事实核查员 also checks each item of its 质量要点.

1. **格式审查员**: structure, headings, figure/table/formula numbering, reference format (GB/T 7714-2015), abstract and keywords.
2. **指导老师**: whether each chapter does its job, whether 绪论's research content matches what was done, whether design explains reasons, and the requirement chain: every requirement ID appears in a design module, its implementation, and at least one test case.
3. **盲审专家（严格版）**: the harshest reasonable external reviewer. Looks for conclusions the text does not back with data, figures, or reasoning, inflated significance, inconsistency between chapters, AI-template writing, and anything a defense committee would challenge. Gives a 盲审 verdict.
4. **事实核查员**: every claim about the project against 项目理解.md, every citation against the literature abstract, and every number for consistency across chapters and plausibility against the requirements and environment.

When subagents are available, run the four roles in parallel with the same inputs and merge the findings; otherwise run them sequentially.

## Fix Loop

1. Merge findings into `qc/审阅意见.md`, sorted 必须修改 / 建议修改 / 可选.
2. Show the user the 必须修改 list and the placeholders that only they can fill.
3. Fix the findings directly in the chapter files, keeping test results and data in final form and consistent across chapters.
4. Re-run Layer 1. Repeat until there are no blocking issues; the user decides when the 建议修改 items are done.

## Before Submission Checklist

- `thesis_qc.py` exits 0 and placeholder count is 0.
- Word file rebuilt with `md2docx_thesis.js`; open in Word, right-click the TOC → 更新域 → 更新整个目录; check page numbers, headers, figure sizes, and table breaks by eye.
- Format adjusted to the school template (fonts, sizes, margins via `--format`; cover page and declaration pages from the school template).
- User has read the full text and can explain every chapter in the defense.
- Plagiarism and AIGC detection are run on the school's designated system; this skill does not predict those scores.

## References

- `references/review-rubric.md`: role checklists, severity levels, and report format.
