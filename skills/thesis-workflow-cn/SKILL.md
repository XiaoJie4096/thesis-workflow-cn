---
name: thesis-workflow-cn
description: Main entry skill for Chinese undergraduate thesis workflows. Use first when the user asks for thesis topic selection, literature retrieval, literature review, proposal drafting, Word conversion, "完整流程", "从选题到综述/开题/成稿", or any task that may involve thesis-related modules. This is the single public workflow entrypoint; it routes internally to modules/undergraduate-thesis-topic, modules/cnki-cssci-search, modules/workbuddy-cnki-webbridge-search, modules/literature-review-cn, modules/thesis-proposal-cn, and modules/docx-editor-cn, asks whether to continue after each completed stage, and defaults to generating Word documents for literature reviews and proposal reports.
---

# Thesis Workflow CN

## Overview

Use this skill as the single public entry point for Chinese undergraduate thesis work. Route all thesis-related requests through this workflow first, then delegate stage-specific work to internal modules under `modules/`.

Do not duplicate the long rules from internal modules. Read and follow the relevant module `SKILL.md` when a stage becomes active.

After each stage is completed, stop and ask the user whether to continue to the next stage. Do not silently proceed to the next major stage unless the user has already explicitly asked for an uninterrupted end-to-end run.

## Internal Modules

- Topic selection and scoping: `modules/undergraduate-thesis-topic/SKILL.md`
- Chinese CNKI/CSSCI/C-journal and English title-abstract retrieval: `modules/cnki-cssci-search/SKILL.md`
- WorkBuddy-only CNKI/知网 retrieval: `modules/workbuddy-cnki-webbridge-search/SKILL.md`
- Chinese literature review drafting or polishing: `modules/literature-review-cn/SKILL.md`
- Chinese undergraduate thesis proposal drafting or polishing: `modules/thesis-proposal-cn/SKILL.md`
- Word document creation, template filling, and `.docx` editing: `modules/docx-editor-cn/SKILL.md`

If a listed module is unavailable in the current environment, continue manually with the same stage boundaries and state the limitation. `$kimi-webbridge` remains an external browser-control skill and must still be read when the WorkBuddy CNKI module requires it.

## Workflow

1. Establish the current stage and existing materials:
   - Major, rough direction, or confirmed title.
   - Whether there is a real system, dataset, survey, experiment, internship case, or only a planned/design project.
   - School template, word count, document format, and deadline if provided.
   - Existing literature records, abstracts, literature review, proposal draft, or Word template.
2. Route to the earliest missing stage. Do not ask the user to restate information that is already present in the thread.
3. Produce the stage output that can become the next stage input.
4. For literature review and proposal stages, create both the text deliverable and a Word `.docx` deliverable by default unless the user explicitly requests text only.
5. At each transition, summarize the handoff in a compact "阶段交接" block: confirmed title, scope, evidence/materials, output files, open gaps, and next recommended action.
6. Ask a concrete next-step question after each completed stage, using the next stage in the default chain.
7. Preserve confirmed constraints across stages, especially implementation status, thesis type, word count, template requirements, citation rules, and anti-fabrication limits.

## Default Stage Chain

Use this chain unless the user asks to skip or start from a later stage:

1. 选题确认: read `modules/undergraduate-thesis-topic/SKILL.md`
2. 文献材料准备: read `modules/workbuddy-cnki-webbridge-search/SKILL.md` for WorkBuddy CNKI/知网 retrieval, `modules/cnki-cssci-search/SKILL.md` for ordinary real literature retrieval, or use user-provided literature records when already available
3. 文献综述写作并转 Word: read `modules/literature-review-cn/SKILL.md`, then `modules/docx-editor-cn/SKILL.md`
4. 开题报告写作并转 Word: read `modules/thesis-proposal-cn/SKILL.md`, then `modules/docx-editor-cn/SKILL.md`

Do not require a separate "Word document" final stage for 文献综述 or 开题报告. Word generation is part of those stages.

## Continuation Prompts

At the end of each completed stage, ask only one concise continuation question:

- After topic confirmation: "题目已确认。是否进入文献综述阶段？我会先确认/准备文献材料，然后写综述并自动转成 Word。"
- After literature retrieval or literature material confirmation: "文献材料已准备好。是否开始写文献综述并生成 Word 文档？"
- After literature review Word output: "文献综述和 Word 文档已完成。是否进入开题报告阶段？我会基于题目和综述写开题报告并自动转成 Word。"
- After proposal Word output: "开题报告和 Word 文档已完成。是否继续进入后续论文正文或其他材料整理？"

If the user says yes, continue with the next stage. If the user says no, stop and keep the handoff ready for later resumption.

## Stage Routing

### Stage 1: Topic

Read `modules/undergraduate-thesis-topic/SKILL.md` when the topic is broad, missing, too large, or needs feasibility comparison.

Exit only when there is a confirmed or recommended title plus a clear thesis type, research object, scope boundary, and evidence/material plan.

After exit, ask whether to enter the literature review path. If literature records are missing, the next action is literature material preparation before drafting the review.

### Stage 2: Literature Retrieval

Read `modules/workbuddy-cnki-webbridge-search/SKILL.md` when the request is for WorkBuddy/workbuddy and needs CNKI/知网, CSSCI, C-journal, C刊, Chinese journal records, bibliographic records, abstracts, or a literature database. In this route, do not use web search/search_query or search engines; the module must use Kimi WebBridge and CNKI's official website.

Read `modules/cnki-cssci-search/SKILL.md` for ordinary non-WorkBuddy Chinese or English literature records, abstracts, or literature database retrieval.

Before retrieval, confirm target counts for each language channel. Treat bibliographic records without abstracts as incomplete if abstracts were requested.

Exit only when the literature output paths or pasted records are available, the actual count is known, and missing abstracts or relevance compromises are clearly marked.

If the user already supplied usable records and abstracts, this stage can be marked complete without live retrieval. Then ask whether to write the literature review and generate Word.

### Stage 3: Literature Review

Read `modules/literature-review-cn/SKILL.md` when the user needs a 文献综述/研究综述 from provided abstracts or literature records.

Ask for the review template or formatting requirements before writing unless the user already said there is no template. Do not cite records outside the provided materials.

Exit with:

- A usable literature review draft.
- A reference list built only from supplied metadata.
- A generated Word `.docx` file created by following `modules/docx-editor-cn/SKILL.md`, using the user's template or default Chinese academic formatting.

If Word generation cannot be completed because a template, dependency, or render step is blocked, report the exact blocker and keep the text draft as the stage output.

### Stage 4: Proposal

Read `modules/thesis-proposal-cn/SKILL.md` after the title is confirmed and enough background or literature material exists.

When the literature review or records are not available, keep the research-status section general and mark that real literature support is still needed.

Exit with:

- Proposal sections that match the user's template when provided.
- A generated Word `.docx` file created by following `modules/docx-editor-cn/SKILL.md`, using the user's template or default Chinese academic formatting.

If Word generation cannot be completed because a template, dependency, or render step is blocked, report the exact blocker and keep the text draft as the stage output.

### Word Handling Inside Stages

Read `modules/docx-editor-cn/SKILL.md` whenever a stage says to generate Word, when the user provides a `.docx` template, or when the user asks for document formatting.

Identify source content and destination template before editing. For `.doc` templates, convert to `.docx` first. Do not claim visual layout correctness unless render or visual verification succeeds.

## Hard Rules

- Do not fabricate references, completed development, experiments, survey data, test results, institutional requirements, or template contents.
- When the project is not actually implemented, write it as planned design, expected implementation, prototype, or system architecture work.
- Prefer Chinese for Chinese thesis deliverables.
- Keep final answers stage-aware: say what stage was completed, what artifact was produced, and what remains.
- When the user asks for the full workflow, execute the current stage, then ask whether to proceed to the next stage.
- Do not bypass the continuation question between major stages unless the user explicitly requests a continuous full run.

## Reference

Read `references/stage-handoff.md` when managing a multi-turn workflow, resuming from existing artifacts, or deciding what information must be carried from one child skill to the next.
