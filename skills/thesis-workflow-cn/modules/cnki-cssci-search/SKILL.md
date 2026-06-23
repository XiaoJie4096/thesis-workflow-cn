---
name: cnki-cssci-search
description: Use for Chinese CNKI/知网 CSSCI or C-journal searches, English/foreign literature title-and-abstract retrieval, or combined Chinese-English literature searches that need target paper-count negotiation, split keyword batches, relevance grading, mandatory abstracts, clean Markdown outputs, and transparent search records. Trigger when the user asks to search CNKI/知网, find CSSCI/C刊 papers, retrieve English/foreign papers, export records/abstracts, or avoid off-topic literature-search results.
---

# CNKI CSSCI And Foreign Literature Search

Use CNKI's official advanced search and export pages to produce reproducible CSSCI/C-journal bibliographic records with abstracts. When English/foreign literature is requested, use structured metadata APIs such as OpenAlex, Crossref, and PubMed to retrieve titles and abstracts. Prefer split keyword batches over one broad expression, and separate directly relevant papers from nearby support and theoretical background.

This skill replaces older one-shot CNKI advanced-search workflows.

## First Response

Before searching, ask the user for the target export count if it is not already explicit.

For Chinese-only searches:

```text
你希望最终导出多少篇文献？
```

For combined Chinese-English searches:

```text
中文文献需要多少篇？英文文献需要多少篇？
```

Also clarify scope only when needed:

- CSSCI only, C-journal, 北大核心, or another source filter.
- English/foreign source scope such as cross-disciplinary, biomedical, education, engineering, or another field.
- Whether the user wants strict relevance only or may include nearby/theoretical support.
- Preferred output format and destination if local files will be generated.

Do not start live retrieval until the needed target count is known for every requested language channel.

## Core Workflow

Choose the requested channels first:

- Chinese channel: CNKI/CSSCI or other Chinese source filters.
- English channel: foreign title-and-abstract retrieval through structured metadata APIs.
- Combined channel: run Chinese and English channels separately, then produce separate final files and one combined search record.

### Chinese Channel

1. Parse the user's topic into core concepts: object/domain, method/theory, technology/tool, scene/application, and outcome when present.
2. Build split keyword groups instead of one large query:
   - Group A: directly relevant words from the user's exact topic.
   - Group B: nearby support words for method, theory, design, evaluation, or application.
   - Group C: theoretical/background words that may support the literature review but are not direct matches.
3. For each group, search by descending combination order:
   - Search the full intersection of all terms in the group first.
   - If the full intersection meets the target with acceptable relevance, stop within that group.
   - If lower-order combinations are needed, complete all combinations at that order before judging sufficiency.
   - Do not stop midway within an order because one combination supplied enough records.
4. Confirm the group plan with the user when keywords require interpretation or expansion.
5. Run CNKI advanced search with the requested source filter.
6. Record every batch: keyword(s), combination order, total result count, academic-journal count, CSSCI/C-journal count, filtered count, keep/export count, and reason.
7. Select papers toward the target count in this order:
   - Directly relevant first.
   - Nearby support only if direct results are insufficient or the user allowed it.
   - Theoretical background only if still short or explicitly requested.
8. Use result pages for screening and record-ID collection only; final bibliographic abstracts must come from CNKI's official "查新（引文格式）" export page or per-paper detail pages.
9. Clean extracted export text before saving; never save whole-page text without cleanup.
10. Verify both record count and abstract count. A bibliographic list without abstracts is not a completed "题录摘要" deliverable.
11. Report limitations plainly.

### English Channel

1. Translate the user's topic into conservative English search concepts: object/domain, method/theory, technology/tool, scene/application, and outcome when present.
2. Build 2-3 query variants: direct phrase, synonym/nearby expression, and abbreviation/full-name form when useful.
3. Prefer structured metadata APIs over browser scraping:
   - OpenAlex for cross-disciplinary discovery and abstracts.
   - Crossref for DOI, citation metadata, venue, and metadata completion.
   - PubMed for biomedical topics.
4. Collect candidates first, then fetch abstracts for selected candidates.
5. Deduplicate by DOI, then PMID, then normalized title plus year.
6. Keep only records with a real abstract in the final English output. If a candidate has no abstract after checking available sources, put it in the search record as an unused candidate, not in the final deliverable.
7. Stop only when the requested English count is reached with abstracts, or report the shortfall plainly.
8. For detailed English-source routing, read `references/foreign-literature-access.md`.

## Relevance Contract

Never present expanded/background papers as direct hits.

Use these labels in records and final reports:

- `直接相关`: closely matches the topic's object/domain plus method/tool/scene.
- `近邻相关`: supports design method, evaluation, application, user experience, mechanism, or adjacent cases.
- `理论扩展`: supports background, literature review, broader theory, or field context.
- `剔除`: keyword hit is off-topic, ambiguous, non-target source, duplicate, or not useful for the stated goal.

If the target count cannot be met without lowering relevance, stop and tell the user exactly how many strict papers were found before expanding.

## Browser And CNKI Rules

- Use supervised browser automation available in the current Codex environment.
- Do not bypass login, institution access, paid access, rate limits, CAPTCHA, or CNKI controls.
- Hidden DOM text such as "安全验证" is not itself a block. Stop only when a visible verification page or form appears.
- Prefer CNKI official pages and export tools. Do not treat cleaned result-page lists as completed abstract exports. If native browser download is unavailable, state that the file is a local cleaned extraction from the official export page.
- For detailed browser steps, read `references/browser-workflow.md`.
- For split-search design and relevance rules, read `references/split-search-method.md`.
- For export cleanup requirements, read `references/export-cleaning.md`.

## Completion Gate

For Chinese output, treat the task as complete only when all of these are true:

- The actual exported record count is known.
- Every exported record has structured bibliographic fields.
- Every exported record has an abstract beginning with `摘要`.
- The record count equals the abstract count.
- Cleanup verification finds no CNKI footer, customer-service, or safety-verification text.

If abstracts are missing, do not say the export is complete. Say that only bibliographic records were obtained, explain why abstracts were not obtained, and ask whether to continue with the official export page or per-paper detail-page extraction.

For English output, treat the task as complete only when all of these are true:

- The actual delivered English record count is known.
- Every delivered record has structured bibliographic fields.
- Every delivered record has a real abstract.
- Every delivered record has `abstract_status: found` in the working data or search record.
- The delivered count equals the requested English count.

If English abstracts are missing, do not include those candidates in the final English title-and-abstract file. Record them as unused candidates and report the shortfall.

## Local Output Files

For Chinese-only searches, create only two default files:

```text
CNKI_CSSCI_<主题短名>_题录摘要_<N>条.md
CNKI_CSSCI_<主题短名>_检索记录.md
```

For combined Chinese-English searches, create only these default files:

```text
CNKI_CSSCI_<主题短名>_题录摘要_<N>条.md
Foreign_<主题短名>_题目摘要_<M>条.md
中英文文献检索记录.md
```

Do not create `.txt` or `.doc` output by default. Create Word-compatible output only when the user explicitly asks for Word or `.doc`.

### Chinese Bibliographic Abstract MD

The Chinese `题录摘要.md` file must be clean and structured. Include only the required bibliographic fields and abstract:

```markdown
# CNKI题录摘要

## [1]
作者：...
题名：...
文献类型/来源类型：期刊论文
期刊名/出版社/学校/会议名：...
年份：...
卷(期)：...
页码：...

摘要：...

## [2]
作者：...
题名：...
文献类型/来源类型：学位论文
期刊名/出版社/学校/会议名：...
年份：...
卷(期)：无
页码：...

摘要：...
```

Use `期刊论文`, `学位论文`, `专著`, `会议论文`, or another accurate source type. If a field is unavailable after checking the source, write `未标明`; if a field is not applicable, write `无`. Do not fabricate missing volume, issue, pages, venue, or source type.

Do not include these per-record fields in `题录摘要.md`:

- relevance label
- search batch
- CNKI URL
- database field
- cited/download counts
- browser/export failure notes
- cleanup logs

Put process details in `检索记录.md`, not in `题录摘要.md`.

### English Title Abstract MD

The English `题目摘要.md` file should mirror the Chinese field-label format and stay minimal. Keep English titles and abstracts in English:

```markdown
# English Titles and Abstracts

## [1]
作者：...
题名：...
文献类型/来源类型：期刊论文
期刊名/出版社/学校/会议名：...
年份：...
卷(期)：...
页码：...

Abstract: ...

## [2]
作者：...
题名：...
文献类型/来源类型：会议论文
期刊名/出版社/学校/会议名：...
年份：...
卷(期)：无
页码：...

Abstract: ...
```

Use the same missing-field rules as Chinese output: `未标明` for unavailable fields and `无` for non-applicable fields. Do not include DOI, source-platform labels, query batches, relevance labels, API logs, raw JSON, or missing-abstract candidates in the final English file unless the user explicitly asks for DOI.

### Search Record MD

The `检索记录.md` or `中英文文献检索记录.md` file should contain:

- Topic, target count, actual count, source filter, and abstract status.
- Chinese batch table with group, combination order, search terms, counts, kept count, and notes.
- English query variants, source platforms checked, candidate count, kept count, and abstract-completeness status when English literature is requested.
- Kept-title list with relevance labels and reasons.
- English unused-candidate list when records were excluded because abstracts were missing.
- Removed/off-topic patterns when useful.
- Limitations and verification results.

## Final Chat Response

Keep the final chat response short. Include:

- Target export count and actual export count.
- Database/source filters and English metadata sources used.
- Abstract status: complete or incomplete.
- Output file paths.
- Any limitation such as unavailable native download, missing abstracts, login/CAPTCHA blocks, or insufficient strict results.
