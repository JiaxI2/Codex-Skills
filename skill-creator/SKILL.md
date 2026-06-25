---
name: skill-creator
description: Create, improve, validate, or migrate Agent Skills for Codex/OpenCode while preserving compatibility with Anthropic-style SKILL.md folders. Use when the user asks to decide whether a skill should be created, classify skill type, enforce workflow-skill contracts with CLI/Hook/Lint gates, build or update a skill, convert Claude/Anthropic skills, add skill tests, improve triggering descriptions, or check portability across agent runtimes.
---

# Agent Skill Creator

Use this skill to create new Agent Skills or migrate existing Claude/Anthropic-style skills so they work cleanly in Codex and OpenCode. Keep the workflow practical: understand the intended behavior, edit only the skill files that matter, validate the result, and forward-test when the risk justifies it.

## Runtime Compatibility

This skill is adapted for Codex/OpenCode usage.

- Do not assume `claude -p`, `.claude/commands`, `present_files`, or Claude-only slash commands exist.
- Use Codex tools, local scripts, and available subagents when present; fall back to inline validation when they are not.
- Treat the bundled eval and benchmark assets as legacy/optional helpers unless the current runtime has the tools they require.
- Prefer static files or conversation summaries over browser-only review flows in headless environments.
- Use UTF-8 when reading or writing `SKILL.md`; Windows default encodings can otherwise break validation.

## Skill Type

This skill is both `consistent-workflow` and `organization-standard`: it decides when to create skills, classifies the skill being created, and enforces a repeatable creation/validation workflow.

Supported skill types:

1. `consistent-workflow`: repeated tasks that must follow the same ordered process.
2. `organization-standard`: company/team-specific procedures, standards, or policies.
3. `reusable-domain-knowledge`: deep domain knowledge encoded as reusable references, scripts, schemas, or assets.
4. `team-expertise`: senior professional knowledge preserved as team-operational guidance.

Skip creating a skill when the task is one-time and simple, the base model can already handle it reliably, or the user is only exploring/prototyping and the workflow is not stable yet.

## Skill/CLI/MCP/Hook Model

创建标准或流程类 skill 时，按以下职责拆分，不要把所有责任都塞进 `SKILL.md`：

- **Skill 是流程说明书**：写清何时触发、输入、步骤、完成标准、人工判断点和例外。
- **CLI 是检查器**：把可稳定判断的规则做成可本地运行的命令，失败用非零退出码和可读错误信息表达。
- **MCP 是工具库**：把需要长期复用的外部能力、项目诊断、查询或自动化能力封装为可调用工具；没有 MCP 时写清替代 CLI 或人工路径。
- **Hook 是门禁系统**：把 CLI 或测试接入 pre-commit、Git hook、CI required check、发布脚本或产线包生成流程，明确在哪个阶段阻塞。

对 `consistent-workflow` 或 `organization-standard` skill，必须判断是否需要 CLI/Hook/Lint/CI/MCP。若规则可机器检查，必须补 `Gate Rules`；若暂不实现，必须写明原因、人工替代项和确认人。

## Skill Creation Gate

Before creating a new skill, run a creation gate mentally or with the CLI:

```bash
python scripts/skill_gate.py assess --prompt "<user request>"
python scripts/skill_gate.py assess --prompt-file request.txt --json
```

Create or update a skill only when at least one use signal is present:

- consistent repeated workflow;
- company/team-specific process or standard;
- reusable deep domain knowledge;
- advanced professional knowledge that should become team knowledge.

Block or defer skill creation when skip signals dominate:

- one-time and simple task;
- base model can handle it without specialized instructions or resources;
- exploration/prototype phase before the workflow stabilizes.

If the gate returns `skip`, explain why a normal answer or temporary note is enough. If the user still explicitly requests a skill, proceed but record the tradeoff in the skill body.

When the gate recommends `consistent-workflow` or `organization-standard`, require both gate-rule design and human confirmation before calling the skill complete.

## Workflow Contract

Trigger: use this workflow when creating, updating, migrating, or validating a skill.

Inputs: user request, existing skill path when present, target runtime, expected reuse pattern, and any project/company standard that must be preserved.

Steps:

1. Run the creation gate and classify the skill type.
2. For `consistent-workflow`, define the required ordered steps before writing detailed instructions.
3. Decide whether resources belong in `scripts/`, `references/`, or `assets/`.
4. Edit only the files needed for the skill behavior.
5. Validate frontmatter and skill type with `quick_validate.py` and `skill_gate.py validate`.
6. Forward-test when the skill controls a real workflow or deliverable.

Exit Criteria: the skill has a clear trigger description, a recognized skill type, required resources are present, workflow skills have an explicit contract, and validation commands pass.

Validation: run `python scripts/quick_validate.py path/to/skill` and `python scripts/skill_gate.py validate path/to/skill`.

Blocking Hook: use `skill_gate.py validate` in pre-commit, CI, or local review scripts so missing skill type, gate rules, human confirmation, or incomplete workflow contract returns a non-zero exit code.

## Gate Rules

For standard/process skills, document these checks before declaring the skill ready:

- CLI checker: command name, input files, pass/fail condition, non-zero exit behavior, and example failure message.
- Hook gate: whether the CLI is wired to pre-commit, Git hook, CI required check, release packaging, or production-package generation.
- MCP tool library: MCP tools required by the workflow, or the explicit reason no MCP is needed and which CLI/manual path replaces it.
- Human confirmation: who confirms the gates are acceptable before the skill is considered complete.
- Skip rationale: if any gate is not implemented, record why it is not stable enough for automation and what manual review replaces it.

A `consistent-workflow` or `organization-standard` skill without `Gate Rules` is incomplete unless the user explicitly accepts the documented skip rationale.

## Human Confirmation

Before finalizing a standard/process skill, capture human feedback in the skill or final report:

- Owner/确认人: the user, team owner, or named reviewer who accepts the workflow.
- Accepted gates: CLI, Hook, CI, MCP, manual review, or documented skip decision.
- Manual review scope: what remains human-only and why it cannot be reliably linted yet.
- Explicit decision: approved, approved with risk, or rejected for another iteration.

If the user has not confirmed these items, ask for confirmation or mark the skill as draft/incomplete.

## Core Workflow

1. Clarify the skill goal with concrete examples.
2. Decide whether the skill needs only instructions or also bundled `scripts/`, `references/`, or `assets/`.
3. Create or edit the skill with the smallest useful change.
4. Validate the skill structure with `scripts/quick_validate.py`.
5. Forward-test realistic prompts when behavior is complex, fragile, or user-facing.
6. Iterate from observed failures, not speculative features.

## Creating a New Skill

Ask where the user wants the skill created. If they do not specify, choose the active Codex user skill location for this machine, or a repo-local skill directory when the skill is project-specific.

Use the initializer instead of hand-assembling the folder:

```bash
python scripts/init_skill.py my-new-skill --path ~/.codex/skills
python scripts/init_skill.py my-new-skill --path .agents/skills --resources scripts,references
```

Then edit the generated `SKILL.md`:

- Keep frontmatter to `name` and `description` unless the local runtime explicitly supports more.
- Put trigger guidance in `description`, because it is visible before the body is loaded.
- Keep the body focused on procedures and non-obvious domain knowledge.
- Add scripts only when deterministic behavior or repeated code is worth the maintenance cost.
- Split long reference material into `references/` and point to it from `SKILL.md`.

If `agents/openai.yaml` needs to be regenerated, use:

```bash
python scripts/generate_openai_yaml.py path/to/skill --interface display_name="Display Name" --interface short_description="Short UI description"
```

## Migrating an Existing Claude/Anthropic Skill

Use `rewrite_skill.py` for the first mechanical pass:

```bash
python scripts/rewrite_skill.py path/to/old-skill path/to/new-skill-codex
python scripts/quick_validate.py path/to/new-skill-codex
```

After the script runs, review the migrated `SKILL.md` manually. Mechanical cleanup cannot fully understand intent.

Focus the review on:

- Removing hard requirements for Claude-only mechanisms such as `claude -p`, `.claude/commands`, `present_files`, and Claude slash commands.
- Replacing Claude-specific language with runtime-neutral language such as "agent", "Codex", "available tools", or "subagents if available".
- Adding or checking a `Runtime Compatibility` section that states what changed and what remains optional.
- Preserving useful bundled resources instead of deleting them just because they came from a Claude skill.
- Updating `description` so Codex triggers the skill for the migrated workflow rather than only for Anthropic-specific prompts.

## Improving an Existing Skill

Before editing, inspect the current skill folder and identify the smallest change that addresses the observed problem.

Use this sequence:

1. Read `SKILL.md` and only the directly relevant bundled files.
2. State the success criteria in concrete terms, such as "validator passes" or "forward test creates the expected file".
3. Edit the resource or instruction that directly controls the behavior.
4. Remove only code or instructions made obsolete by the current edit.
5. Run validation and a focused smoke test.

For triggering issues, update the frontmatter `description` first. It should say what the skill does and when to use it, while staying concise enough to survive truncation in large skill sets.

## Validation

Run the validator after every structural change:

```bash
python scripts/quick_validate.py path/to/skill
python scripts/quick_validate.py path/to/skill/SKILL.md
```

The validator checks:

- `SKILL.md` exists or the supplied path points to one.
- Frontmatter is present and parseable.
- `name` and `description` exist and are strings.
- `name` is lowercase hyphen-case and no longer than 64 characters.
- `description` avoids angle brackets and stays within the supported length.
- Only compatible top-level frontmatter keys are used.

The validator is designed to work even when `PyYAML` is unavailable. When `PyYAML` is installed, it uses it for stricter parsing.

## Forward Testing

Forward-test when the skill is complex, modifies files, creates deliverables, or changes behavior that users rely on.

Good forward tests look like real user requests. They should not reveal your diagnosis, expected answer, or hidden implementation notes. If subagents are available, give each one only the skill path, the task, and any input artifacts. If subagents are unavailable, run the same prompt yourself in a fresh, minimal context.

Useful checks include:

- The intended skill would trigger from the prompt.
- The instructions lead to the expected workflow without extra user hand-holding.
- Bundled scripts run successfully in the target environment.
- Outputs are inspectable and match the user-visible success criteria.

## Legacy Evaluation Assets

This folder may include Anthropic-origin evaluation helpers such as `eval-viewer/`, benchmark aggregation scripts, and description optimization scripts. Use them only when their runtime assumptions are true.

- If a script shells out to `claude -p`, do not use it in Codex unless the user explicitly has Claude CLI available and wants that path.
- If a review viewer requires a browser server but the environment is headless, generate a static artifact or summarize results inline.
- Prefer Codex-native forward testing for day-to-day skill changes.

## Packaging

Package only after validation passes and the user wants a distributable artifact:

```bash
python scripts/package_skill.py path/to/skill
```

If packaging an installed user-level skill, copy it to a writable staging location first, package the staged copy, and then copy the final artifact to the requested output location.
