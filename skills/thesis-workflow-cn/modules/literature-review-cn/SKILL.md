---
name: literature-review-cn
description: Write Chinese literature reviews from a user-provided thesis title or research direction, reference abstracts, and optional template or formatting requirements. Use when Codex needs to draft, expand, organize, or polish a 文献综述/研究综述 based on provided literature summaries, especially for Chinese undergraduate thesis writing with structured sections, user-provided format compliance, non-fragmented paragraphs, citation/reference consistency, and GB/T 7714-2015 reference formatting.
---

# Literature Review CN

Use this skill to write a Chinese literature review from a user-provided thesis title or research direction and reference abstracts.

## Workflow

1. Before writing, ask the user to upload or paste the literature review template or formatting requirements. If the user says there is no template or requirement, use the default structure and rules.
2. Check whether the user provided a thesis title or research direction.
3. Check whether the user provided reference abstracts, literature summaries, or structured research notes.
4. If the template/format decision, title/direction, or literature material is missing, ask for the missing input before writing the review.
5. If the inputs are present, write the literature review directly unless the user asks for diagnosis, outline-only work, or revision.
6. Follow the user's template or formatting requirements first, then follow the detailed default writing rules in `references/review-writing-rules.md` for any unspecified parts.

## Hard Rules

- Write in Chinese by default.
- If the user provides a literature review template or formatting requirements, follow them for section names, order, length, citation style, typography-related instructions, and reference style wherever they do not conflict with the anti-fabrication rules.
- If the user explicitly says there is no template or formatting requirement, use the default structure and rules in this skill.
- Base the review on the user-provided reference abstracts or literature summaries.
- Do not cite literature outside the provided abstracts.
- Do not invent nonexistent authors, years, titles, journals, publishers, methods, findings, or references.
- Build the final reference list only from the bibliography or abstract records provided by the user; do not infer, reconstruct, or add references from general knowledge or from the review text.
- Format the final reference list according to GB/T 7714-2015 as far as the provided bibliographic metadata allows.
- If bibliographic fields are missing, preserve available fields and do not invent missing author, title, source, year, volume, issue, page range, DOI, publisher, school, or document type information.
- Keep the required structure: title, 提要/前言, 正文, 总结, 参考文献.
- Write at least 3000 Chinese characters unless the user requests another length.
- Keep body paragraphs coherent and developed; avoid one-sentence paragraphs and list-like fragments.
- Use citations such as `作者（年份）` or `文献[编号]`, and keep them consistent with the reference list.
- Include at least 15 references when the user has supplied enough references.

## Output Style

Prefer integrated academic prose over bullet lists in the final review. Use readable transitions, group related studies before discussing representative works, and avoid ending sections with thin single-sentence claims.
