---
name: aicoding-behavior-driven-development
description: Convert SDD requirements and MVP scope into BDD behavior scenarios, acceptance criteria, examples, edge cases, and regression obligations before TDD implementation.
---

# AiCoding BDD: Behavior-Driven Development
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

Use this skill after SDD and MVP planning and before TDD implementation.

BDD means **Behavior-Driven Development / 行为驱动开发**.

## Purpose

BDD describes what the system must do from an observable behavior perspective. It bridges requirements and tests.

## Scenario format

Use `Given / When / Then`.

```gherkin
Scenario: <observable behavior>
  Given <initial context>
  And <relevant precondition>
  When <user/system action>
  Then <expected observable result>
  And <state, event, output, or error is correct>
```

## Required scenario coverage

For each P0 requirement, define at least:

- normal path;
- boundary path;
- error path;
- compatibility or migration path if relevant;
- regression path if modifying existing behavior.

For embedded / firmware, also consider:

- initialization;
- ISR or RTOS context;
- timing;
- watchdog;
- communication loss;
- power loss;
- boot / OTA / rollback;
- memory alignment and endianness.

## Mapping to tests

Every BDD scenario should map to at least one test obligation:

```text
Scenario → Unit / Contract / Integration / System / HIL test
```

Use `references/aicoding-sdd-bdd-docsync/bdd-scenarios-template.md`.
