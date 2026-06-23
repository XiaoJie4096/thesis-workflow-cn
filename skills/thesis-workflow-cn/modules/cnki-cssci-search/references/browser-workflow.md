# Browser Workflow

Use this reference when executing live CNKI searches in a browser.

## Page Setup

Open:

```text
https://kns.cnki.net/kns8s/AdvSearch
```

Wait for the page to settle. Inspect visible controls before clicking. CNKI may keep hidden verification text in the DOM; do not treat hidden text alone as a block.

## Literature Type And Source Filter

1. Select `学术期刊` when the user asks for journal papers.
2. Select the requested source category, normally `CSSCI` for CSSCI/C-journal work.
3. If source filters are easier to apply on the results page than on the advanced page, run the keyword first, then use the left-side `来源类别` facet.
4. Confirm the visible filtered result count after selecting `CSSCI`.

## Search Rows

- Use `主题` by default unless the user asks for title, author, source, or full-text searching.
- CNKI operators inside an input:
  - ` + ` means OR.
  - ` * ` means AND.
  - ` - ` means NOT.
- Keep spaces around operators.
- For split-search mode, follow the combination order defined in `split-search-method.md`. Avoid one expression that mixes direct, nearby, and background groups.

## Results Page

For each batch, capture:

- Total result count.
- Academic-journal count if visible.
- CSSCI/C-journal facet count.
- Count after selecting the source facet.
- Top visible records and obvious off-topic patterns.

Use page size 50 when available. Sort by relevance unless the user asks for citation count; citation sorting can surface high-citation but off-topic papers.

## Export

Use CNKI's export path:

```text
导出与分析 -> 导出文献 -> 查新（引文格式）
```

The official export page is usually:

```text
https://kns.cnki.net/dm8/manage/export.html?displaymode=NEW&filename=...
```

`filename` is a comma-separated list of encrypted record IDs from selected result checkboxes.

If a URL with too many IDs fails, split exports into chunks of about 20 records and combine cleaned text afterward. Save cleaned `.md` output by default; create Word-compatible output only when the user explicitly asks for it.

## CookieName Export URL

When the `导出与分析` menu is unstable because of hover layers, scroll position, or click handling, use the same official export page by collecting record IDs from the result page.

Each result row normally has a checkbox like:

```html
<input name="CookieName" type="checkbox" value="encrypted-record-id" />
```

The `value` is the record ID used by CNKI's export system. A stable workflow is:

1. Collect `input[name="CookieName"]` values for the selected result rows.
2. Deduplicate IDs.
3. Split IDs into chunks of about 20 records to avoid overly long URLs.
4. URL-encode IDs and join them with English commas.
5. Open the official export page:

```text
https://kns.cnki.net/dm8/manage/export.html?displaymode=NEW&filename=ID1,ID2,ID3
```

6. Confirm the page is `文献管理中心` and the mode is `查新（引文格式）`.
7. Extract records only if the page contains both numbered records and abstracts.

This still uses CNKI's official export page. Do not use it to bypass login, institution access, CAPTCHA, paid access, or other CNKI controls.

## Pagination Fallbacks

Prefer visible pagination controls when they work. If click-based pagination is unstable, use CNKI's keyboard navigation when the page indicates that arrow keys are supported.

Fallback workflow:

1. Collect current-page `CookieName` IDs.
2. Send `ArrowRight`.
3. Wait for the result list to refresh.
4. Verify that the page marker changed, such as `1/65` to `2/65`.
5. Verify that collected IDs are new, not duplicates from the previous page.
6. Repeat until the planned page count or target candidate count is reached.

Do not assume the key press succeeded. Always verify both page number and ID uniqueness after each page turn.

## Failure Handling

- Visible CAPTCHA or safety verification: ask the user to complete it, then continue.
- Login or institutional-access prompt: ask the user to sign in or confirm access.
- Native download unsupported: use cleaned text extraction from the official export page only after stating the limitation.
- Missing export option: record the last successful step and ask whether to use a fallback extraction.
