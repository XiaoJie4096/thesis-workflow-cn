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
- 不能声称: unverified implementation, unavailable data, fabricated references, experiments, tests, or external facts.
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

## Default Next-Step Questions

- After topic confirmation: ask whether to enter literature review preparation and drafting.
- After literature material preparation: ask whether to write the literature review and generate Word.
- After literature review Word output: ask whether to enter proposal drafting and Word generation.
- After proposal Word output: ask whether to continue to later thesis-body work or stop.

## Resume Rule

When resuming a workflow, inspect existing files and thread context first. Continue from the earliest incomplete gate, not from stage 1 by default.
