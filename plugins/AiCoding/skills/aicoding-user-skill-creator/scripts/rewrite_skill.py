#!/usr/bin/env python3
"""
Copy a Claude/Anthropic-style skill and make a conservative Codex/OpenCode
compatibility pass over its SKILL.md.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

from quick_validate import validate_skill


PLATFORM_REPLACEMENTS = [
    ("Claude Code", "the current agent runtime"),
    ("Claude.ai", "the current agent runtime"),
    ("Claude", "the agent"),
    ("claude -p", "the runtime's non-interactive agent command, if available"),
    (".claude/commands", "the runtime's command or skill registration mechanism"),
    ("present_files", "the available file presentation mechanism"),
]


def normalize_skill_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        raise ValueError("Destination skill name must contain at least one letter or digit")
    if len(value) > 64:
        raise ValueError("Destination skill name is longer than 64 characters")
    return value


def split_frontmatter(content: str):
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md has no valid YAML frontmatter")
    return match.group(1), content[match.end() :]


def extract_description(frontmatter: str) -> str:
    match = re.search(r"^description:\s*(.*)$", frontmatter, re.MULTILINE)
    if not match:
        return "Migrated Agent Skill for Codex/OpenCode-compatible workflows."
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] in {"'", '"'} and value[-1] == value[0]:
        value = value[1:-1]
    return value


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{escaped}"'


def migrate_body(body: str) -> str:
    migrated = body
    for old, new in PLATFORM_REPLACEMENTS:
        migrated = migrated.replace(old, new)

    if "## Runtime Compatibility" not in migrated:
        section = (
            "## Runtime Compatibility\n\n"
            "This skill has been migrated for Codex/OpenCode-style Agent Skill usage. "
            "Runtime-specific features such as Claude-only CLI commands, slash commands, "
            "browser presentation helpers, or subagents should be treated as optional and "
            "used only when the current environment provides them.\n\n"
        )
        title_match = re.match(r"^(# .+?\r?\n+)", migrated)
        if title_match:
            migrated = migrated[: title_match.end()] + section + migrated[title_match.end() :]
        else:
            migrated = section + migrated
    return migrated


def migrate_skill(source: Path, destination: Path, force: bool) -> Path:
    if not source.exists() or not source.is_dir():
        raise ValueError(f"Source skill directory not found: {source}")
    if not (source / "SKILL.md").exists():
        raise ValueError(f"Source skill has no SKILL.md: {source}")

    skill_name = normalize_skill_name(destination.name)
    if destination.exists():
        if not force:
            raise ValueError(f"Destination already exists: {destination}")
        shutil.rmtree(destination)

    shutil.copytree(source, destination)

    skill_md = destination / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(content)
    old_description = extract_description(frontmatter)
    description = (
        f"Codex/OpenCode-compatible migration of {old_description}"
        if "Codex/OpenCode" not in old_description
        else old_description
    )
    if len(description) > 1024:
        description = description[:1021].rstrip() + "..."

    migrated = (
        "---\n"
        f"name: {skill_name}\n"
        f"description: {yaml_quote(description)}\n"
        "---\n\n"
        f"{migrate_body(body).lstrip()}"
    )
    skill_md.write_text(migrated, encoding="utf-8", newline="\n")

    valid, message = validate_skill(destination)
    if not valid:
        raise ValueError(f"Migrated skill failed validation: {message}")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate a Claude/Anthropic-style skill folder for Codex/OpenCode usage."
    )
    parser.add_argument("source", help="Source skill directory")
    parser.add_argument("destination", help="Destination skill directory")
    parser.add_argument("--force", action="store_true", help="Replace destination if it exists")
    args = parser.parse_args()

    try:
        output = migrate_skill(Path(args.source), Path(args.destination), args.force)
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1

    print(f"[OK] Migrated skill to {output}")
    print("[OK] Validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
