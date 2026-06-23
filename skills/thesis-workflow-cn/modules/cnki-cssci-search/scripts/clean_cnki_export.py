#!/usr/bin/env python3
"""Clean CNKI export-page text while preserving bibliographic records."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


JUNK_PATTERN = re.compile(r"\n?读者服务\n购买知网卡.*?\n安全验证", re.S)
RECORD_PATTERN = re.compile(r"^\[[0-9]+\]", re.M)
ABSTRACT_PATTERN = re.compile(r"^摘要[:：]", re.M)
LEFTOVER_PATTERNS = [
    "读者服务",
    "购买知网卡",
    "拖动下方拼图完成验证",
    "安全验证",
]


def clean_text(text: str) -> tuple[str, int]:
    cleaned, removed = JUNK_PATTERN.subn("", text)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip() + "\n"
    return cleaned, removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean CNKI export text and report record counts.")
    parser.add_argument("input", help="Input TXT file saved from a CNKI export page")
    parser.add_argument("-o", "--output", help="Output cleaned export file")
    parser.add_argument("--expected-count", type=int, help="Expected number of records")
    parser.add_argument("--allow-missing-abstracts", action="store_true", help="Do not fail when abstract count differs from record count")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_name(input_path.stem + "_cleaned" + input_path.suffix)

    text = input_path.read_text(encoding="utf-8")
    cleaned, removed = clean_text(text)
    output_path.write_text(cleaned, encoding="utf-8")

    count = len(RECORD_PATTERN.findall(cleaned))
    abstract_count = len(ABSTRACT_PATTERN.findall(cleaned))
    leftovers = [p for p in LEFTOVER_PATTERNS if p in cleaned]
    abstracts_ok = count == abstract_count

    print(f"output={output_path}")
    print(f"removed_blocks={removed}")
    print(f"record_count={count}")
    print(f"abstract_count={abstract_count}")
    print(f"abstracts_ok={abstracts_ok}")
    if args.expected_count is not None:
        print(f"expected_count={args.expected_count}")
        print(f"count_ok={count == args.expected_count}")
    print(f"leftovers={','.join(leftovers) if leftovers else 'none'}")

    failed = bool(leftovers)
    failed = failed or (args.expected_count is not None and count != args.expected_count)
    failed = failed or (not args.allow_missing_abstracts and not abstracts_ok)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
