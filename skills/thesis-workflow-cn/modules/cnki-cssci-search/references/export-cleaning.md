# Export Cleaning

Use this reference when saving CNKI export-page text as local files.

## Do Not Save Whole Page Text

CNKI export pages may include:

- Navigation text.
- Export menu labels.
- Footer and customer-service text.
- Copyright and filing records.
- Safety verification prompts.

Extract only the generated bibliographic records and abstracts. A result-page table without abstracts is not sufficient for a completed `题录摘要` output.

## Official Export Page Required For Abstracts

Use result pages for screening, relevance checks, counts, and record-ID collection. Do not use result pages as the final source for `题录摘要`.

Result pages are list pages: abstracts may be absent, fields can be split across multiple lines, and page-shell text can mix with result text. The final `题录摘要.md` must come from one of these sources:

- CNKI's official `文献管理中心 -> 查新（引文格式）` export page.
- Per-paper detail pages, when the official export page is unavailable and the user approves this slower fallback.

The official export page is acceptable only when it produces numbered records with abstracts, for example:

```text
[1]
作者. 题名[J]. 来源, 年, 卷(期): 页码.
摘要: ...
```

Convert the official citation line into the final field-label format before saving the deliverable.

If the official export page cannot be opened or does not include abstracts, do not mark the task complete. Report that abstracts were not obtained and ask whether to continue with an approved fallback.

## Preferred Extraction Boundary

For `查新（引文格式）`, the useful records normally begin after:

```text
排序
发表时间
被引频次
```

Keep section headers that you add yourself, such as export chunk labels. Remove CNKI page shell text.

## Cleanup Rules

Remove footer/verification blocks conservatively. A practical rule is to delete from:

```text
读者服务
```

through the next:

```text
安全验证
```

Do not delete by broad words that may appear in abstracts.

## Verification

After cleanup:

1. Count records using a pattern such as `^\[[0-9]+\]`.
2. Count abstracts using `摘要` markers. The abstract count must equal the record count.
3. Check that expected count equals exported count.
4. Search for leftover shell text:

```text
读者服务
购买知网卡
拖动下方拼图完成验证
安全验证
```

5. Preview the first and last records for readable Chinese and complete abstracts.

If abstracts are missing, do not mark the task complete. Report that bibliographic records were obtained but abstracts were not, then continue with an approved route such as the official `查新（引文格式）` export page or per-paper detail-page extraction.

## Final MD Format

Keep `题录摘要.md` minimal and field-based:

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
```

Use `未标明` for fields unavailable after checking the source, and `无` for fields that do not apply. Do not fabricate missing source type, venue, year, volume, issue, or pages.

Do not include relevance labels, search batches, CNKI links, database labels, cited/download counts, cleanup logs, or browser failure notes in this final MD file. Put those details in `检索记录.md`.

Use `scripts/clean_cnki_export.py` for deterministic cleanup when working from a saved text file.
