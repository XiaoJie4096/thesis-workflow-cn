---
name: thesis-outline-cn
description: Build the full chapter outline and word budget for a Chinese undergraduate thesis body after the proposal is done. Use when the user asks for 论文目录, 论文大纲, 正文提纲, 章节安排, 字数分配, or wants to start writing the thesis body (正文) from a confirmed title, proposal, literature records, and project materials. Produces plan/大纲.md and plan/字数分配.json for teacher review before any chapter is drafted.
---

# Thesis Outline CN

## Core Positioning

Use this skill to turn a confirmed title, proposal, and materials into a three-level thesis outline with a per-section word budget. The outline is the contract for every later stage: chapter writing, figure planning, and QC all read it. Do not draft chapter text in this stage.

The outline must be confirmed by the user, and the user should be told to show it to their supervisor (指导老师) before drafting. Undergraduates usually cannot judge outline quality alone; a supervisor-approved outline prevents large rewrites later.

## Inputs

Check what already exists in the thread or project folder before asking:

- Confirmed title, thesis type, and project status from the stage handoff.
- Proposal text or its 论文提纲 section, and the literature review.
- School requirements: total word count, required chapter list, template, citation style. If the school gives a chapter list, follow it first.
- Project materials summary if `modules/thesis-materials-cn` has already run.

Ask only for what blocks a usable outline. Typical blocking questions: total word count (default 10000–15000 Chinese characters for undergraduate body text if the user does not know), and whether the school prescribes chapter names.

## Workflow

1. Classify the thesis type and pick the base pattern from `references/outline-patterns.md`. For 系统设计与实现、算法模型改进、工程设计, it points to the type template in `../../references/paper-types/`; take the chapter skeleton, the variant matching the topic, and the word allocation from that template. Reuse the proposal's 论文提纲 when present; refine it instead of replacing it.
2. Map every chapter and section to the concrete topic. No generic headings such as "相关技术" when the real technology is known; write "Unity3D 引擎与 C# 脚本技术".
3. Check feasibility against project status. If the project is planned or partial, sections about implementation and testing must be framed as design, prototype, or test plan. Do not create sections that need data, experiments, or features the user does not have.
4. Assign word budgets using the type template's 字数分配 table, or the ratios in `references/word-budget.md` for the other types, scaled to the user's total. Budget at the section level; chapter totals must add up to the overall target.
5. For each section, list its main evidence source (文献 / 源码 / 截图 / 数据 / 用户口述) and the figures or tables it is expected to hold. This becomes the input to the materials gap check and figure planning.
6. Write `plan/大纲.md` and `plan/字数分配.json` in the thesis project folder (create `<论文项目>/plan/` if needed).
7. Show the outline in chat as a compact tree with word counts, ask the user to confirm or edit, and remind them to send it to their supervisor.

## Output Files

`plan/大纲.md`:

```markdown
# 基于Unity3D的农场类游戏的设计与实现 — 论文大纲

论文类型：系统设计与实现　项目状态：已实现　目标字数：12000

## 第1章 绪论（1500）
### 1.1 研究背景（400）— 来源：文献[综述]
### 1.2 研究目的及意义（300）— 来源：文献、开题报告
...
## 第4章 系统设计（3000）
### 4.1 系统总体架构设计（600）— 来源：源码目录结构 — 图：系统总体架构图
### 4.3 数据存储设计（700）— 来源：存档脚本 — 表：存档数据结构表
...
```

`plan/字数分配.json` (read by `thesis_qc.py`; `title` must match the chapter's `#` heading text exactly):

```json
{
  "total": 12000,
  "chapters": [
    {"title": "第1章 绪论", "target": 1500,
     "sections": [{"title": "1.1 研究背景", "target": 400}]}
  ]
}
```

## Hard Rules

- Three heading levels at most inside the body (章 / 节 / 小节).
- Each of chapters 2 to 5 carries one main research task; do not split one task across chapters or stack two tasks in one.
- Plan every section the type template calls for, including 测试, 实验, and 性能 sections.
- Keep innovation claims modest and checkable.
- Abstract, references, and acknowledgements are not part of the word budget unless the school counts them.
- Stop after the outline. Do not start chapter drafting until the user confirms.

## References

- `references/outline-patterns.md`: chapter patterns by thesis type with typical figures and tables.
- `../../references/paper-types/*.md`: full type templates (skeleton, variants, word allocation, chapter-by-chapter writing steps, figures, abstract, sentence frames, quality points).
- `references/word-budget.md`: chapter and section ratios and adjustment rules.
- For the older proposal-stage outline rules, see `../thesis-proposal-cn/references/undergraduate-outline-rules.md`; keep the two consistent.
