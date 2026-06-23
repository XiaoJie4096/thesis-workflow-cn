# thesis-workflow-cn

`thesis-workflow-cn` 是一个面向中文本科毕业论文流程的 Codex Skill 包。它把选题、文献检索、文献综述、开题报告和 Word 文档处理整合为一个入口 skill，并通过内部模块完成各阶段任务。

这个 skill 主要服务于中文论文写作场景，重点约束包括：阶段式交接、完成一个阶段后询问是否继续、参考文献防虚构、基于真实材料写作，以及文献综述和开题报告阶段默认生成 Word 文档。

## 包含内容

- `thesis-workflow-cn`：公开入口 skill，负责识别论文任务阶段并调度内部模块。
- `undergraduate-thesis-topic`：本科论文选题、题目收窄、可行性评估和题目优化。
- `cnki-cssci-search`：知网、CSSCI、C 刊以及英文题名和摘要检索流程。
- `workbuddy-cnki-webbridge-search`：WorkBuddy 场景下通过 Kimi WebBridge 进行知网检索的专用流程。
- `literature-review-cn`：基于用户提供或实际检索到的文献记录和摘要撰写中文文献综述。
- `thesis-proposal-cn`：中文本科开题报告撰写。
- `docx-editor-cn`：Word `.docx` 创建、模板填充和文档编辑辅助模块。

## 安装方式

推荐克隆本仓库，然后把 skill 目录链接到 Codex 的 skills 目录。

Windows PowerShell 示例：

```powershell
git clone https://github.com/MMKLN0/thesis-workflow-cn.git
cmd /c mklink /J "%USERPROFILE%\.codex\skills\thesis-workflow-cn" "<repo-path>\skills\thesis-workflow-cn"
```

其中 `<repo-path>` 替换为你本地克隆后的仓库路径。链接完成后，重启 Codex 让 skill 生效。

如果无法访问 GitHub，也可以下载压缩包版本：

1. 解压 `thesis-workflow-cn.zip` 到任意本地目录。
2. 在 PowerShell 中执行：

```powershell
cmd /c mklink /J "%USERPROFILE%\.codex\skills\thesis-workflow-cn" "<解压目录>\skills\thesis-workflow-cn"
```

其中 `<解压目录>` 替换为压缩包解压后的目录。链接完成后，重启 Codex。

## 使用方式

可以直接向 Codex 提出中文本科论文流程任务，例如：

```text
帮我从本科论文选题开始，完成文献综述和开题报告
```

入口 skill 默认按以下阶段推进：

1. 选题确认
2. 文献材料准备
3. 文献综述写作并转 Word
4. 开题报告写作并转 Word

每完成一个主要阶段后，skill 会先询问是否继续进入下一阶段，而不是默认一次性静默跑完整个流程。

## 重要规则

- 参考文献必须来自用户提供或实际检索到的记录。
- 缺失的作者、年份、期刊、页码、DOI 等文献信息不能凭空补全。
- 如果项目尚未真实实现，论文内容必须写成拟设计、预期实现、原型或系统架构工作，不能假装已经完成开发、实验或测试。
- Word 文档的版式正确性只有在实际渲染或视觉检查完成后才能声称已经验证。
- 中文论文交付物默认使用中文表达，并保留用户已确认的题目、专业、研究对象、模板和格式要求。

## 仓库结构

```text
skills/
  thesis-workflow-cn/
    SKILL.md
    agents/
    references/
    modules/
```

核心入口在：

```text
skills/thesis-workflow-cn/SKILL.md
```

内部模块集中在：

```text
skills/thesis-workflow-cn/modules/
```

## 第三方代码

仓库内包含的 `docx-editor-cn` 模块带有独立 MIT 许可证文件：

```text
skills/thesis-workflow-cn/modules/docx-editor-cn/LICENSE.txt
```

重新分发或修改本仓库时，请保留该许可证声明。

## 许可证

本仓库使用 MIT License。详见 `LICENSE`。
