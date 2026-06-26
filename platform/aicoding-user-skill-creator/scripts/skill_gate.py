#!/usr/bin/env python3
"""
Gate Agent Skill creation and workflow/standard-skill structure.

Model:
- Skill is the process manual.
- CLI is the checker.
- MCP is the tool library.
- Hook is the gate system.

Use `assess` before creating a new skill. Use `validate` as a hook/lint rule
after drafting a skill, especially for consistent workflow or standard skills.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


USE_SIGNALS = {
    "consistent-workflow": [
        "repeat",
        "repeated",
        "workflow",
        "process",
        "standard operating",
        "一致",
        "重复",
        "流程",
        "步骤",
        "固定做法",
    ],
    "organization-standard": [
        "company",
        "team standard",
        "policy",
        "compliance",
        "coding standard",
        "公司",
        "团队",
        "规范",
        "标准",
        "门禁",
    ],
    "reusable-domain-knowledge": [
        "domain",
        "reference",
        "schema",
        "protocol",
        "datasheet",
        "可复用",
        "领域知识",
        "协议",
        "资料",
        "参考",
    ],
    "team-expertise": [
        "expert",
        "senior",
        "tribal",
        "team knowledge",
        "best practice",
        "高级",
        "专家",
        "经验",
        "团队知识",
    ],
}

SKIP_SIGNALS = {
    "one-off-simple": [
        "one-off",
        "simple",
        "trivial",
        "一次性",
        "简单",
        "临时",
        "只要这次",
    ],
    "base-model-enough": [
        "basic",
        "general",
        "already handles",
        "基础",
        "通用",
        "模型已经",
        "不需要专门",
    ],
    "exploration-or-prototype": [
        "explore",
        "prototype",
        "brainstorm",
        "try",
        "探索",
        "原型",
        "试试",
        "头脑风暴",
    ],
}

REQUIRED_WORKFLOW_TERMS = {
    "trigger": ["trigger", "触发", "何时使用"],
    "inputs": ["input", "输入", "前置条件"],
    "steps": ["step", "步骤", "流程"],
    "exit_criteria": ["exit criteria", "done", "完成标准", "退出条件", "成功标准"],
    "validation": ["validate", "validation", "验证", "校验"],
    "blocking_hook": ["hook", "lint", "cli", "门禁", "阻塞"],
}

REQUIRED_GATE_TERMS = {
    "cli_checker": ["cli", "检查器", "checker", "lint", "脚本", "command", "命令"],
    "hook_gate": ["hook", "门禁", "pre-commit", "ci", "required check", "阻塞"],
    "mcp_tool_library": ["mcp", "工具库", "tool library", "available tools", "可用工具"],
    "human_confirmation": ["人工确认", "human confirmation", "确认人", "owner", "负责人"],
    "skip_rationale": ["暂不", "不需要", "skip", "原因", "rationale", "替代"],
}

TYPE_ALIASES = {
    "consistent-workflow": {"consistent-workflow", "workflow", "一致工作流程", "固定流程"},
    "organization-standard": {
        "organization-standard",
        "company-standard",
        "team-standard",
        "组织规范",
        "公司标准",
        "团队标准",
    },
    "reusable-domain-knowledge": {
        "reusable-domain-knowledge",
        "domain-knowledge",
        "可复用领域知识",
        "领域知识",
    },
    "team-expertise": {"team-expertise", "expertise", "团队知识", "专家经验", "高级专业知识"},
}


def find_signals(text: str, signal_map: dict[str, list[str]]) -> dict[str, list[str]]:
    lowered = text.lower()
    found = {}
    for name, terms in signal_map.items():
        hits = [term for term in terms if term.lower() in lowered]
        if hits:
            found[name] = hits
    return found


def assess_prompt(prompt: str) -> dict:
    use_hits = find_signals(prompt, USE_SIGNALS)
    skip_hits = find_signals(prompt, SKIP_SIGNALS)
    should_create = bool(use_hits) and not (skip_hits and not use_hits)
    if use_hits and skip_hits:
        should_create = len(use_hits) >= len(skip_hits)
    needs_gate_rules = bool({"consistent-workflow", "organization-standard"} & set(use_hits))
    return {
        "should_create_skill": should_create,
        "recommended_types": sorted(use_hits),
        "needs_gate_rules": needs_gate_rules,
        "requires_human_confirmation": needs_gate_rules,
        "use_signals": use_hits,
        "skip_signals": skip_hits,
        "decision": "create" if should_create else "skip",
    }


def read_prompt(args) -> str:
    parts = []
    if args.prompt:
        parts.append(args.prompt)
    if args.prompt_file:
        parts.append(Path(args.prompt_file).read_text(encoding="utf-8"))
    if not parts:
        parts.append(sys.stdin.read())
    return "\n".join(parts).strip()


def read_skill_md(path: Path) -> str:
    skill_md = path if path.is_file() else path / "SKILL.md"
    if not skill_md.exists():
        raise ValueError(f"SKILL.md not found: {skill_md}")
    return skill_md.read_text(encoding="utf-8")


def extract_skill_types(content: str) -> set[str]:
    types = set()
    match = re.search(r"^##\s+Skill Type\s*$([\s\S]*?)(?:^##\s+|\Z)", content, re.MULTILINE)
    if not match:
        match = re.search(r"^##\s+Skill 类型\s*$([\s\S]*?)(?:^##\s+|\Z)", content, re.MULTILINE)
    if not match:
        return types
    section = match.group(1).lower()
    for canonical, aliases in TYPE_ALIASES.items():
        if any(alias.lower() in section for alias in aliases):
            types.add(canonical)
    return types


def section_exists(content: str, names: list[str]) -> bool:
    for name in names:
        if re.search(rf"^##\s+{re.escape(name)}\s*$", content, re.MULTILINE):
            return True
    return False


def section_body(content: str, names: list[str]) -> str:
    names_pattern = "|".join(re.escape(name) for name in names)
    match = re.search(
        rf"^##\s+(?:{names_pattern})\s*$([\s\S]*?)(?:^##\s+|\Z)",
        content,
        re.MULTILINE,
    )
    return match.group(1).lower() if match else ""


def validate_workflow_contract(content: str) -> list[str]:
    errors = []
    if not section_exists(content, ["Workflow Contract", "工作流契约"]):
        errors.append("consistent-workflow skills must include ## Workflow Contract or ## 工作流契约")
        return errors
    contract = section_body(content, ["Workflow Contract", "工作流契约"])
    for key, terms in REQUIRED_WORKFLOW_TERMS.items():
        if not any(term.lower() in contract for term in terms):
            errors.append(f"workflow contract missing {key}: expected one of {', '.join(terms)}")
    return errors


def validate_gate_rules(content: str) -> list[str]:
    errors = []
    if not section_exists(content, ["Gate Rules", "门禁规则"]):
        errors.append("standard/workflow skills must include ## Gate Rules or ## 门禁规则")
        return errors
    gate = section_body(content, ["Gate Rules", "门禁规则"])
    for key, terms in REQUIRED_GATE_TERMS.items():
        if not any(term.lower() in gate for term in terms):
            errors.append(f"gate rules missing {key}: expected one of {', '.join(terms)}")
    return errors


def validate_human_confirmation(content: str) -> list[str]:
    errors = []
    if not section_exists(content, ["Human Confirmation", "人工反馈确认"]):
        errors.append("standard/workflow skills must include ## Human Confirmation or ## 人工反馈确认")
        return errors
    section = section_body(content, ["Human Confirmation", "人工反馈确认"])
    required = {
        "owner": ["owner", "负责人", "确认人"],
        "accepted_gates": ["gate", "hook", "ci", "门禁", "阻塞"],
        "manual_review": ["manual", "人工", "review", "审查"],
        "explicit_decision": ["approve", "批准", "确认", "reject", "拒绝"],
    }
    for key, terms in required.items():
        if not any(term.lower() in section for term in terms):
            errors.append(f"human confirmation missing {key}: expected one of {', '.join(terms)}")
    return errors


def validate_skill(path: Path) -> dict:
    content = read_skill_md(path)
    errors = []
    skill_types = extract_skill_types(content)
    if not skill_types:
        errors.append("SKILL.md must include ## Skill Type or ## Skill 类型 with at least one recognized type")
    if "consistent-workflow" in skill_types:
        errors.extend(validate_workflow_contract(content))
    if {"consistent-workflow", "organization-standard"} & skill_types:
        errors.extend(validate_gate_rules(content))
        errors.extend(validate_human_confirmation(content))
    return {
        "valid": not errors,
        "skill_types": sorted(skill_types),
        "errors": errors,
    }


def print_json(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate Agent Skill creation and workflow contracts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    assess_parser = subparsers.add_parser("assess", help="Decide whether a request should become a skill.")
    assess_parser.add_argument("--prompt", help="Request text to assess")
    assess_parser.add_argument("--prompt-file", help="UTF-8 file containing request text")
    assess_parser.add_argument("--json", action="store_true", help="Print JSON result")
    assess_parser.add_argument(
        "--skip-exit-zero",
        action="store_true",
        help="Return exit code 0 even when the decision is skip.",
    )

    validate_parser = subparsers.add_parser("validate", help="Validate skill type and gates.")
    validate_parser.add_argument("skill_path", help="Skill directory or SKILL.md path")
    validate_parser.add_argument("--json", action="store_true", help="Print JSON result")

    args = parser.parse_args()

    if args.command == "assess":
        result = assess_prompt(read_prompt(args))
        if args.json:
            print_json(result)
        else:
            print(f"decision: {result['decision']}")
            print(f"needs_gate_rules: {str(result['needs_gate_rules']).lower()}")
            print(f"requires_human_confirmation: {str(result['requires_human_confirmation']).lower()}")
            if result["recommended_types"]:
                print("recommended_types: " + ", ".join(result["recommended_types"]))
        if result["decision"] == "skip" and not args.skip_exit_zero:
            return 2
        return 0

    if args.command == "validate":
        try:
            result = validate_skill(Path(args.skill_path))
        except Exception as exc:
            result = {"valid": False, "skill_types": [], "errors": [str(exc)]}
        if args.json:
            print_json(result)
        else:
            print("Skill gate valid!" if result["valid"] else "Skill gate failed!")
            for error in result["errors"]:
                print(f"- {error}")
        return 0 if result["valid"] else 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
