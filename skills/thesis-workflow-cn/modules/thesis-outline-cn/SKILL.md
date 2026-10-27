---
name: thesis-outline-cn
description: Build the full chapter outline and word budget for a Chinese undergraduate thesis body after the proposal is done. Use when the user asks for 论文目录, 论文大纲, 正文提纲, 章节安排, 字数分配, or wants to start writing the thesis body (正文) from a confirmed title, proposal, literature records, and project materials. Produces plan/大纲.md and plan/字数分配.json for teacher review before any chapter is drafted.
---

# Thesis Outline CN

## Core Positioning

Use this skill to turn a confirmed title, proposal, and materials into a thesis outline with a per-section word budget. The outline is the contract for every later stage: chapter writing, figure planning, and QC all read it. Do not draft chapter text in this stage.

The outline plans the finished, submitted thesis. The test chapter plans which cases, metrics, and result tables it reports; the body later writes those results as completed work.

The outline must be confirmed by the user, and the user should be told to show it to their supervisor (指导老师) before drafting. Undergraduates usually cannot judge outline quality alone; a supervisor-approved outline prevents large rewrites later.

## Inputs

Check what already exists in the thread or project folder before asking:

- Confirmed title, thesis type, and project status from the stage handoff.
- Proposal text or its 论文提纲 section, and the literature review.
- School requirements: total word count, required chapter list, template, citation style. If the school gives a chapter list, follow it first.
- Project materials summary if `modules/thesis-materials-cn` has already run.

Ask only for what blocks a usable outline. Typical blocking questions: total word count (default 10000–15000 Chinese characters for undergraduate body text if the user does not know), and whether the school prescribes chapter names.

## Workflow

1. Classify the thesis type with `references/outline-patterns.md` and open its type template in `../../references/paper-types/`; take the chapter skeleton, the variant matching the topic, and the word allocation from that template. Reuse the proposal's 论文提纲 when present; refine it instead of replacing it.
2. Map every chapter and section to the concrete topic. No generic headings such as "相关技术" when the real technology is known; write "Unity3D 引擎与 C# 脚本技术".
3. Size the sections. Each 二级节 gets at least 600 words and is written as 3–6 paragraphs directly under its heading. A chapter usually has 3–5 节, so a 12000-word body has about 20 节 in total. Merge thin topics into a neighbouring section instead of giving them their own heading. Use 三级小节 only where one section covers several parallel items, such as modules in a design chapter, issues in a diagnosis, or measures in a countermeasure section; each 小节 then gets at least 400 words.
4. Assign word budgets using the type template's 字数分配 table, scaled to the user's total; see `references/word-budget.md` for the adjustment rules. Budget at the section level; chapter totals must add up to the overall target.
5. For each section, note what it covers and the figures or tables it is expected to hold. This becomes the input to figure planning.
6. Write `plan/大纲.md` and `plan/字数分配.json` in the thesis project folder (create `<论文项目>/plan/` if needed). `大纲.md` holds the heading tree with budgets and each section's notes.
7. Show the outline in chat as a compact tree with word counts, ask the user to confirm or edit, and remind them to send it to their supervisor.

## Output Files

`plan/大纲.md`:

```markdown
# 基于Unity3D的农场类游戏的设计与实现 — 论文大纲

论文类型：系统设计与实现　项目状态：已实现　目标字数：12000

## 第1章 绪论（1600）
### 1.1 研究背景与意义（600）
要点：农场类游戏的玩家群体与玩法特点；独立开发用 Unity 实现的价值。
...
## 第4章 系统设计（3000）
### 4.1 系统总体架构设计（700）— 图：系统总体架构图
要点：分层结构，各层职责与调用关系。
### 4.2 功能模块设计（1200）
#### 4.2.1 种植模块设计（400）— 图：作物生长状态图
#### 4.2.2 背包与商店模块设计（400）— 表：物品数据字段表
#### 4.2.3 存档模块设计（400）— 图：存档流程图
...
## 第6章 系统测试（1800）
### 6.1 测试环境与功能测试（600）— 表：测试环境表、功能测试用例表（关联 F 编号）
### 6.2 性能测试（600）— 表：帧率与加载时间测试结果
### 6.3 测试结论（600）
要点：逐条对照第3章 F/N 需求，写明测得值和是否达到。
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

- Three heading levels at most inside the body (章 / 节 / 小节); most sections stop at 节.
- Each of chapters 2 to 5 carries one main research task; do not split one task across chapters or stack two tasks in one.
- Plan every section the type template calls for, including 测试, 实验, 实证结果, and 评价 sections. The section that checks results against the earlier requirements, hypotheses, or problems is its own section of at least 600 words and covers each item.
- Keep innovation claims modest and checkable.
- Abstract, references, and acknowledgements are not part of the word budget unless the school counts them.
- Stop after the outline. Do not start chapter drafting until the user confirms.

## References

- `references/outline-patterns.md`: how to pick the thesis type and its template.
- `../../references/paper-types/*.md`: full type templates (skeleton, variants, word allocation, chapter-by-chapter writing steps, figures, abstract, sentence frames, quality points).
- `references/word-budget.md`: budget adjustment rules and the word-count method.
- For the older proposal-stage outline rules, see `../thesis-proposal-cn/references/undergraduate-outline-rules.md`; keep the two consistent.
