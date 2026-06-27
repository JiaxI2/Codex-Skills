---
name: aicoding-sdd-spec-driven-development
description: Create and maintain Specification-Driven Development documents that define requirements, constraints, interfaces, architecture impact, MVP scope, behavior obligations, tests, and documentation impact before implementation begins.
---

# AiCoding SDD: Specification-Driven Development
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

Use this skill before implementing or modifying non-trivial behavior.

SDD means **Specification-Driven Development / 规范驱动开发**. It is not just a design document. It is the source of truth that links requirements, behavior, tests, architecture, implementation, and documentation.

## Required SDD sections

Every SDD must contain or update these sections:

1. Problem statement and objective.
2. Current behavior and known constraints.
3. Target behavior.
4. Functional requirements.
5. Non-functional requirements.
6. Explicit assumptions.
7. Interfaces, APIs, protocols, files, data formats, configuration, and CLI contracts.
8. Architecture and module impact.
9. MVP scope classification: P0/P1/P2/P3.
10. BDD scenario obligations.
11. Test strategy: unit, contract, integration, system, and embedded-specific tests when relevant.
12. Documentation synchronization impact.
13. Rollback or compatibility plan.
14. Traceability matrix.

## SDD-first rule

Do not begin implementation before the SDD exists for the change.

Small changes may use a short SDD section inside an existing issue, plan, or docs file. Large changes should create a dedicated file, for example:

```text
docs/sdd/<feature-or-change>.md
```

## Change synchronization rule

If the code changes, review whether the SDD must change. If the SDD does not need to change, provide a written no-doc-change justification.

## Output

Produce or update an SDD using `references/aicoding-sdd-bdd-docsync/sdd-template.md`.
