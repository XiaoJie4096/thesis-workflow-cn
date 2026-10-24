#!/usr/bin/env python3
"""Inventory a student's graduation-project folder so the agent reads the right files first.

Skips generated/vendor folders (node_modules, Unity Library/Temp, build output, .git ...),
counts source files and lines by language, lists images, data files, documents, and
likely entry points or config files. Writes a Markdown inventory.

Usage:
  python project_inventory.py <project-folder> [-o materials/项目清单.md] [--max-list 80]
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

SKIP_DIRS = {
    ".git", ".svn", ".hg", ".idea", ".vscode", ".vs", "__pycache__", ".pytest_cache", ".mypy_cache",
    "node_modules", "bower_components", "vendor", "venv", ".venv", "env", "dist", "build", "out", "target",
    "bin", "obj", ".gradle", ".next", ".nuxt", "coverage",
    # Unity / Unreal / Godot generated folders
    "Library", "Temp", "Logs", "UserSettings", "MemoryCaptures", "Builds", "Intermediate", "Saved",
    "DerivedDataCache", "Binaries", ".godot", ".import",
}

LANG = {
    ".py": "Python", ".java": "Java", ".kt": "Kotlin", ".cs": "C#", ".cpp": "C++", ".cc": "C++", ".c": "C",
    ".h": "C/C++ Header", ".hpp": "C/C++ Header", ".go": "Go", ".rs": "Rust", ".js": "JavaScript",
    ".jsx": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript", ".vue": "Vue", ".php": "PHP",
    ".rb": "Ruby", ".swift": "Swift", ".m": "MATLAB/Obj-C", ".r": "R", ".sql": "SQL", ".html": "HTML",
    ".css": "CSS", ".scss": "SCSS", ".less": "LESS", ".wxml": "WXML", ".wxss": "WXSS", ".dart": "Dart",
    ".gd": "GDScript", ".lua": "Lua", ".shader": "Shader", ".hlsl": "Shader", ".glsl": "Shader",
    ".ipynb": "Jupyter",
}
IMAGES = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg"}
DATA = {".csv", ".xlsx", ".xls", ".json", ".sav", ".dta", ".parquet", ".db", ".sqlite", ".mat", ".txt"}
DOCS = {".md", ".docx", ".doc", ".pdf", ".pptx", ".ppt"}
KEY_NAMES = {
    "readme.md", "package.json", "pom.xml", "build.gradle", "requirements.txt", "pyproject.toml",
    "setup.py", "manage.py", "app.py", "main.py", "application.yml", "application.properties",
    "docker-compose.yml", "dockerfile", "app.json", "project.config.json", "vite.config.ts",
    "vite.config.js", "cargo.toml", "go.mod", "projectversion.txt", "manifest.json", "projectsettings.asset",
    "editorbuildsettings.asset",
}
UNITY_ASSET_DIRS = {"Scripts", "Scenes", "Prefabs", "Resources", "UI", "Animations"}


def walk(root: Path):
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            entries = list(d.iterdir())
        except (PermissionError, OSError):
            continue
        for e in entries:
            if e.is_dir():
                if e.name not in SKIP_DIRS and not e.name.startswith("."):
                    stack.append(e)
            elif e.is_file():
                yield e


def line_count(p: Path) -> int:
    try:
        with p.open("rb") as fh:
            return sum(1 for _ in fh)
    except OSError:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory a graduation-project folder.")
    parser.add_argument("project", help="Project folder to scan")
    parser.add_argument("-o", "--output", default="materials/项目清单.md", help="Output Markdown path")
    parser.add_argument("--max-list", type=int, default=80, help="Max files listed per category")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    if not root.is_dir():
        print(f"error=not a folder: {root}")
        return 1

    lang_files: Counter[str] = Counter()
    lang_lines: Counter[str] = Counter()
    by_dir: dict[str, Counter[str]] = defaultdict(Counter)
    sources: list[tuple[int, Path]] = []
    images: list[Path] = []
    data: list[Path] = []
    docs: list[Path] = []
    keys: list[Path] = []
    unity = (root / "Assets").is_dir() and (root / "ProjectSettings").is_dir()

    for f in walk(root):
        rel = f.relative_to(root)
        ext = f.suffix.lower()
        if ext in LANG:
            n = line_count(f)
            lang_files[LANG[ext]] += 1
            lang_lines[LANG[ext]] += n
            top = rel.parts[0] if len(rel.parts) > 1 else "."
            by_dir[top][LANG[ext]] += 1
            sources.append((n, rel))
        elif ext in IMAGES:
            images.append(rel)
        if f.name.lower() in KEY_NAMES:
            keys.append(rel)
            continue
        if ext in IMAGES:
            images.append(rel)
        elif ext in DATA and f.stat().st_size > 0:
            data.append(rel)
        elif ext in DOCS:
            docs.append(rel)

    out: list[str] = [f"# 项目清单：{root.name}", "", f"扫描路径：`{root}`", ""]
    if unity:
        version = root / "ProjectSettings" / "ProjectVersion.txt"
        v = version.read_text(encoding="utf-8", errors="ignore").splitlines()[0] if version.exists() else "未知"
        out += [f"项目类型判断：Unity 工程（{v}）。重点阅读 `Assets/` 下的脚本、场景和预制体。", ""]
        sub = sorted(p.name for p in (root / "Assets").iterdir() if p.is_dir())
        out += ["Assets 子目录：" + "、".join(sub) if sub else "Assets 下无子目录", ""]
        missing = sorted(UNITY_ASSET_DIRS - set(sub))
        if missing:
            out += [f"常见目录未找到：{'、'.join(missing)}（脚本可能放在其他位置）", ""]

    out += ["## 代码规模", "", "| 语言 | 文件数 | 行数 |", "|---|---:|---:|"]
    for lang, n in lang_files.most_common():
        out.append(f"| {lang} | {n} | {lang_lines[lang]} |")
    out.append(f"| **合计** | **{sum(lang_files.values())}** | **{sum(lang_lines.values())}** |")
    out += ["", "行数为物理行数（含空行和注释），只用于判断规模，不要直接写进论文当作“代码量”。", ""]

    out += ["## 目录分布", ""]
    for d, c in sorted(by_dir.items(), key=lambda kv: -sum(kv[1].values())):
        out.append(f"- `{d}/`：" + "，".join(f"{k} {v}" for k, v in c.most_common()))
    out.append("")

    def listing(title: str, items: list, fmt) -> None:
        out.extend([f"## {title}（{len(items)}）", ""])
        if not items:
            out.append("- 无")
        for it in items[: args.max_list]:
            out.append(fmt(it))
        if len(items) > args.max_list:
            out.append(f"- …… 另有 {len(items) - args.max_list} 个")
        out.append("")

    listing("关键配置与入口文件", sorted(keys), lambda p: f"- `{p.as_posix()}`")
    listing("最大的源代码文件（优先阅读）", sorted(sources, reverse=True),
            lambda t: f"- `{t[1].as_posix()}`（{t[0]} 行）")
    listing("图片（可能可作论文截图）", sorted(images), lambda p: f"- `{p.as_posix()}`")
    listing("数据文件", sorted(data), lambda p: f"- `{p.as_posix()}`")
    listing("文档", sorted(docs), lambda p: f"- `{p.as_posix()}`")

    dest = Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"output={dest.resolve()}")
    print(f"unity={unity} source_files={sum(lang_files.values())} source_lines={sum(lang_lines.values())} "
          f"images={len(images)} data_files={len(data)} docs={len(docs)}")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
