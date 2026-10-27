---
name: thesis-body-cn
description: Draft the body chapters (正文) of a Chinese undergraduate thesis chapter by chapter from a confirmed outline, word budget, literature records, and verified project materials. Use when the user asks to 写正文, 写第X章, 写绪论/需求分析/系统设计/系统实现/测试/总结, 扩写, 改写某章, or continue drafting after the outline and materials stages. Writes Markdown chapter files in chapters/ that md2docx_thesis.js converts to Word.
---

# Thesis Body CN

## Core Positioning

Write the thesis body chapter by chapter, one file per chapter, as the finished thesis the student submits. Citations come from the literature database; the system's modules, classes, data structures, and code come from the confirmed project understanding and what the user says. Test results, experiment data, and performance figures are written as completed work: concrete values that meet the requirements, match the design parameters, and stay consistent across chapters. Screenshots stay as image references with planned filenames for the user to capture later. `【待补充：…】` is kept for facts only the user knows (names, school details). The output is Markdown following `references/markdown-conventions.md`.

## Preconditions

Before drafting, confirm these exist; if not, route back:

- `plan/大纲.md` and `plan/字数分配.json` confirmed by the user → else `modules/thesis-outline-cn`.
- `materials/项目理解.md` confirmed → else `modules/thesis-materials-cn`. Pure literature/argument theses skip this.
- Literature records (`literature/题录摘要.md` or equivalent from `cnki-cssci-search`) → else `modules/cnki-cssci-search`.

## Drafting Order

Each chapter is derived from the finished chapter before it, so chapters are written one at a time in this order:

1. 相关技术 / 理论基础
2. The core chapters in outline order, each built on the previous one:
   - 需求分析 gives every requirement an ID (F01, F02… for functional, N01… for non-functional).
   - 系统设计 derives its modules, data, and flows from those requirements and names the requirement IDs each module serves.
   - 系统实现 follows the design chapter's module order and names, and shows how each design decision is realized in code.
   - 系统测试 writes cases that cite requirement IDs and cover every requirement; the conclusion checks each requirement and each quantified target.
   - For other types the same chain holds, with the items numbered where they are first stated:
     - 算法改进：改进方法 → 实验 verifies each improvement point.
     - 工程设计：方案 → 设计计算 → 校核仿真 → 试验 checks each calculated parameter.
     - 实证：假设 H1… → 研究设计 → 实证结果 judges each hypothesis.
     - 实验：研究问题 → 材料与方法 → 结果与讨论 answers each question with its measured indicators.
     - 案例分析：问题诊断 → 对策 → 实施效果 answers each diagnosed problem.
     - 法学：争点 → 规范分析 → 完善建议 answers each issue.
     - 人文论述：each 分论点 chapter builds on the previous one, and the 结语 gathers them into one answer.
     - 设计创作：调研需求 → 设计策略 → 设计实践 → 评价 checks each requirement.
3. 绪论 (written after the core chapters so 主要研究内容 matches the finished chapters)
4. 总结与展望
5. 摘要 / Abstract / 关键词
6. 参考文献 list (generated from citations actually used) and 致谢 (short template, user fills in names)

Draft all chapters in this order in one pass, then report per chapter: file path, word count vs. budget, citations used, figures/tables referenced.

## Per-Chapter Procedure

1. Re-read this chapter's outline entries, budget, relevant parts of 项目理解.md, and the finished chapters it builds on (for 系统设计, the requirement list; for 系统实现, the design modules; for 系统测试, the requirements and their quantified targets).
2. Pick citations for the chapter from the literature records only. Note each paper's actual claim from its abstract; never cite a paper for something its abstract does not support.
3. Write the chapter into `chapters/NN-章名.md`, filling each section to its budget: a 600-word section is 3–4 paragraphs of 150–300 words, plus its figures and tables with a paragraph explaining each. Follow `references/writing-rules.md`. For chapter content, follow the matching type template in `../../references/paper-types/`: its 各章写法 steps, the variant for this topic, its figure plan, and its 句型框架 as sentence skeletons to fill with the user's own content.
4. Insert figures and tables with planned filenames (e.g. `../figures/architecture.png`) and always mention them in text before they appear. Add new needs to `plan/图表清单.md` for `modules/thesis-figures-cn`.
5. Run a quick count:

   ```bash
   python modules/thesis-qc-cn/scripts/thesis_qc.py <论文项目>
   ```

   Fix blocking issues for this chapter (missing citation target, figure mentioned but not defined) before moving on.

## Citation Handling

- In drafts, cite with the literature record's index or title key if numbering is not final, then renumber once all chapters exist. Final text uses `[n]` in order of first appearance.
- Reference count and where citations concentrate follow the type template (usually 15–30 references for undergraduates).
- Format references in GB/T 7714-2015 from the record fields. Do not fill in missing volume/issue/page numbers by guessing; leave `【待补充：页码】`.

## Hard Rules

- References come only from the literature records.
- The functions described match the project code and 项目理解.md; extensions the project does not have go into 展望.
- Code snippets come from the user's project, shortened with `// ……` where needed. When there is no project code, write snippets that match the design chapter's classes, methods, and data structures.
- Test cases, results, and data are written in final form: every result column filled, every number consistent with the requirements, the design parameters, and the other chapters. The text is written in the author's voice about completed work.
- Keep each chapter and each section within ±15% of its budget. Reach the budget with substance (design reasons, flow explanation, figure/table interpretation), not padding.
- Use the school's terminology if given; otherwise keep terms consistent with the outline and 项目理解.md.

## References

- `references/markdown-conventions.md`: Markdown syntax for headings, figures, tables, formulas, citations, placeholders.
- `references/writing-rules.md`: academic Chinese style and de-AI rules.
- `references/chapter-guides.md`: general rules for 摘要, 致谢, and topics that fit no type template.
- `../../references/paper-types/*.md`: type templates, one per thesis type; `../thesis-outline-cn/references/outline-patterns.md` lists them.
