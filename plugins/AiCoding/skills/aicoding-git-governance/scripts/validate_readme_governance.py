#!/usr/bin/env python3
"""Validate opt-in portable README governance profiles."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote


MARKDOWN_URL_RE = re.compile(r"\[[^\]]*\]\((https?://[^)]+)\)", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}|UNRESOLVED_PLACEHOLDER|TODO_PLACEHOLDER")
ALLOWED_BADGE_CATEGORIES = {"language", "toolchain", "first-party", "status"}


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, code: str, message: str) -> None:
        self.errors.append(f"{code}: {message}")

    def warn(self, code: str, message: str) -> None:
        self.warnings.append(f"{code}: {message}")


class Validator:
    def __init__(self, root: Path, config: dict, findings: Findings) -> None:
        self.root = root.resolve()
        self.config = config
        self.findings = findings
        self.readme = config.get("readme", {})
        self.adapter_cache: dict[tuple[str, str], dict] = {}
        names = [
            self.readme.get("file", "README.md"),
            self.readme.get("secondary_language_file", "README_CN.md"),
            self.readme.get("english_language_file", "README_EN.md"),
        ]
        self.readme_paths = list(dict.fromkeys(str(name) for name in names if name))
        self.readme_text: dict[str, str] = {}
        for name in self.readme_paths:
            path = self.repo_path(name, "README-GOV-001")
            if path is None or not path.is_file():
                self.findings.error("README-GOV-001", f"configured README file is missing: {name}")
                self.readme_text[name] = ""
            else:
                self.readme_text[name] = path.read_text(encoding="utf-8")

    @property
    def primary_text(self) -> str:
        primary = str(self.readme.get("file", "README.md"))
        return self.readme_text.get(primary, "")

    def repo_path(self, value: str, code: str) -> Path | None:
        if not value:
            self.findings.error(code, "a required repository-relative path is empty")
            return None
        path = (self.root / value).resolve()
        try:
            path.relative_to(self.root)
        except ValueError:
            self.findings.error(code, f"path escapes repository root: {value}")
            return None
        return path

    def section_body(self, semantic: str) -> str:
        marker = f"<!-- governance:section:{semantic} -->"
        start = self.primary_text.find(marker)
        if start < 0:
            return ""
        body_start = start + len(marker)
        next_start = self.primary_text.find("<!-- governance:section:", body_start)
        return self.primary_text[body_start : next_start if next_start >= 0 else None]

    def marker_body(self, start_marker: str, end_marker: str) -> str | None:
        start = self.primary_text.find(start_marker)
        end = self.primary_text.find(end_marker, start + len(start_marker))
        if start < 0 or end < 0:
            return None
        return self.primary_text[start + len(start_marker) : end]

    def run_adapter(self, value: str, contract: str, code: str) -> dict | None:
        cache_key = (value, contract)
        if cache_key in self.adapter_cache:
            return self.adapter_cache[cache_key]
        path = self.repo_path(value, code)
        if path is None or not path.is_file():
            self.findings.error(code, f"adapter does not exist: {value or '<empty>'}")
            return None
        if path.suffix.lower() == ".ps1":
            shell = shutil.which("pwsh") or shutil.which("powershell")
            if not shell:
                self.findings.error(code, "PowerShell is required to execute the configured adapter")
                return None
            command = [shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(path)]
        elif path.suffix.lower() == ".py":
            command = [sys.executable, str(path)]
        else:
            command = [str(path)]
        command.extend(["-Contract", contract, "-RepoRoot", str(self.root)])
        result = subprocess.run(command, cwd=self.root, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            self.findings.error(code, f"adapter failed for {contract}: {detail}")
            return None
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            self.findings.error(code, f"adapter returned invalid JSON for {contract}: {exc}")
            return None
        if not isinstance(payload, dict):
            self.findings.error(code, f"adapter result for {contract} must be a JSON object")
            return None
        self.adapter_cache[cache_key] = payload
        return payload

    def validate_structure(self) -> None:
        policy = self.readme.get("structure")
        if not isinstance(policy, dict):
            return
        profile = policy.get("profile", "legacy")
        if profile not in {"legacy", "30s-3min-persona"}:
            self.findings.error("README-GOV-010", f"unsupported readme.structure profile: {profile}")
            return
        if profile == "legacy":
            return
        required = self.readme.get("required_sections", [])
        if not isinstance(required, list):
            self.findings.error("README-GOV-011", "readme.required_sections must be an array")
            return
        for semantic in required:
            marker = f"<!-- governance:section:{semantic} -->"
            if marker not in self.primary_text:
                self.findings.error("README-GOV-012", f"missing semantic section marker: {semantic}")
        for semantic in ("value-proposition", "quick-start", "personas"):
            if semantic not in required:
                self.findings.error("README-GOV-013", f"30s-3min-persona requires semantic section: {semantic}")
        value_marker = "<!-- governance:section:value-proposition -->"
        first_heading = self.primary_text.find("\n## ")
        if self.primary_text.find(value_marker) > first_heading >= 0:
            self.findings.error("README-GOV-018", "value proposition must appear before the first level-two section")
        value_body = re.sub(r"<!--.*?-->", "", self.section_body("value-proposition"), flags=re.DOTALL).strip()
        if not value_body:
            self.findings.error("README-GOV-019", "value proposition must state one user outcome")
        quick_start = self.section_body("quick-start")
        steps = re.findall(r"(?m)^\s*\d+[.)]\s+", quick_start)
        if not steps:
            self.findings.error("README-GOV-014", "Quick Start must contain at least one copyable step")
        if len(steps) > 3:
            self.findings.error("README-GOV-014", f"Quick Start has {len(steps)} steps; maximum is 3")
        if "<!-- governance:quick-start:expected-result -->" not in quick_start:
            self.findings.error("README-GOV-015", "Quick Start must mark its expected result")
        if "<!-- governance:quick-start:doctor -->" not in quick_start:
            self.findings.error("README-GOV-016", "Quick Start must mark a doctor/troubleshooting entry")
        personas = self.section_body("personas")
        if not re.search(r"\[[^\]]+\]\((?:https://|\.?\.?/|#)[^)]+\)", personas):
            self.findings.error("README-GOV-017", "persona section must link to authoritative detail")

    def validate_banner(self) -> None:
        policy = self.readme.get("banner")
        if not isinstance(policy, dict) or not policy.get("enabled", False):
            return
        values = {key: str(policy.get(key, "")) for key in ("source_path", "light_path", "dark_path")}
        resolved: dict[str, Path] = {}
        for key, value in values.items():
            path = self.repo_path(value, "README-GOV-020")
            if path is None or not path.is_file():
                self.findings.error("README-GOV-020", f"enabled banner file is missing: {key}={value or '<empty>'}")
                continue
            resolved[key] = path
            if PLACEHOLDER_RE.search(path.read_text(encoding="utf-8")):
                self.findings.error("README-GOV-021", f"banner source/output has unresolved placeholder: {value}")
        for key in ("light_path", "dark_path"):
            if values[key] and not values[key].lower().endswith(".svg"):
                self.findings.error("README-GOV-022", f"banner output must be SVG: {values[key]}")
        if values["light_path"] == values["dark_path"] and values["light_path"]:
            self.findings.error("README-GOV-023", "light and dark banner outputs must be distinct")
        normalized = self.primary_text.replace("\\", "/")
        if f'{values["light_path"].replace(chr(92), "/")}#gh-light-mode-only' not in normalized:
            self.findings.error("README-GOV-024", "README must reference the light SVG with #gh-light-mode-only")
        if f'{values["dark_path"].replace(chr(92), "/")}#gh-dark-mode-only' not in normalized:
            self.findings.error("README-GOV-025", "README must reference the dark SVG with #gh-dark-mode-only")

    @staticmethod
    def badge_lines(text: str) -> list[str]:
        return [line.strip() for line in text.splitlines() if "img.shields.io" in line]

    def validate_badges(self) -> None:
        policy = self.readme.get("badges")
        if not isinstance(policy, dict):
            return
        mode = policy.get("policy", "minimal")
        if mode not in {"minimal", "tech-stack-projection", "off"}:
            self.findings.error("README-GOV-030", f"unsupported badge policy: {mode}")
            return
        color_policy = policy.get("color_policy", "classified")
        if color_policy != "classified":
            self.findings.error("README-GOV-039", f"unsupported badge color policy: {color_policy}")
        blocks = {name: self.badge_lines(text) for name, text in self.readme_text.items()}
        if len({tuple(lines) for lines in blocks.values()}) > 1:
            self.findings.error("README-GOV-031", "badge blocks differ across configured README files")
        for name, lines in blocks.items():
            for line in lines:
                urls = re.findall(r"https?://[^)\s]+", line, re.IGNORECASE)
                if any(url.lower().startswith("http://") for url in urls):
                    self.findings.error("README-GOV-032", f"badge URLs must use HTTPS: {name}")
        if mode != "tech-stack-projection":
            return
        if not policy.get("verify_versions", False):
            self.findings.error("README-GOV-033", "tech-stack-projection requires verify_versions = true")
            return
        payload = self.run_adapter(str(policy.get("source_adapter", "")), "badges", "README-GOV-033")
        if payload is None:
            return
        items = payload.get("badges")
        if not isinstance(items, list) or not items:
            self.findings.error("README-GOV-034", "badge adapter must return a non-empty badges array")
            return
        for item in items:
            if not isinstance(item, dict):
                self.findings.error("README-GOV-034", "each badge adapter item must be an object")
                continue
            name = str(item.get("name", ""))
            version = str(item.get("version", ""))
            source = str(item.get("source", ""))
            color = str(item.get("color", ""))
            category = str(item.get("category", ""))
            if not all((name, version, source, color)) or category not in ALLOWED_BADGE_CATEGORIES:
                self.findings.error("README-GOV-035", f"invalid badge adapter item: {item}")
                continue
            source_path = self.repo_path(source, "README-GOV-036")
            if source_path is None or not source_path.is_file():
                self.findings.error("README-GOV-036", f"badge version source is missing: {source}")
            elif version not in source_path.read_text(encoding="utf-8"):
                self.findings.error("README-GOV-037", f"badge version {version} is not present in {source}")
            for readme_name, lines in blocks.items():
                searchable = unquote("\n".join(lines)).lower()
                for expected in (name, version, color):
                    if expected.lower() not in searchable:
                        self.findings.error(
                            "README-GOV-038",
                            f"{readme_name} badge block does not project {name} {expected}",
                        )

    def validate_capabilities(self) -> None:
        policy = self.readme.get("capability_showcase")
        if not isinstance(policy, dict) or not policy.get("enabled", False):
            return
        if policy.get("max_lines_per_item") != 1 or not policy.get("require_detail_url", False):
            self.findings.error(
                "README-GOV-051",
                "enabled capability showcase requires max_lines_per_item = 1 and require_detail_url = true",
            )
        payload = self.run_adapter(
            str(policy.get("source_adapter", "")), "capabilities", "README-GOV-040"
        )
        if payload is None:
            return
        capabilities = payload.get("capabilities")
        if not isinstance(capabilities, list):
            self.findings.error("README-GOV-041", "capability adapter must return a capabilities array")
            return
        body = self.marker_body(
            "<!-- governance:capability-showcase:start -->",
            "<!-- governance:capability-showcase:end -->",
        )
        if body is None:
            self.findings.error("README-GOV-042", "capability showcase markers are missing")
            return
        content_lines = [line.strip() for line in body.splitlines() if line.strip()]
        if any(not line.startswith("- ") for line in content_lines):
            self.findings.error("README-GOV-043", "each capability must occupy exactly one Markdown list line")
        parsed: dict[str, str] = {}
        for line in content_lines:
            name_match = re.search(r"\*\*([^*]+)\*\*", line)
            urls = MARKDOWN_URL_RE.findall(line)
            if not name_match or len(urls) != 1:
                self.findings.error("README-GOV-044", f"capability line needs one bold name and one URL: {line}")
                continue
            if not urls[0].lower().startswith("https://"):
                self.findings.error("README-GOV-045", f"capability detail URL must use HTTPS: {line}")
            name = name_match.group(1)
            if name in parsed:
                self.findings.error("README-GOV-046", f"duplicate capability line: {name}")
            parsed[name] = urls[0]
        enabled: dict[str, str] = {}
        for item in capabilities:
            if not isinstance(item, dict) or not item.get("enabled", False):
                continue
            name = str(item.get("name", ""))
            detail_url = str(item.get("detailUrl", ""))
            if not name or not detail_url.lower().startswith("https://"):
                self.findings.error("README-GOV-047", f"invalid enabled capability adapter item: {item}")
                continue
            enabled[name] = detail_url
        for name, detail_url in enabled.items():
            if name not in parsed:
                self.findings.error("README-GOV-048", f"enabled capability is missing from showcase: {name}")
            elif parsed[name] != detail_url:
                self.findings.error("README-GOV-049", f"capability detail URL differs from adapter: {name}")
        for name in parsed:
            if name not in enabled:
                self.findings.error("README-GOV-050", f"ghost capability is present in showcase: {name}")

    @staticmethod
    def has_cycle(nodes: set[str], edges: list[tuple[str, str]]) -> bool:
        adjacency: dict[str, list[str]] = {node: [] for node in nodes}
        for source, target in edges:
            adjacency.setdefault(source, []).append(target)
        active: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> bool:
            if node in active:
                return True
            if node in visited:
                return False
            active.add(node)
            for target in adjacency.get(node, []):
                if visit(target):
                    return True
            active.remove(node)
            visited.add(node)
            return False

        return any(visit(node) for node in nodes if node not in visited)

    def validate_architecture_graph(self) -> None:
        policy = self.readme.get("architecture_graph")
        if not isinstance(policy, dict) or not policy.get("enabled", False):
            return
        blocks = re.findall(r"```mermaid\s*(.*?)```", self.primary_text, re.DOTALL | re.IGNORECASE)
        if not blocks:
            self.findings.error("README-GOV-060", "enabled architecture graph has no Mermaid block")
            return
        maximum = int(policy.get("max_nodes", 20))
        if maximum > 20 or maximum < 1:
            self.findings.error("README-GOV-061", "architecture_graph.max_nodes must be between 1 and 20")
            maximum = min(max(maximum, 1), 20)
        commands: set[str] = set()
        for block in blocks:
            nodes = set(re.findall(r"(?m)^\s*([A-Za-z][A-Za-z0-9_-]*)\s*(?:\[|\(|\{)", block))
            if len(nodes) > maximum:
                self.findings.error("README-GOV-062", f"Mermaid graph has {len(nodes)} nodes; maximum is {maximum}")
            if policy.get("require_layered_subgraphs", True) and not re.search(r"(?m)^\s*subgraph\b", block):
                self.findings.error("README-GOV-063", "Mermaid graph must use layered subgraph groups")
            edges = re.findall(
                r"(?m)^\s*([A-Za-z][A-Za-z0-9_-]*)\s*(?:-->|-\.->|==>)\s*([A-Za-z][A-Za-z0-9_-]*)",
                block,
            )
            if policy.get("require_feedback_edge", False) and not self.has_cycle(nodes, edges):
                self.findings.error("README-GOV-064", "loop graph must contain a real feedback edge")
            commands.update(match.strip() for match in re.findall(r"cmd:([^\"\]\r\n]+)", block))
        if commands:
            payload = self.run_adapter(
                str(policy.get("command_adapter", "")), "commands", "README-GOV-065"
            )
            if payload is None:
                return
            registered = payload.get("commands")
            if not isinstance(registered, list):
                self.findings.error("README-GOV-066", "command adapter must return a commands array")
                return
            for command in sorted(commands):
                if command not in registered:
                    self.findings.error("README-GOV-067", f"Mermaid references unknown command: {command}")

    def validate_evolution(self) -> None:
        policy = self.readme.get("evolution")
        if not isinstance(policy, dict):
            return
        mode = policy.get("quadrants_section", "recommended")
        if mode not in {"recommended", "required", "off"}:
            self.findings.error("README-GOV-070", f"unsupported quadrants_section: {mode}")
            return
        if mode == "off":
            return
        names = policy.get("content_files", [self.readme.get("file", "README.md")])
        if not isinstance(names, list):
            self.findings.error("README-GOV-071", "evolution.content_files must be an array")
            return
        content = "\n".join(
            path.read_text(encoding="utf-8")
            for name in names
            if (path := self.repo_path(str(name), "README-GOV-071")) is not None and path.is_file()
        )
        markers = [
            "<!-- governance:evolution-quadrants -->",
            "<!-- quadrant:known-known -->",
            "<!-- quadrant:known-unknown -->",
            "<!-- quadrant:unknown-known -->",
            "<!-- quadrant:unknown-unknown -->",
        ]
        missing = [marker for marker in markers if marker not in content]
        if missing and mode == "required":
            self.findings.error("README-GOV-072", f"required four-quadrant view is incomplete: {missing}")
        elif missing:
            self.findings.warn("README-GOV-073", f"recommended four-quadrant view is incomplete: {missing}")

    def validate_star_history(self) -> None:
        policy = self.readme.get("star_history")
        if not isinstance(policy, dict):
            return
        mode = policy.get("mode", "off")
        if mode not in {"page-link", "chart", "off"}:
            self.findings.error("README-GOV-080", f"unsupported star_history mode: {mode}")
            return
        configured_url = str(policy.get("url", ""))
        scanned = "\n".join(self.readme_text.values()) + "\n" + configured_url
        if re.search(r"(?i)[?&](?:sealed_token|token|credential|auth)=", scanned):
            self.findings.error("README-GOV-081", "Star History URL contains a forbidden credential parameter")
        if mode == "off":
            return
        if not configured_url.lower().startswith("https://"):
            self.findings.error("README-GOV-082", "Star History URL must use HTTPS")
        if configured_url not in self.primary_text:
            self.findings.error("README-GOV-083", "configured Star History URL is not present in README")
        if mode == "chart" and not policy.get("anonymous_endpoint_verified", False):
            self.findings.error("README-GOV-084", "chart mode requires anonymous_endpoint_verified = true")

    def validate(self) -> None:
        self.validate_structure()
        self.validate_banner()
        self.validate_badges()
        self.validate_capabilities()
        self.validate_architecture_graph()
        self.validate_evolution()
        self.validate_star_history()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()

    root = args.repo_root.resolve()
    config_path = args.config if args.config.is_absolute() else root / args.config
    with config_path.open("rb") as handle:
        config = tomllib.load(handle)

    findings = Findings()
    Validator(root, config, findings).validate()
    for warning in findings.warnings:
        print(warning, file=sys.stderr)
    for error in findings.errors:
        print(error, file=sys.stderr)
    if findings.errors:
        print(
            f"Portable README governance failed: errors={len(findings.errors)}, warnings={len(findings.warnings)}",
            file=sys.stderr,
        )
        return 1
    print(f"Portable README governance passed (warnings={len(findings.warnings)}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
