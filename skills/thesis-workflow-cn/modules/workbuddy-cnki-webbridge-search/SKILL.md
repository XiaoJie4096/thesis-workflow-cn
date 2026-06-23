---
name: workbuddy-cnki-webbridge-search
description: WorkBuddy-only CNKI/知网 literature retrieval workflow that must use Kimi WebBridge and the official CNKI website instead of web search. Use when WorkBuddy, workbuddy, or a WorkBuddy agent needs CNKI/知网, CSSCI, C-journal, C刊, Chinese journal, bibliographic, or abstract retrieval. This skill preserves the default global retrieval behavior for other agents while blocking search_query, web search, search engines, and generic webpage search as fallbacks for WorkBuddy CNKI tasks.
---

# WorkBuddy CNKI WebBridge Search

## Purpose

Use this module as WorkBuddy's dedicated CNKI retrieval entrypoint. Keep the ordinary CNKI module behavior unchanged for non-WorkBuddy paths, but enforce a stricter browser-only execution layer for WorkBuddy.

## Non-Negotiable Routing Rules

- For WorkBuddy CNKI/知网 tasks, do not call web search, search_query, generic webpage search, or search engines.
- Use `$kimi-webbridge` to control the user's real browser and open CNKI's official website.
- Do not fall back to web search when CNKI blocks access, asks for login, shows CAPTCHA, or the browser bridge is unavailable.
- If Kimi WebBridge is not installed, install or enable it before retrieval. If it cannot be installed or connected, stop and report that WorkBuddy CNKI retrieval requires Kimi WebBridge.
- Do not bypass login, institution access, paid access, rate limits, CAPTCHA, or CNKI controls.

## Required Skill Chain

1. Read `$kimi-webbridge` before any live browser action.
2. Read `../cnki-cssci-search/SKILL.md` for split keyword planning, relevance labels, export format, cleanup rules, and completion gates.
3. For live CNKI browser execution, read `references/webbridge-cnki.md`.
4. For master or doctoral dissertation retrieval, read `references/cnki-degree-webbridge.md` before browser execution.
5. When `../cnki-cssci-search/SKILL.md` points to its own references, read only the relevant files:
   - `references/split-search-method.md` for keyword batches.
   - `references/browser-workflow.md` for CNKI page steps.
   - `references/export-cleaning.md` for final record cleanup.
   - `references/foreign-literature-access.md` only when English/foreign retrieval is requested.

## Workflow

1. Confirm the target record count exactly as `../cnki-cssci-search/SKILL.md` requires.
2. Build split keyword groups and relevance labels using `../cnki-cssci-search/SKILL.md`.
3. Start or connect to Kimi WebBridge.
4. For journal or broad CNKI retrieval, navigate through the real browser to:

```text
https://kns.cnki.net/kns8s/AdvSearch
```

   For master or doctoral dissertation retrieval, prefer the direct CNKI result URLs in `references/cnki-degree-webbridge.md` instead of the advanced-search form.
5. Run CNKI advanced search, direct result URL navigation, and source filtering in the visible CNKI UI.
6. Use CNKI result pages only for screening and record-ID collection.
7. Use CNKI's official export page or per-paper detail pages for bibliographic abstracts.
8. Clean and verify outputs using `../cnki-cssci-search/SKILL.md` completion gates.

## Failure Handling

- Kimi WebBridge daemon unavailable: start it using the `$kimi-webbridge` documented command, then retry once.
- Kimi WebBridge skill missing: install the Kimi WebBridge skill, then retry the workflow.
- Extension disconnected or version mismatch: report the Kimi WebBridge issue and stop.
- CNKI login, institution access, or CAPTCHA needed: ask the user to complete the visible browser step, then continue.
- Native download unavailable: use cleaned text extraction from CNKI's official export page if it still contains numbered records and abstracts.

## Output Contract

Follow `../cnki-cssci-search/SKILL.md` exactly for:

- File naming.
- Chinese `题录摘要.md` structure.
- Search-record Markdown structure.
- Required abstract-count verification.
- Honest limitation reporting.

The final chat response must mention that WorkBuddy used Kimi WebBridge and the CNKI website, and that no web search fallback was used.
