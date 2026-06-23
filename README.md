# thesis-workflow-cn

`thesis-workflow-cn` is a Codex skill pack for Chinese undergraduate thesis workflows. It provides one public entry skill and several internal modules for topic selection, literature retrieval, literature review drafting, proposal drafting, and Word document handling.

The current package is designed for Chinese thesis-writing scenarios. It emphasizes stage-by-stage handoff, anti-fabrication rules for references, and Word deliverable generation for literature review and proposal stages.

## What It Includes

- `thesis-workflow-cn`: the public workflow entrypoint.
- `undergraduate-thesis-topic`: topic selection, narrowing, and feasibility evaluation.
- `cnki-cssci-search`: CNKI/CSSCI/C-journal and English title/abstract retrieval workflow.
- `workbuddy-cnki-webbridge-search`: WorkBuddy-only CNKI retrieval workflow through Kimi WebBridge.
- `literature-review-cn`: Chinese literature review drafting from provided records and abstracts.
- `thesis-proposal-cn`: Chinese undergraduate proposal drafting.
- `docx-editor-cn`: Word `.docx` creation and editing helpers.

## Install

Clone this repository, then link the skill directory into your Codex skills folder.

On Windows PowerShell:

```powershell
git clone https://github.com/<your-name>/thesis-workflow-cn.git
cmd /c mklink /J "%USERPROFILE%\.codex\skills\thesis-workflow-cn" "<repo-path>\skills\thesis-workflow-cn"
```

Restart Codex after linking the skill.

## Usage

Ask Codex for a Chinese undergraduate thesis workflow task, for example:

```text
帮我从本科论文选题开始，完成文献综述和开题报告
```

The entry skill should route the request through these default stages:

1. 选题确认
2. 文献材料准备
3. 文献综述写作并转 Word
4. 开题报告写作并转 Word

After each major stage, the skill asks whether to continue to the next stage instead of silently running the whole process.

## Important Rules

- References must come from user-provided or actually retrieved records.
- Missing bibliography fields must not be guessed.
- If a project has not been implemented, the thesis text must describe it as planned design, expected implementation, prototype, or system architecture work.
- Word layout correctness should only be claimed after actual render or visual verification.

## Repository Layout

```text
skills/
  thesis-workflow-cn/
    SKILL.md
    agents/
    references/
    modules/
```

## Third-Party Code

The bundled `docx-editor-cn` module includes its own MIT license file at:

```text
skills/thesis-workflow-cn/modules/docx-editor-cn/LICENSE.txt
```

Keep that notice when redistributing or modifying the repository.

## License

This repository is released under the MIT License. See `LICENSE` for details.
