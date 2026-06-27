---
name: aicoding-sdd-bdd-tdd-development-flow
description: Orchestrate AiCoding's standalone-capable SDD, MVP, BDD, architecture-first, TDD, layered verification, and documentation synchronization workflow. Superpowers may be reused when available but is never required.
---

# AiCoding SDD + MVP + BDD + TDD Development Flow
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

Use this skill when the user asks the agent to implement, modify, refactor, debug, document, or maintain non-trivial software, firmware, tooling, automation, architecture, protocol, build, release, or documentation behavior in an AiCoding-managed project.

This is the top-level orchestration skill. It must keep working even if Superpowers is not installed or the user does not follow the Superpowers workflow.

## Compatibility principle

Superpowers is optional. AiCoding's workflow must remain self-contained.

```text
If Superpowers skills are available:
  reuse them as accelerators where they fit.

If Superpowers skills are not available:
  use the local AiCoding fallback skills and templates in this kit.

Never block, skip, or weaken the SDD→MVP→BDD→TDD→Docs Sync flow just because Superpowers is absent.
```

## Execution modes

### Mode A: Standalone AiCoding Mode

Use this mode by default when external skills are unknown or unavailable.

Required local skills:

- `aicoding-sdd-spec-driven-development`
- `aicoding-mvp-planning`
- `aicoding-behavior-driven-development`
- `aicoding-architecture-first-scaffolding`
- `aicoding-tdd-fallback`
- `aicoding-documentation-synchronization`

### Mode B: Superpowers-Enhanced Mode

Use this mode only when compatible Superpowers skills are installed and useful.

Optional reusable skills:

- `test-driven-development`
- `writing-plans`
- `systematic-debugging`
- `code-review`
- `finishing-a-branch`

Even in this mode, AiCoding SDD, MVP, BDD, architecture-first scaffolding, traceability, and documentation synchronization remain mandatory.

## Core workflow

```text
SDD First
→ MVP Scope Gate
→ BDD Behavior Specification
→ PDR / ADR Architecture Review
→ Architecture-first Scaffolding
→ Architecture Validation Gate
→ TDD Implementation
→ Unit / Contract / Integration / System Test
→ Documentation Synchronization
→ Traceability / Verification Report
```

## Gate 1: SDD First

Before changing code, create or update the SDD. The SDD must describe:

- purpose and problem statement;
- functional requirements;
- non-functional requirements;
- constraints and assumptions;
- public API, protocol, data, configuration, and file format contracts;
- architecture and module impact;
- MVP scope;
- BDD scenarios and test obligations;
- documentation synchronization impact;
- embedded / firmware constraints when relevant.

## Gate 2: MVP Scope

Classify scope into:

- P0: must be delivered for the first useful vertical slice;
- P1: high-value follow-up or high-risk dependency;
- P2: useful but deferrable enhancement;
- P3: explicitly out of scope for this change.

The first implementation must prefer the smallest useful end-to-end slice that validates the main risk.

## Gate 3: BDD Behavior

Translate P0 and high-risk P1 requirements into behavior scenarios. Use `Given / When / Then` language.

BDD scenarios describe externally observable behavior, including:

- normal path;
- boundary path;
- error path;
- compatibility path;
- configuration path;
- regression path.

## Gate 4: PDR / ADR Architecture Review

Before writing concrete logic, record the architecture decision or design review:

- selected design;
- rejected alternatives;
- interface boundaries;
- dependency direction;
- data ownership;
- concurrency / interrupt / lifecycle constraints;
- failure mode and rollback strategy;
- testing strategy.

For small changes, this may be a short ADR section inside the SDD. For larger work, use a dedicated PDR/ADR document.

## Gate 5: Architecture-first Scaffolding

Before adding full business logic, create the architecture skeleton:

- directories and module boundaries;
- public headers/interfaces/contracts;
- dependency direction;
- stubs, mocks, fakes, or placeholders;
- build wiring;
- minimal runnable path;
- smoke tests or compile/link verification.

Do not fill in complex implementation until the skeleton is validated.

## Gate 6: Architecture Validation

The skeleton must pass the applicable minimum checks before implementation continues:

- compile / link / type check;
- interface contract check;
- minimal smoke test;
- dependency direction check;
- test harness bootstrapping;
- embedded memory map / linker / boot path sanity when relevant.

## Gate 7: TDD Implementation

Use the best available TDD path:

```text
If an external `test-driven-development` skill is available:
  use it for detailed red-green-refactor execution.
Else:
  use `aicoding-tdd-fallback`.
```

The required local loop is always:

```text
write failing test
→ implement minimum code
→ pass test
→ refactor
→ update traceability
```

## Gate 8: Layered Verification

Use the test pyramid appropriate to the project:

```text
static check
→ unit test
→ contract test
→ integration test
→ system test
```

For embedded and firmware work, extend with SIL, PIL, HIL, fault injection, watchdog, power-loss, memory-map, boot, OTA, rollback, and timing checks when relevant.

## Gate 9: Documentation Synchronization

Run `aicoding-documentation-synchronization` before declaring completion.

If the AiCoding documentation synchronization hook is installed, the final commit must also pass:

```text
scripts/check-documentation-sync.ps1 -Mode pre-commit -Staged
scripts/check-documentation-sync.ps1 -Mode all
```

Code and docs must stay in the same branch and preferably the same commit or PR.

## Agent execution rule

The agent must not claim completion until it can answer:

1. Which SDD section changed?
2. Which MVP items were delivered or deferred?
3. Which BDD scenarios cover the behavior?
4. Which architecture interfaces or modules changed?
5. Which TDD path was used: Superpowers TDD or AiCoding fallback TDD?
6. Which tests prove the behavior?
7. Which documents were synchronized?
8. Did the documentation synchronization hook or equivalent policy check pass?
9. What remains out of scope or risky?

## Output format

End with an implementation report:

```markdown
## Implementation Report

### Execution Mode
- Mode: Standalone AiCoding / Superpowers-Enhanced
- External skills used:
- Local fallbacks used:

### SDD / Requirements
- Updated:
- Deferred:

### MVP Scope
- P0 delivered:
- P1/P2 deferred:
- P3 out of scope:

### BDD Scenarios
- Scenario IDs:
- Acceptance coverage:

### Architecture
- Skeleton created/validated:
- Interfaces changed:
- PDR/ADR updated:

### TDD / Tests
- TDD mode: external skill / `aicoding-tdd-fallback`
- Unit tests:
- Contract tests:
- Integration/system tests:

### Documentation Sync
- Documents updated:
- Hook / CI / policy check:
- No-doc-change justification, if any:

### Traceability
| Requirement | Scenario | Test | Code | Document |
|---|---|---|---|---|

### Risks / Follow-up
-
```
