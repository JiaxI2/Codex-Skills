---
name: aicoding-tdd-fallback
description: Provide a self-contained AiCoding TDD loop when Superpowers or another external test-driven-development skill is not available.
---

# AiCoding TDD Fallback
## Skill Type

This skill is both consistent-workflow and organization-standard.

- consistent-workflow: it defines an ordered AiCoding engineering workflow that agents must follow for repeatable delivery.
- organization-standard: it encodes AiCoding project policy for standalone-capable SDD, MVP, BDD, architecture-first, TDD fallback, verification, and documentation synchronization.

## Workflow Contract

Trigger: use this skill when the described AiCoding workflow phase is relevant to a non-trivial software, firmware, tooling, automation, architecture, test, documentation, install, release, or maintenance change.

Inputs: user request, repository AGENTS instructions, existing SDD/BDD/architecture/test/docs artifacts when present, current code and git state, and any applicable project verification commands.

Steps: read the local repository rules, identify the current workflow phase, produce or update only the artifacts required by that phase, keep Superpowers optional, run the repository's validation commands, and hand off to the next AiCoding workflow phase only when the phase output is inspectable.

Exit criteria: the phase has a concrete done state, required artifacts exist or are explicitly marked not applicable, tests or validation commands have been run where available, and documentation impact has been reviewed.

Validation: use repository tests, build checks, lint, skill validators, plugin validators, documentation sync checks, and manual review according to the local project.

Blocking hook: AiCoding platform repositories should wire scripts/check-documentation-sync.ps1 into pre-commit and CI so code/config/platform changes cannot finish without documentation review.

## Gate Rules

CLI checker: scripts/check-documentation-sync.ps1 -Mode all is the default documentation sync command when the AiCoding platform docs-sync files are installed; project-specific build, test, lint, and skill validation commands remain authoritative for code and Skill changes.

Hook gate: use .githooks/pre-commit and CI required checks to run docs-sync and repository governance gates before commit or merge; when hooks are not installed, run the CLI checker manually and report that hook enforcement is not active.

MCP tool library: no MCP is required for this workflow because repository-local scripts, tests, and docs provide deterministic gates; MCP tools may be added later for project discovery or long-running diagnostics, with the CLI/manual path remaining the fallback.

Human confirmation: owner/confirmation is the AiCoding maintainer or user integrating this workflow; accepted gates are CLI validation, pre-commit hook, CI docs-sync, repository tests, and manual review for requirements, architecture, release, and documentation judgment.

Skip rationale: skip only gates that are not available in the active repository, and replace them with an explicit manual review note or a project-specific command in the final report.
## Human Confirmation

Owner/confirmation: the AiCoding maintainer or user integrating this workflow confirms that standalone AiCoding mode is required and Superpowers remains optional.

Accepted gates: CLI validation, pre-commit hook, CI docs-sync, repository tests, plugin/skill validators, and manual review for requirements, architecture, release, and documentation judgment.

Manual review scope: product intent, MVP tradeoffs, architecture approval, behavior completeness, release readiness, and documentation adequacy remain human-reviewed when they cannot be reliably linted.

Decision: approved for AiCoding integration with the stated gates and manual review boundaries.

Use this skill only when an external `test-driven-development` skill is not available or the user does not want to use Superpowers.

This skill exists so AiCoding can complete the full SDD→MVP→BDD→TDD→Docs Sync workflow independently.

## Scope

This is a minimal but strict TDD workflow. It does not attempt to replace advanced external TDD skills when they are available.

## Inputs

Before using this skill, the agent should already have:

- SDD requirements;
- MVP P0/P1 scope;
- BDD scenarios;
- architecture scaffold;
- test strategy.

## TDD loop

For each module or behavior slice:

```text
1. Select one BDD scenario or requirement slice.
2. Write the smallest failing test that proves the expected behavior.
3. Run or reason about the test failure.
4. Implement the minimum production code required to pass.
5. Run tests again.
6. Refactor without changing behavior.
7. Update traceability and documentation if public behavior, interface, architecture, configuration, or test strategy changed.
```

## Test selection

Prefer this order:

```text
unit test
→ contract test
→ integration test
→ system test
```

For embedded / firmware:

```text
host-side unit test
→ SIL
→ PIL
→ HIL
→ bench validation
```

Use mocks/fakes for hardware boundaries unless the test is explicitly HIL.

## Refactor rule

Refactoring is allowed only after the relevant test passes. If behavior changes during refactor, create or update a BDD scenario and test first.

## Done criteria

A TDD slice is done only when:

- the failing test was created or documented;
- production code passes the test;
- no unrelated behavior was changed;
- relevant documentation and traceability were updated;
- remaining gaps are documented.

Use `references/aicoding-sdd-bdd-docsync/tdd-fallback-template.md`.
