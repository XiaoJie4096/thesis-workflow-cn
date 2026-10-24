"""Shared matplotlib style for Chinese thesis charts.

Copy this file into <figures>/src/ next to the chart scripts, then:

    from thesis_plot_style import apply_style, save
    apply_style()
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ...
    save(fig, __file__)   # writes <figures>/<script stem>.png at 300 dpi
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

CJK_FONTS = ["SimSun", "SimHei", "Microsoft YaHei", "Songti SC", "PingFang SC",
             "Noto Serif CJK SC", "Noto Sans CJK SC", "WenQuanYi Micro Hei"]

# Grayscale-friendly palette: still readable when the thesis is printed in black and white
PALETTE = ["#1f1f1f", "#6b6b6b", "#a8a8a8", "#3a6ea5", "#c0504d"]
HATCHES = ["", "//", "..", "xx", "\\\\"]


def apply_style() -> str:
    """Pick an installed Chinese font and set a clean print style. Returns the font name."""
    installed = {f.name for f in font_manager.fontManager.ttflist}
    font = next((f for f in CJK_FONTS if f in installed), None)
    if font is None:
        raise RuntimeError("No Chinese font found; install SimSun/SimHei or Noto CJK before plotting")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": [font, "Times New Roman", "DejaVu Sans"],
        "mathtext.fontset": "stix",
        "axes.unicode_minus": False,
        "font.size": 10.5,
        "axes.titlesize": 10.5,
        "axes.labelsize": 10.5,
        "legend.fontsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": plt.cycler(color=PALETTE),
        "axes.grid": True,
        "grid.linestyle": ":",
        "grid.alpha": 0.5,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "figure.dpi": 100,
    })
    return font


def save(fig, script_file: str) -> Path:
    """Save next to the figures folder (parent of src/) as <script stem>.png. No title inside the image:
    the caption is written in the Markdown image syntax and numbered by the Word converter."""
    script = Path(script_file).resolve()
    out = script.parent.parent / f"{script.stem}.png"
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out
