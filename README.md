# thesis-workflow-cn

`thesis-workflow-cn` 是一个面向中文本科毕业论文流程的 Codex Skill 包。它把选题、文献检索、文献综述、开题报告和 Word 文档处理整合为一个入口 skill，并通过内部模块完成各阶段任务。

这个 skill 主要服务于中文论文写作场景，重点约束包括：阶段式交接、完成一个阶段后询问是否继续、参考文献只用检索到的记录、正文按最终提交的完成稿写，以及文献综述和开题报告阶段默认生成 Word 文档。

## 包含内容

- `thesis-workflow-cn`：公开入口 skill，负责识别论文任务阶段并调度内部模块。
- `undergraduate-thesis-topic`：本科论文选题、题目收窄、可行性评估和题目优化。
- `cnki-cssci-search`：知网、CSSCI、C 刊以及英文题名和摘要检索流程。
- `workbuddy-cnki-webbridge-search`：WorkBuddy 场景下通过 Kimi WebBridge 进行知网检索的专用流程。
- `literature-review-cn`：基于用户提供或实际检索到的文献记录和摘要撰写中文文献综述。
- `thesis-proposal-cn`：中文本科开题报告撰写。
- `thesis-outline-cn`：正文三级大纲和按节字数分配。
- `thesis-materials-cn`：读取项目代码、截图、数据，输出项目理解（待用户确认）和截图清单。
- `thesis-body-cn`：按"需求→设计→实现→测试"逐章推导写正文（Markdown），按最终提交的完成稿写，测试结果和数据写成完成状态。
- `thesis-figures-cn`：架构图、模块图、流程图、E-R 图、类图等用 Mermaid 生成，数据图用 matplotlib 生成，截图列清单交给用户。
- `thesis-qc-cn`：脚本检查字数、引用、图表编号、占位和模板化表达，再按格式审查、指导老师、盲审专家、事实核查四个角色审阅。
- `docx-editor-cn`：Word `.docx` 创建、模板填充、文档编辑，以及把整篇 Markdown 论文转成格式规范的 Word。

正文阶段的几个模块共用 `references/paper-types/` 里的论文类型模板。目前有九类：系统设计与实现、算法模型改进、工程设计、实证研究、实验研究、案例分析对策研究、法学研究、人文论述、设计创作策划方案。每类从约 50 篇 985、211 高校高被引学位论文中归纳章节结构和写法，并按本科篇幅换算。模板包括章节骨架和子类变体、字数分配、各章写作步骤、图表配置、摘要写法、句型框架和质量要点。

## 安装方式

推荐克隆本仓库，然后把 skill 目录链接到 Codex 的 skills 目录。

Windows PowerShell 示例：

```powershell
git clone https://github.com/XiaoJie4096/thesis-workflow-cn.git
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

Claude Code 用户把同一个目录链接到 `%USERPROFILE%\.claude\skills\thesis-workflow-cn` 即可。

### 正文阶段的依赖

| 用途 | 依赖 | 安装 |
|---|---|---|
| 整篇论文转 Word | Node.js 18+ | `cd skills/thesis-workflow-cn/modules/docx-editor-cn && npm install` |
| 结构图、流程图渲染 | Node.js 22+ + 本机 Chrome 或 Edge | 无需安装、无需联网，Mermaid 已内置在 `modules/thesis-figures-cn/vendor/mermaid/`（Node.js 较旧时自动改用 `npx` 下载 mermaid-cli） |
| 数据图 | Python 3.9+、matplotlib | `pip install matplotlib` |
| 质检、项目扫描 | Python 3.9+ | 只用标准库 |

没有 Chrome/Edge 时，可以把生成的 `.mmd` 文件内容粘贴到 https://mermaid.live 手动导出 PNG。

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
5. 正文大纲与字数分配（建议发给指导老师确认）
6. 素材整理与截图清单（读项目代码、截图、数据）
7. 分章写作（默认每写完一章停下来给用户看，也可以选一次写完）
8. 图表制作
9. 质检与模拟盲审
10. 整篇论文转 Word

每完成一个主要阶段后，skill 会先询问是否继续进入下一阶段，而不是默认一次性静默跑完整个流程。

正文阶段示例：

```text
开题已经过了，题目是"基于Unity3D的农场类游戏的设计与实现"，项目在 D:\Unity\FarmGame，
文献在上次检索的 题录摘要.md 里，学校要求正文 12000 字，帮我写论文正文
```

正文阶段的文件都放在一个论文项目文件夹里：

```text
论文/
├── plan/        大纲.md、字数分配.json、图表清单.md
├── materials/   项目清单.md、项目理解.md、截图清单.md
├── literature/  题录摘要.md
├── chapters/    00-摘要.md、01-绪论.md …… 90-参考文献.md、91-致谢.md
├── figures/     src/*.mmd、src/*.py、*.png
├── qc/          质检报告.md、审阅意见.md
└── output/      论文.docx
```

常用脚本（在 `skills/thesis-workflow-cn/` 下运行）：

```bash
python modules/thesis-materials-cn/scripts/project_inventory.py D:/Unity/FarmGame -o 论文/materials/项目清单.md
python modules/thesis-figures-cn/scripts/render_figures.py 论文/figures
python modules/thesis-qc-cn/scripts/thesis_qc.py 论文
node modules/docx-editor-cn/scripts/md2docx_thesis.js 论文/chapters -o 论文/output/论文.docx
```

生成的 Word 打开后，右键目录选"更新域"，再按学校模板检查版式；封面、诚信声明等页面从学校模板复制。

## 重要规则

- 参考文献必须来自用户提供或实际检索到的记录。
- 缺失的作者、年份、期刊、页码、DOI 等文献信息不能凭空补全。
- 用户没有项目代码时，按确认的大纲和需求设计系统，正文同样写成已完成开发和测试的状态，代码片段与设计保持一致。
- 正文按最终提交的完成稿写：测试结果、性能指标写成完成状态，数值和需求、设计前后一致。只有用户本人才知道的信息（姓名、学校信息）写成 `【待补充：…】`，截图保留图片引用，由用户之后补拍。
- 质检不能代替学校的查重和 AIGC 检测，skill 不预测检测结果。
- Word 文档的版式正确性只有在实际渲染或视觉检查完成后才能声称已经验证。
- 中文论文交付物默认使用中文表达，并保留用户已确认的题目、专业、研究对象、模板和格式要求。

## 仓库结构

```text
skills/
  thesis-workflow-cn/
    SKILL.md
    agents/
    references/
      paper-types/   论文类型模板
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
