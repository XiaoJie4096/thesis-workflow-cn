#!/usr/bin/env python3
"""Render thesis figure sources to PNG.

Sources live in <figures>/src/:
  *.mmd  Mermaid diagrams  -> rendered offline with the bundled Mermaid and the installed Chrome/Edge
                              (mermaid_render.js); falls back to @mermaid-js/mermaid-cli via npx
  *.py   matplotlib charts -> executed with cwd=<figures>; each script saves <stem>.png itself

Outputs go to <figures>/<stem>.png. Up-to-date outputs are skipped unless --force is given.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MERMAID_CLI = "@mermaid-js/mermaid-cli@12.0.0"
OFFLINE_RENDERER = Path(__file__).with_name("mermaid_render.js")
BUNDLED_MERMAID = Path(__file__).resolve().parent.parent / "vendor" / "mermaid" / "mermaid.min.js"

BROWSER_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/microsoft-edge",
]

# Black-and-white academic look with Chinese-capable fonts
MERMAID_CONFIG = {
    "theme": "neutral",
    "themeVariables": {
        "fontFamily": "SimSun, 'Songti SC', 'Noto Serif CJK SC', 'Microsoft YaHei', sans-serif",
        "fontSize": "16px",
    },
    "flowchart": {"htmlLabels": True, "curve": "linear"},
}


def find_browser() -> str | None:
    env = os.environ.get("CHROME_PATH") or os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if env and Path(env).exists():
        return env
    for c in BROWSER_CANDIDATES:
        if Path(c).exists():
            return c
    return None


def outdated(src: Path, out: Path) -> bool:
    return not out.exists() or out.stat().st_mtime < src.stat().st_mtime


def render_mermaid(src: Path, out: Path, scale: int, tmp: Path, browser: str | None) -> tuple[bool, str]:
    cfg = tmp / "mermaid.json"
    cfg.write_text(json.dumps(MERMAID_CONFIG), encoding="utf-8")
    node = shutil.which("node")
    if node and browser and BUNDLED_MERMAID.exists():
        # Offline path: bundled mermaid.min.js + installed Chrome/Edge, no download
        cmd = [node, str(OFFLINE_RENDERER), str(src), str(out), "--browser", browser,
               "--scale", str(scale), "--config", str(cfg)]
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if proc.returncode == 0 and out.exists():
            return True, ""
        if proc.returncode != 3:   # 3 = Node.js too old for the offline renderer
            return False, (proc.stderr or proc.stdout).strip()[-800:]
    # Fallback: mermaid-cli through npx (downloads the package, and Chromium when no browser is installed)
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        return False, "Node.js not found; install Node.js, or paste the .mmd into https://mermaid.live"
    cmd = [npx, "-y", MERMAID_CLI, "-i", str(src), "-o", str(out), "-s", str(scale), "-b", "white", "-c", str(cfg)]
    env = os.environ.copy()
    if browser:
        pcfg = tmp / "puppeteer.json"
        pcfg.write_text(json.dumps({"executablePath": browser, "args": ["--no-sandbox"]}), encoding="utf-8")
        cmd += ["-p", str(pcfg)]
        env["PUPPETEER_SKIP_DOWNLOAD"] = "1"
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if proc.returncode != 0 or not out.exists():
        return False, (proc.stderr or proc.stdout).strip()[-800:]
    return True, ""


def render_python(src: Path, out: Path, figures_dir: Path) -> tuple[bool, str]:
    proc = subprocess.run([sys.executable, str(src)], cwd=figures_dir, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        return False, (proc.stderr or proc.stdout).strip()[-800:]
    if not out.exists():
        return False, f"script finished but {out.name} was not created (save to '{out.name}' in the figures folder)"
    return True, ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Mermaid and matplotlib figure sources to PNG.")
    parser.add_argument("figures", nargs="?", default="figures", help="Figures folder containing src/ (default: figures)")
    parser.add_argument("--force", action="store_true", help="Re-render even when the PNG is up to date")
    parser.add_argument("--scale", type=int, default=3, help="Mermaid scale factor (default 3, about 300 dpi when inserted at 15 cm)")
    parser.add_argument("--only", help="Render only sources whose file name contains this text")
    args = parser.parse_args()

    figures_dir = Path(args.figures).resolve()
    src_dir = figures_dir / "src"
    if not src_dir.is_dir():
        print(f"error=source folder not found: {src_dir}")
        return 1

    sources = sorted(p for p in src_dir.iterdir() if p.suffix.lower() in {".mmd", ".py"})
    if args.only:
        sources = [p for p in sources if args.only in p.name]
    browser = find_browser()
    if browser and BUNDLED_MERMAID.exists():
        print(f"mermaid=offline (bundled) browser={browser}")
    else:
        print(f"mermaid=npx {MERMAID_CLI} browser={browser or 'none (mermaid-cli will download Chromium)'}")

    ok, skipped, failed = [], [], []
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for src in sources:
            out = figures_dir / f"{src.stem}.png"
            if not args.force and not outdated(src, out):
                skipped.append(out.name)
                continue
            if src.suffix.lower() == ".mmd":
                success, err = render_mermaid(src, out, args.scale, tmp, browser)
            else:
                success, err = render_python(src, out, figures_dir)
            (ok if success else failed).append(out.name if success else (src.name, err))

    print(f"rendered={len(ok)} skipped={len(skipped)} failed={len(failed)}")
    for name in ok:
        print(f"  ok      {name}")
    for name, err in failed:
        print(f"  FAILED  {name}\n          {err}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
