---
name: thesis-materials-cn
description: Read the user's project and materials before a Chinese undergraduate thesis body is drafted. Use when the user has source code, a Unity/Web/App project, screenshots, survey data, experiment results, interview notes, or design documents for their thesis, or asks 读我的项目, 项目理解, 截图清单 before writing 正文. Produces materials/项目理解.md and materials/截图清单.md.
---

# Thesis Materials CN

## Core Positioning

The thesis describes the system the user built. This stage reads the user's project and materials and writes down what the project is in the user's own terms. Drafting starts after the user confirms the project summary.

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

4. Write `materials/截图清单.md`: for each running-screen figure the outline plans, the target filename under `figures/`, the section that uses it, and exactly what screen and state it shows.

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
## 5. 已有截图与数据
## 6. 需要用户确认的问题
1. ……
```

## 截图清单.md Format

```markdown
# 截图清单

| 文件 | 所在节 | 画面内容 |
|---|---|---|
| figures/farm-planting.png | 5.2 种植系统实现 | 已播种的地块，三种作物处于不同生长阶段，界面显示背包 |
```

## Hard Rules

- A feature counts as implemented when the code or the user confirms it.
- Screenshots are taken by the user later; the chapters keep their image references.
- Do not copy large code blocks into the thesis plan; record file paths and function names.
- Do not send the user's source code to external services.

## Handoff

Pass to drafting: the confirmed 项目理解.md and 截图清单.md.
