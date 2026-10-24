---
name: thesis-materials-cn
description: Collect and verify the real materials a Chinese undergraduate thesis body depends on before drafting. Use when the user has source code, a Unity/Web/App project, screenshots, survey data, experiment results, interview notes, or design documents for their thesis, or when you need to know what is missing (素材缺口, 缺什么材料, 读我的项目, 项目理解) before writing 正文. Produces materials/项目理解.md and materials/素材缺口清单.md.
---

# Thesis Materials CN

## Core Positioning

The thesis describes the system the user actually built. This stage reads the user's project and materials, writes down what the project is in the user's own terms, and lists what each outline section will draw on. Drafting starts only after the user confirms the project summary.

## Inputs

- Confirmed `plan/大纲.md` from `modules/thesis-outline-cn` (if missing, run outline first or ask the user for the chapter list).
- Project path (source code folder, Unity project, design docs), screenshots folder, data files, and anything the user has said about the project.

## Workflow

1. Scan the project:

   ```bash
   python modules/thesis-materials-cn/scripts/project_inventory.py <项目路径> -o <论文项目>/materials/项目清单.md
   ```

   It reports languages and line counts, directory layout, key config files (Unity version, package.json, requirements, pom.xml, etc.), the largest source files, images, data files, and docs. It skips Library/Temp/node_modules/build output.

2. Read the key files the inventory points to: entry scripts, managers/controllers, data models, save/load code, configs, and existing README or design docs. For large projects, split reading by module and use subagents if the runtime allows; each subagent returns module name, responsibility, key classes/functions with file paths, data structures, and open questions.

3. Write `materials/项目理解.md` using the four information classes below, then show the user a short version and ask them to correct it. This confirmation is mandatory: the design and implementation chapters are built on it, so a misread module carries through the whole thesis.

4. Compare the confirmed outline against the evidence and write `materials/素材缺口清单.md` (Gap Report). Every section in the outline gets a status.

5. Tell the user which gaps block drafting (the project itself is unclear) and which screenshots they will capture later.

## Four Information Classes

Label every statement in 项目理解.md with one of these:

- `【原文】` read directly from code, data, or documents; include the file path.
- `【用户确认】` stated or confirmed by the user in this conversation.
- `【推断】` inferred by the agent from code structure; must be confirmed before it can be written into the thesis as fact.
- `【建议】` suggested extension or improvement; may appear in the thesis only as 展望 or design intent, never as implemented work.

## 项目理解.md Format

```markdown
# 项目理解（待用户确认）

## 1. 项目概况
- 项目类型：Unity 2022.3 3D 单机游戏【原文：ProjectSettings/ProjectVersion.txt】
- 核心玩法：种植—收获—出售—升级【用户确认】

## 2. 功能模块
| 模块 | 职责 | 关键文件 | 状态 | 信息类别 |
|---|---|---|---|---|
| 种植系统 | 翻地、播种、浇水、生长阶段切换 | Assets/Scripts/Farm/CropManager.cs | 已实现 | 原文 |

## 3. 数据与存储
## 4. 技术栈与开发环境
## 5. 已有素材（截图、数据、测试记录）
## 6. 需要用户确认的问题
1. ……
```

## 素材缺口清单.md Format

```markdown
# 素材缺口清单

| 大纲位置 | 需要的材料 | 现状 | 处理方式 | 阻塞写作 |
|---|---|---|---|---|
| 5.2 种植系统实现 | 种植过程运行截图 2 张 | 无 | 用户截图，先放占位 | 否 |
| 6.3 性能测试 | 帧率测试数据 | 无 | 按完成状态写出 | 否 |
| 2.1 Unity3D 引擎 | 相关文献 | 文献库已有 3 篇 | 直接引用 | 否 |
```

Status values: 已有 / 部分 / 无. Handling options: 直接使用, 用户补充, 先放占位, 按完成状态写出, 写进展望.

## Hard Rules

- A feature counts as implemented when the code or the user confirms it.
- Test results, performance numbers, and similar data the user has not provided are written in final form during drafting; record them in the gap list as 按完成状态写出.
- Screenshots are taken by the user. List exactly what each screenshot should show and its target filename under `figures/`.
- Do not copy large code blocks into the thesis plan; record file paths and function names.
- Do not send the user's source code to external services.

## Handoff

Pass to drafting: the confirmed 项目理解.md, the gap list, and the list of blocking gaps already resolved or explicitly accepted as placeholders.
