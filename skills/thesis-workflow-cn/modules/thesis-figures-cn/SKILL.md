---
name: thesis-figures-cn
description: Plan and produce figures and tables for a Chinese undergraduate thesis. Use when the user asks for 论文配图, 架构图, 功能模块图, 流程图, E-R图, 用例图, 类图, 时序图, 状态图, 数据图表, 柱状图/折线图, 三线表, 截图清单, or 图表编号. Generates diagrams as Mermaid source, data charts as Python matplotlib scripts, renders them to PNG, and lists screenshots the user must capture.
---

# Thesis Figures CN

## Core Positioning

Figures in an undergraduate thesis fall into three groups, each handled differently:

| Group | Examples | Who makes it | How |
|---|---|---|---|
| 结构图 / 流程图 | 架构图、功能模块图、流程图、E-R 图、用例图、类图、时序图、状态图 | Agent | Mermaid `.mmd` → PNG |
| 数据图 | 测试结果柱状图、折线图、饼图 | Agent, from the numbers in the chapters | Python `.py` (matplotlib) → PNG |
| 截图 | 运行界面、场景、编辑器配置 | User | Agent writes the capture list |

Tables are written directly in the chapter Markdown as three-line tables (see `../thesis-body-cn/references/markdown-conventions.md`).

## Workflow

1. Build `plan/图表清单.md` from the outline, the drafted chapters, and the 图表配置 table of the matching type template in `../../references/paper-types/`:

   ```markdown
   | 编号 | 图/表题 | 所在节 | 类型 | 文件 | 来源 | 状态 |
   |---|---|---|---|---|---|---|
   | 图4-1 | 系统总体架构图 | 4.1 | Mermaid | figures/architecture.png | 项目理解.md §2 | 待生成 |
   | 图5-2 | 种植系统运行界面 | 5.2 | 截图 | figures/farm-planting.png | 用户截图 | 待用户提供 |
   | 表6-1 | 功能测试用例表 | 6.2 | 表格 | — | 第3章需求编号 | 已写入正文 |
   ```

   Numbers are assigned automatically at Word build time; the list uses them only for planning.

2. Write diagram sources into `<论文项目>/figures/src/`. Use the patterns in `references/diagram-patterns.md`. Every node and relation must come from 项目理解.md or the outline; do not add modules that do not exist.

3. Write chart scripts into `figures/src/`, taking every number from the chapter text and tables so the chart and the text show the same values. Each script imports the shared style:

   ```python
   import sys; sys.path.insert(0, r"<skill>/modules/thesis-figures-cn/scripts")
   from thesis_plot_style import apply_style, save
   import matplotlib.pyplot as plt

   apply_style()
   fig, ax = plt.subplots(figsize=(6, 3.6))
   ax.bar(["场景A", "场景B"], [58, 61])   # same numbers as 表6-3
   ax.set_ylabel("平均帧率 / FPS")
   save(fig, __file__)                      # writes figures/<stem>.png
   ```

4. Render everything:

   ```bash
   python modules/thesis-figures-cn/scripts/render_figures.py <论文项目>/figures
   ```

   It renders `src/*.mmd` offline with the bundled Mermaid (`vendor/mermaid/`) in the installed Chrome or Edge, runs `src/*.py`, skips up-to-date outputs, and prints `rendered= skipped= failed=`. Use `--force` to re-render and `--only 名称` for one file.

5. Look at each rendered PNG (open the image) and fix overlapping labels, unreadable text, or too-wide layouts. Prefer `flowchart TB` for tall diagrams; split diagrams with more than ~15 nodes.

6. Write the screenshot list for the user (`materials/截图清单.md` or in chat): filename, what screen/state to show, suggested resolution, and which section uses it. Keep the placeholder image reference in the chapter so the Word file shows a yellow box until the file exists.

## Figure Rules

- The caption goes in the Markdown image alt text; no title inside the image itself.
- Chinese labels, 宋体/黑体, black and white or grayscale friendly; no decorative colors, shadows, or 3D effects.
- One figure, one message. Architecture and module diagrams show structure; flowcharts show one process.
- Every figure must be mentioned in the text before it appears ("如图4-1所示") and explained in one or two sentences after.
- Charts need axis labels with units, and their values match the chapter text.

## Requirements

- Mermaid: Node.js 22+ and Chrome or Edge installed; no network needed. Mermaid 12.2.0 is bundled in `vendor/mermaid/mermaid.min.js` and driven by `scripts/mermaid_render.js`. The browser is found automatically; set `CHROME_PATH` if detection fails. With an older Node.js or no browser, `render_figures.py` falls back to `@mermaid-js/mermaid-cli` through npx, which needs network on first run.
- Charts: Python with matplotlib and a Chinese font (SimHei / Microsoft YaHei / SimSun on Windows; Noto Sans CJK on Linux/macOS).
- If Mermaid cannot run, write the `.mmd` source anyway and tell the user to paste it into https://mermaid.live and export PNG, or redraw in draw.io / ProcessOn.

## References

- `references/diagram-patterns.md`: Mermaid templates for common thesis diagrams.
