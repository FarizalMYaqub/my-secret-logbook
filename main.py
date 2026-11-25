#!/usr/bin/env python3
"""Writes one secret-logbook line to the grader's output file."""

import os
import sys
from pathlib import Path

ENTRY_TEXT = (
    "Day 412: He said 'quick question' at 9:03. It is now Thursday. "
    "I have started a family in the thread. We are happy. Do not rescue us."
)

MAX_CHARS = 200
OUTPUT_NAME = "entry.txt"


def output_directory() -> Path:
    configured = os.environ.get("OUTPUT_DIR", "").strip()
    if configured:
        return Path(configured)
    return Path("/output")


def validate(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("entry text is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry text is {len(text)} chars, over {MAX_CHARS}")
    text.encode("utf-8")


def publish(directory: Path, text: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / OUTPUT_NAME
    staging = directory / (OUTPUT_NAME + ".staging")
    staging.write_text(text, encoding="utf-8", newline="")
    staging.replace(target)
    return target


def confirm(path: Path, expected: str) -> None:
    landed = path.read_text(encoding="utf-8")
    if landed != expected:
        raise RuntimeError("written entry does not match expected text")


def main() -> int:
    try:
        validate(ENTRY_TEXT)
    except ValueError as problem:
        print(f"refusing to write entry: {problem}", file=sys.stderr)
        return 1
    written = publish(output_directory(), ENTRY_TEXT)
    confirm(written, ENTRY_TEXT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
