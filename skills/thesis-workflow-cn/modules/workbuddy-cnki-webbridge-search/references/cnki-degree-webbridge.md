# CNKI Degree Dissertation Retrieval With WebBridge

Use this reference for WorkBuddy CNKI master or doctoral dissertation retrieval. Continue to obey the browser-only boundary in `webbridge-cnki.md`: use Kimi WebBridge and CNKI official pages, never web search or search engines.

## Direct Result URLs

Prefer direct CNKI result URLs for degree dissertation searches because they avoid fragile advanced-search form input and Vue state-update issues.

Master dissertations:

```text
https://kns.cnki.net/kns8s/search?kw={url_encoded_keywords}&korder=SU&dbcode=CMFD
```

Doctoral dissertations:

```text
https://kns.cnki.net/kns8s/search?kw={url_encoded_keywords}&korder=SU&dbcode=CDMD
```

Default rules:

- Search `CMFD` and `CDMD` separately, then deduplicate and merge.
- Do not use `dbcode=CDMD,CMFD`; CNKI may reject combined values.
- Do not depend on `CDFD` as the default combined degree-dissertation entry; use separate `CMFD` and `CDMD` searches instead.
- Use `CJFD` only for journal searches, not for degree dissertations.

## Keyword Strategy

Use Chinese concepts first for dissertation databases. Chinese dissertations often use Chinese terms where English abbreviations miss records.

For emerging or mixed Chinese-English topics, search 3-5 keyword variants:

- Chinese full concept, such as `生成式人工智能 动画`.
- English abbreviation angle, such as `AI 动画创作` or `AIGC 动画`, when relevant.
- Technical method angle, such as `扩散模型 视频生成`.
- Application or subdomain angle, such as `人工智能 二维动画`.
- Method-output angle, such as `图生视频 动画`.

Record each keyword, database code, visible result count, kept count, and reason in the search record.

## WebBridge Batch Pattern

For multiple keyword/database combinations, prefer a small Python driver that calls the Kimi WebBridge command endpoint and handles URL encoding, waiting, evaluation, parsing, and deduplication in Python.

Use the WebBridge endpoint:

```text
http://127.0.0.1:10086/command
```

Use one stable session for the whole run, such as `workbuddy-cnki-retrieval`.

Recommended pattern:

```python
import time
from urllib.parse import quote

import requests

ENDPOINT = "http://127.0.0.1:10086/command"
SESSION = "workbuddy-cnki-retrieval"


def command(action, args):
    return requests.post(
        ENDPOINT,
        json={"action": action, "args": args, "session": SESSION},
        timeout=30,
    ).json()


for keyword, dbcode in searches:
    url = f"https://kns.cnki.net/kns8s/search?kw={quote(keyword)}&korder=SU&dbcode={dbcode}"
    command("navigate", {"url": url, "newTab": True, "group_title": "WorkBuddy 知网检索"})
    time.sleep(4)
    text = command("evaluate", {"code": "document.body.innerText"})["value"]
    # Parse text, collect candidates, deduplicate by normalized title + author + year.
```

If embedding JavaScript in Python strings becomes fragile, keep JavaScript simple, prefer single quotes inside JS, or store complex JavaScript in a separate temporary `.js` file and read it into Python before posting.

## Waiting And Verification

Treat navigation completion as "navigation started", not as "CNKI results rendered".

Default wait values:

- Search result list: wait 3-4 seconds.
- Dissertation detail or abstract page: wait 4-5 seconds.
- Advanced-search page with dropdowns: wait about 5 seconds.

After waiting, verify page state by checking visible text, result rows, title text, or extracted counts. Do not rely on sleep alone.

## Result-Page Field Mapping

Degree dissertation result rows differ from journal result rows.

Typical innerText row shape:

```text
1\t标题\t作者\t学校\t年份\t引用数
```

Map fields as:

- `[1]`: title
- `[2]`: author
- `[3]`: school or degree-granting institution
- `[4]`: year

Do not reuse journal field mapping blindly. Journal rows commonly map the third content field to journal/source name, while degree rows map it to school.

## Text Extraction

For result lists and abstracts, `document.body.innerText` is often the most stable first extraction target because it avoids brittle CSS selectors.

Use DOM queries inside `evaluate` when you need hrefs, checkbox values, record IDs, or other attributes. Do not expect plain `innerText` to preserve DOM structure.

## Dissertation Abstract Extraction

Dissertation detail pages may contain two visible "摘要" occurrences:

- A navigation or table-of-contents label.
- The actual abstract heading, commonly `摘要：`.

Prefer the heading with a colon:

```python
body = page_text

start = body.find("摘要：")
if start < 0:
    start = body.find("摘要:")
if start < 0:
    start = body.find("摘要")

kw = body.find("关键词", start if start >= 0 else 0)

if start >= 0 and kw > start:
    abstract = body[start + 3:kw].strip()
else:
    abstract = ""
```

For `摘要:` with a half-width colon, adjust the offset if needed after inspecting the extracted prefix. Always verify that the extracted text is the body abstract, not a sidebar or table-of-contents fragment.

## CAPTCHA And Access Blocks

If CNKI shows a visible CAPTCHA, safety verification, login prompt, or institution-access prompt, ask the user to complete it in the browser and continue afterward. Do not bypass it and do not fall back to web search.

Direct result URLs may reduce interaction with fragile forms, but they are not a CAPTCHA bypass and must not be described that way.
