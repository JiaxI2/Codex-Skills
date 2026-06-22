#!/usr/bin/env python3
"""Validate Release Notes headings against repository-governance.toml."""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER = re.compile(r"\{\{[^{}]+\}\}")


def heading_aliases(heading: str) -> set[str]:
    """Return canonical aliases for plain or bilingual headings."""
    parts = [item.strip() for item in re.split(r"\s+/\s+", heading) if item.strip()]
    return set(parts) or {heading.strip()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("release_notes", type=Path)
    args = parser.parse_args()

    with args.config.open("rb") as fh:
        config = tomllib.load(fh)

    text = args.release_notes.read_text(encoding="utf-8")
    headings = set()
    for item in HEADING.findall(text):
        headings.update(heading_aliases(item))
    release = config.get("release", {})
    required = list(release.get("required_sections", []))

    if release.get("require_explicit_deprecations", False):
        required.append("Deprecations")

    errors: list[str] = []
    for heading in dict.fromkeys(required):
        if heading not in headings:
            errors.append(f"missing required heading: {heading}")

    placeholders = PLACEHOLDER.findall(text)
    for item in placeholders:
        errors.append(f"unresolved placeholder: {item}")

    if "Full Changelog" in headings and "/compare/" not in text:
        errors.append("Full Changelog section has no compare URL")

    if errors:
        print("\n".join(errors))
        return 1

    print(f"Release Notes validated for profile: {release.get('profile', 'unknown')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
