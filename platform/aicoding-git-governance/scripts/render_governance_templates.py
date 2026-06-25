#!/usr/bin/env python3
"""Render selected governance templates from repository-governance.toml."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tomllib
from pathlib import Path

FILES = {
    "readme": ("README_TEMPLATE.md", "readme.file", "README.md", "readme.enabled"),
    "changelog": ("CHANGELOG_TEMPLATE.md", "changelog.file", "CHANGELOG.md", "changelog.enabled"),
    "release-notes": ("RELEASE_NOTES_TEMPLATE.md", None, "RELEASE_NOTES.md", "release.enabled"),
}


def get_nested(data: dict, dotted: str | None, default=None):
    if not dotted:
        return default
    value = data
    for key in dotted.split("."):
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value


def bool_value(data: dict, dotted: str, default: bool) -> bool:
    value = get_nested(data, dotted, default)
    return bool(value)


def replace_known_values(text: str, config: dict) -> str:
    project = config.get("project", {})
    readme = config.get("readme", {})
    urls = readme.get("urls", {})
    replacements = {
        "PROJECT_NAME": project.get("name", ""),
        "REPOSITORY_URL": project.get("repository_url", ""),
        "DOCUMENTATION_URL": urls.get("documentation", ""),
        "CHANGELOG_URL": urls.get("changelog", "./CHANGELOG.md"),
        "LATEST_RELEASE_URL": urls.get("latest_release", ""),
        "RELEASES_URL": urls.get("releases", ""),
        "ISSUES_URL": urls.get("issues", ""),
        "CONTRIBUTING_URL": urls.get("contributing", "./CONTRIBUTING.md"),
        "SECURITY_URL": urls.get("security", "./SECURITY.md"),
        "LICENSE_URL": urls.get("license", "./LICENSE"),
    }
    for key, value in replacements.items():
        if value:
            text = text.replace("{{" + key + "}}", str(value))
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    parser.add_argument("--only", choices=sorted(FILES), action="append")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    with args.config.open("rb") as fh:
        config = tomllib.load(fh)

    assets = Path(__file__).resolve().parent.parent / "assets"
    selected = set(args.only or FILES.keys())
    created: list[Path] = []

    for key in selected:
        template_name, output_key, fallback, enabled_key = FILES[key]
        if not bool_value(config, enabled_key, True):
            continue

        output_name = get_nested(config, output_key, fallback) if output_key else fallback
        destination = args.output_dir / str(output_name)

        if destination.exists() and not args.force:
            print(f"skip existing: {destination}", file=sys.stderr)
            continue

        text = (assets / template_name).read_text(encoding="utf-8")
        text = replace_known_values(text, config)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
        created.append(destination)
        print(f"created: {destination}")

    if not created:
        print("No files created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
