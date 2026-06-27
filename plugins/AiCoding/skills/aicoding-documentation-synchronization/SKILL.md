---
name: aicoding-documentation-synchronization
description: Keep AiCoding SDD, BDD, API, architecture, README, changelog, test, release, and embedded documentation synchronized with code changes; pair with hooks and CI for enforcement.
---

# AiCoding Documentation Synchronization
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

Use this skill before finishing any task that changes code, behavior, architecture, interfaces, protocols, configuration, tests, build, release, installation, hooks, or generated plugin exposure.

## Principle

Documentation synchronization is not optional. Docs are part of the implementation contract.

This skill tells the agent what to update. The repository hook and CI gate enforce that relevant documentation updates are present.

## Change-to-document mapping

### Functional behavior change

Update:

- SDD target behavior and requirements;
- BDD scenarios;
- README or usage docs;
- test plan or validation evidence;
- CHANGELOG when user-visible or release-relevant.

### API / interface / protocol change

Update:

- SDD interface contract;
- API docs or header comments;
- README examples;
- compatibility notes;
- CHANGELOG.

### Architecture change

Update:

- SDD architecture impact;
- PDR / ADR;
- architecture diagram or module boundary notes;
- dependency rules;
- migration / rollback notes.

### Configuration / build / install change

Update:

- config documentation;
- install/update/status docs;
- CI or verification docs;
- AGENTS.md if agent workflow changes.

### Test / CI change

Update:

- test strategy;
- validation command list;
- coverage expectation;
- CI documentation.

### Embedded / firmware change

Update when relevant:

- memory map;
- linker command notes;
- boot flow;
- OTA / rollback behavior;
- watchdog and power-loss assumptions;
- SIL/PIL/HIL plan;
- hardware binding notes.

## Same-commit / same-PR rule

If code and docs both need changes, they must be submitted in the same branch and preferably the same commit or PR.

## No-doc-change justification

If the agent determines documentation does not need to change, it must state why.

Acceptable examples:

- purely internal formatting change;
- no behavior, interface, architecture, configuration, test, build, or release impact;
- generated file only and source docs already describe generation behavior.

## Hook integration

When the hook package is installed, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check-documentation-sync.ps1 -Mode pre-commit -Staged
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check-documentation-sync.ps1 -Mode all
```

Use `references/aicoding-sdd-bdd-docsync/documentation-sync-checklist.md`.
