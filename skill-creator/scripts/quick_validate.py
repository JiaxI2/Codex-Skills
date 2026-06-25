#!/usr/bin/env python3
"""
Validate a Codex/OpenCode-compatible Agent Skill.

The validator accepts either a skill directory or a direct path to SKILL.md. It
uses PyYAML when available, but falls back to a small frontmatter parser for
simple skill metadata so validation still works in minimal environments.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - exercised in minimal envs
    yaml = None


MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
ALLOWED_PROPERTIES = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}


def resolve_skill_md(path: Path) -> Path:
    if path.is_file():
        if path.name != "SKILL.md":
            raise ValueError("File path must point to SKILL.md")
        return path
    return path / "SKILL.md"


def parse_scalar(value: str):
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value in {"{}", "[]"}:
        return {} if value == "{}" else []
    return value


def parse_frontmatter(frontmatter_text: str):
    if yaml is not None:
        try:
            parsed = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML in frontmatter: {exc}") from exc
        if not isinstance(parsed, dict):
            raise ValueError("Frontmatter must be a YAML dictionary")
        return parsed

    parsed = {}
    current_map_key = None
    for raw_line in frontmatter_text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith((" ", "\t")):
            if current_map_key is not None:
                continue
            raise ValueError("Nested frontmatter requires PyYAML")
        if ":" not in raw_line:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")
        key, value = raw_line.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError("Frontmatter contains an empty key")
        if value.strip() == "":
            parsed[key] = {}
            current_map_key = key
        else:
            parsed[key] = parse_scalar(value)
            current_map_key = None
    return parsed


def validate_skill(skill_path):
    """Return (is_valid, message) for a skill directory or SKILL.md path."""
    try:
        skill_md = resolve_skill_md(Path(skill_path))
    except ValueError as exc:
        return False, str(exc)

    if not skill_md.exists():
        return False, "SKILL.md not found"

    try:
        content = skill_md.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return False, f"SKILL.md must be UTF-8 encoded: {exc}"

    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    try:
        frontmatter = parse_frontmatter(match.group(1))
    except ValueError as exc:
        return False, str(exc)

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        allowed = ", ".join(sorted(ALLOWED_PROPERTIES))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. Allowed properties are: {allowed}",
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if not name:
        return False, "Name cannot be empty"
    if not re.match(r"^[a-z0-9-]+$", name):
        return (
            False,
            f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
        )
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
    if len(name) > MAX_SKILL_NAME_LENGTH:
        return (
            False,
            f"Name is too long ({len(name)} characters). Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
        )

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if not description:
        return False, "Description cannot be empty"
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"
    if len(description) > MAX_DESCRIPTION_LENGTH:
        return (
            False,
            f"Description is too long ({len(description)} characters). Maximum is {MAX_DESCRIPTION_LENGTH} characters.",
        )

    compatibility = frontmatter.get("compatibility", "")
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > MAX_COMPATIBILITY_LENGTH:
            return (
                False,
                f"Compatibility is too long ({len(compatibility)} characters). Maximum is {MAX_COMPATIBILITY_LENGTH} characters.",
            )

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory_or_SKILL.md>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
