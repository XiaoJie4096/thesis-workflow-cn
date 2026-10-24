# Stage Handoff

Use this compact handoff format between thesis workflow stages.

## Handoff Fields

- 论文题目: confirmed title or best current candidate.
- 论文类型: system design, empirical analysis, literature review, teaching/design case, management/business analysis, or other.
- 项目状态: implemented, partially implemented, planned/design only, dataset available, survey available, or unknown.
- 范围边界: object, scenario, method, platform, population, company/case, or module boundary.
- 文献材料: search output files, pasted records, abstract count, language channel, and relevance limits.
- 模板要求: school template, section names, typography, word count, citation style, and Word file path.
- 阶段输出: text draft path, Word `.docx` path, search record path, or other generated artifact.
- 论文项目: thesis project folder path (from stage 5 on).
- 大纲与字数: `plan/大纲.md` and `plan/字数分配.json` status (draft / user-confirmed / supervisor-confirmed) and total target.
- 素材: `materials/项目理解.md` confirmation status and the project/data paths it was built from.
- 图表: `plan/图表清单.md` status, rendered count, screenshots still owed by the user.
- 章节进度: chapters drafted with word count vs. budget.
- 下一步: one concrete next action and the skill that should handle it.
- 继续确认: the exact yes/no question asked before entering the next major stage.

## Transition Gates

Topic to retrieval:
The title or direction must be narrow enough to generate keyword groups. If not, return to topic scoping.

Retrieval to review:
The literature records must include abstracts or structured summaries. If only titles are available, ask whether to continue retrieval or write a pre-search outline only.

Review to proposal:
The confirmed title, literature review text, and literature review Word output should be available. If Word output is blocked, record the blocker and ask the user whether to continue with text-only material.

Proposal completion:
The proposal text and proposal Word output should be available. If Word output is blocked, record the blocker and ask the user whether to continue with text-only material.

Proposal to outline:
A confirmed title, thesis type, project status, and total word target must exist. The proposal's 论文提纲 is reused when present.

Outline to materials:
The user has confirmed the outline. If the user wants to wait for supervisor feedback, stop here and record it.

Materials to drafting:
The user has confirmed 项目理解.md (or explicitly said the thesis has no project materials). Literature records are in `literature/`.

Drafting to figures:
All chapter files exist, or the user asked to make figures for finished chapters first.

Figures to QC:
Agent-made figures render without errors; owed screenshots are listed.

QC to Word:
The QC findings are fixed in the chapter files. Screenshots the user has not captured yet show as image boxes in Word.

## Default Next-Step Questions

- After topic confirmation: ask whether to enter literature review preparation and drafting.
- After literature material preparation: ask whether to write the literature review and generate Word.
- After literature review Word output: ask whether to enter proposal drafting and Word generation.
- After proposal Word output: ask whether to enter the thesis body (outline and word budget first) or stop.
- After outline confirmation: ask for project/material paths and whether to start materials analysis.
- After materials confirmation: ask whether to start chapter drafting.
- After all chapters: report word count vs. budget per chapter and ask whether to produce figures.
- After figures: ask whether to run QC and mock blind review.
- After QC: ask whether to build the full thesis Word file.

## Resume Rule

When resuming a workflow, inspect existing files and thread context first. Continue from the earliest incomplete gate, not from stage 1 by default.

For the thesis body, the project folder is the state: check `plan/`, `materials/`, `chapters/`, `figures/`, and `qc/` in that order, and run `thesis_qc.py` to get current word counts and open issues before choosing the next action.
