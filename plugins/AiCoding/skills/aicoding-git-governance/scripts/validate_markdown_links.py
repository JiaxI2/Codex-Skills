#!/usr/bin/env python3
"""Validate local Markdown links, reference links, anchors, and placeholders."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

INLINE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REF_USE = re.compile(r"(?<!!)\[([^\]]+)\]\[([^\]]*)\]")
REF_DEF = re.compile(r"^\s*\[([^\]]+)\]:\s*(\S+)", re.MULTILINE)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER = re.compile(r"\{\{[^{}]+\}\}")
EXTERNAL = ("http://", "https://", "mailto:", "tel:", "data:")


def anchor(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = re.sub(r"[^\w\-\s\u4e00-\u9fff]", "", text)
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", text)).strip("-")


def anchors(markdown: str) -> set[str]:
    counts: dict[str, int] = {}
    found: set[str] = set()
    for _, title in HEADING.findall(markdown):
        base = anchor(title)
        index = counts.get(base, 0)
        found.add(base if index == 0 else f"{base}-{index}")
        counts[base] = index + 1
    return found


def clean(target: str) -> str:
    target = target.strip().strip("<>")
    target = re.split(r'\s+["\']', target, maxsplit=1)[0]
    return unquote(target)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    for item in PLACEHOLDER.findall(text):
        errors.append(f"{path}: unresolved placeholder {item}")

    definitions = {key.lower(): value for key, value in REF_DEF.findall(text)}
    targets = [clean(x) for x in INLINE.findall(text)]

    for label, key in REF_USE.findall(text):
        lookup = (key or label).lower()
        if lookup not in definitions:
            errors.append(f"{path}: missing reference [{lookup}]")
        else:
            targets.append(clean(definitions[lookup]))

    local_anchors = anchors(text)

    for target in targets:
        if not target or target.startswith(EXTERNAL) or "{{" in target:
            continue
        if target.startswith("#"):
            if target[1:] not in local_anchors:
                errors.append(f"{path}: missing anchor {target}")
            continue

        file_name, separator, target_anchor = target.partition("#")
        destination = (path.parent / file_name).resolve()
        if not destination.exists():
            errors.append(f"{path}: missing local target {target}")
            continue

        if separator and destination.suffix.lower() in {".md", ".markdown"}:
            other = destination.read_text(encoding="utf-8")
            if target_anchor not in anchors(other):
                errors.append(f"{path}: missing target anchor {target}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    for path in args.files:
        if not path.exists():
            errors.append(f"{path}: file does not exist")
        else:
            errors.extend(validate(path))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated {len(args.files)} Markdown file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
