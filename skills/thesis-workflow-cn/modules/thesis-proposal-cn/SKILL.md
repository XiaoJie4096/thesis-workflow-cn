---
name: thesis-proposal-cn
description: Generate usable Chinese undergraduate thesis proposal text after a thesis topic is confirmed, especially for 开题报告 sections such as 选题依据, 研究意义, 国内外研究现状, 研究内容, 研究方法, 论文提纲, 进度安排, and 预期成果. Use when the user asks to draft, complete, polish, or reorganize a Chinese本科开题报告 from a confirmed topic, literature review, retrieved literature records, school template, or existing proposal draft.
---

# Thesis Proposal CN

## Core Positioning

Use this skill to produce directly usable Chinese undergraduate thesis proposal text. Treat it as a post-retrieval, post-literature-review writing skill: the topic should already be confirmed, and literature-related sections should be based on the user's provided literature review, abstracts, or bibliographic records whenever available.

Do not output both an "analysis version" and a "paste-ready version". Unless the user explicitly asks for diagnosis or comparison, write the final proposal text directly.

## Default Boundaries

- Default to undergraduate-feasible research design.
- Do not include complex data analysis, pure theoretical modeling, difficult algorithm innovation, large-scale experiments, or research tasks beyond ordinary undergraduate capacity.
- For software/system-design topics, prefer requirements analysis, architecture/design, function implementation, testing, and optimization.
- For literature-related content, never invent authors, years, article titles, journals, data, policies, cases, or representative studies.
- If the user provides a literature review, summarize from it and preserve its scope.
- If no literature review or literature records are provided, write only a general background-style draft and briefly state that the research-status section still needs real literature support.

## Workflow

1. Identify the requested output:
   - Full proposal sections;
   - One section such as 选题依据, 研究意义, 研究现状, 研究内容, or 论文提纲;
   - Polishing or restructuring an existing proposal draft.
2. Check for the minimum inputs:
   - Thesis title or confirmed research topic;
   - Major/discipline or paper type if provided;
   - Literature review, abstracts, bibliographic records, or school template if provided.
3. Ask at most a few concise questions only when the missing information blocks a usable draft. If the title and task are clear, write immediately.
4. Read `references/proposal-writing-rules.md` before drafting full proposal text or any prose section.
5. Read `references/undergraduate-outline-rules.md` before generating or revising a thesis outline.
6. Produce clean formal Chinese text that can be placed into a proposal document with minimal editing.

## Output Rules

- Use section headings that match the user's requested template when a template is provided.
- When no template is provided, use common Chinese proposal headings: 选题依据, 研究意义, 国内外研究现状, 研究内容, 研究方法, 论文提纲, 研究进度安排, 预期成果.
- Prefer coherent paragraphs over long bullet lists for prose sections.
- Keep claims concrete and bounded; avoid empty phrases such as "具有十分重要的意义" unless followed by specific value.
- A proposal describes the research before it is carried out: write 研究内容, 研究方法, and 预期成果 as planned work (拟设计、拟实现、预期达到).

## Optional Skill Coordination

This skill may reference other skills as optional prior or follow-up steps, but must not assume they are installed or already used.

- If the topic is not confirmed, use `../undergraduate-thesis-topic/SKILL.md` or perform a brief narrowing step manually.
- If real literature records are needed, use `../cnki-cssci-search/SKILL.md` or ask the user to provide literature review materials.
- If the user provides abstracts and asks for a stronger research-status section, summarize from the provided materials directly or use `../literature-review-cn/SKILL.md`.
- If the user wants a Word document after the proposal text is approved, follow `../docx-editor-cn/SKILL.md` or the available document tools.
