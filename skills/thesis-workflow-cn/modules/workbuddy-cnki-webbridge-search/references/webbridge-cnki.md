# Kimi WebBridge CNKI Execution Notes

Use this reference only after reading `$kimi-webbridge`.

## Connection Guard

On Windows, if the Kimi WebBridge command endpoint is unavailable, start the daemon once:

```powershell
& "$env:USERPROFILE\.kimi-webbridge\bin\kimi-webbridge.exe" start
```

Then retry the WebBridge command. Do not run stop, restart, or uninstall automatically.

## Request Encoding

When sending WebBridge commands on Windows, never inline Chinese JSON in PowerShell. Write each request body to a uniquely named UTF-8 JSON temp file, post it with `curl.exe --data-binary`, then delete the temp file.

Use one stable session name for the whole retrieval, such as:

```text
workbuddy-cnki-retrieval
```

The first CNKI navigation should set a visible group title such as:

```text
WorkBuddy 知网检索
```

## Browser-Only Boundary

Allowed:

- `navigate` to CNKI official pages.
- `snapshot` to inspect visible controls.
- `click`, `fill`, `evaluate`, `cdp`, and `screenshot` when needed for CNKI UI interaction.
- `network` only to inspect the current CNKI browser session, not to replace CNKI with another data source.

Forbidden:

- Web search, search_query, generic webpage search, or search engine queries.
- Using third-party pages as a replacement for CNKI records.
- Bypassing CNKI login, CAPTCHA, institution access, paid access, or rate limits.

## CNKI Start URL

Open CNKI advanced search in the real browser:

```text
https://kns.cnki.net/kns8s/AdvSearch
```

Continue with `../cnki-cssci-search/SKILL.md` and its `references/browser-workflow.md` for source filters, result collection, export URL handling, and cleanup.
