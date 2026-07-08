# Codex-Skills

中文文档 / Chinese documentation: [README_CN.md](README_CN.md).

`Codex-Skills` is the source repository for reusable Codex skills, AiCoding plugin sources, Codex lifecycle hooks, and standalone personal skills.

## Repository Role

- Source of truth for maintained skills and plugin package sources.
- Build source for `plugins/AiCoding`, the deployable AiCoding Codex plugin.
- Home for standalone personal skills such as `obsidian-markdown`, `obsidian-cli`, and `obsidian-bases`.
- Source repository for skills and plugin package content; runtime environments should expose explicit standalone skill directories or the installed AiCoding plugin, not this whole repository as a long-term Skill Root.

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

The short version:

- `embedded/` contains embedded-domain skill sources.
- `platform/` contains cross-domain platform workflow skill sources, including Git governance.
- `plugins/AiCoding/skills/` is generated from `config/aicoding-plugin-pack.json`; do not edit it by hand.
- `plugins/AiCoding/hooks/` is manually maintained plugin hook source.
- `.agents/plugins/marketplace.json` is the development marketplace for local plugin testing.

## Directory Guide

- `embedded/`: embedded firmware skill family: C99, architecture, ARM, DSP, EtherCAT/CiA402, OS, motor control, and review routing.
- `platform/aicoding-git-governance/`: Git-Skill source for branch, commit, CHANGELOG, release, hook, and repository governance workflows.
- `platform/aicoding-kit-maintenance/`: maintenance workflow for Codex-Skills/AiCoding architecture, plugin packaging, submodule updates, hooks, and completion gates.
- `platform/aicoding-sdd-bdd-tdd-development-flow/`: standalone-capable SDD, MVP, BDD, architecture-first, TDD fallback, layered verification, and documentation synchronization workflow for AiCoding.
- `platform/aicoding-user-skill-creator/`: User-Skill-Creator source for creating, validating, improving, and migrating AiCoding user skills without conflicting with the system `skill-creator`.
- `plugins/AiCoding/`: generated/installable Codex plugin package with manual manifest/hooks and generated skills/BUILDINFO.
- `config/aicoding-plugin-pack.json`: single source for which skills are packaged into AiCoding.
- `scripts/build-plugin.ps1`: reproducible plugin generation.
- `scripts/verify-plugin.ps1`: plugin package validation.
- `scripts/compare-generated.ps1`: repeated-build drift check.
- `obsidian-*`: standalone personal Obsidian skills; not packaged into AiCoding.

## Build And Verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-plugin.ps1 -Plugin AiCoding -Configuration Development -Clean -Verify
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/compare-generated.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify-skills.ps1
```

For release builds, use `-Configuration Release` only from a clean source tree excluding generated plugin outputs.

## Runtime Principles

- `aicoding-*` capabilities are exposed as a group through the AiCoding Plugin.
- Standalone skills are exposed through explicit user Skill Root directories or links.
- Do not edit `plugins/AiCoding/skills/` or `plugins/AiCoding/BUILDINFO.json` by hand.
- Do not modify the Codex plugin cache directly.
## Git Governance Standard

All AiCoding-governed Git repositories should write their branch, environment, commit type, and release-note rules in README or an equivalent governance document.

- Branches: `main` or `master` is the stable production branch and must not receive direct code edits except approved release or hotfix integration; `develop` is the DEV integration branch; `feature/<scope>` branches start from `develop`; `test` maps to FAT when a shared test environment exists; `release/<version>` maps to UAT/pre-production; `hotfix/<scope>` starts from `main` and is merged back to `main` and `develop`.
- Environments: `DEV` is developer debugging, `FAT` is functional acceptance testing, `UAT` is user acceptance/pre-production, and `PRO` is production.
- Commit types: `feat` adds functionality, `fix` repairs bugs, `docs` changes documentation only, `style` changes formatting without behavior impact, `refactor` restructures code without feature or bug-fix intent, `perf` improves performance, `test` adds or corrects tests, and `chore` changes build/supporting tools or maintenance files.
- Single commits: one commit should contain one category of change, no more than three tightly related topics, and a typed subject such as `feat(scope): summary`.
- Releases: Tag and GitHub Release notes must group every included commit by type, state the primary release type, and describe the concrete user-facing or maintenance impact.

## Maintenance Rules

- Keep each skill source in one place; generated plugin copies are not source.
- Update `CHANGELOG.md` for every normal commit and mark the commit type explicitly.
- Keep Codex hooks and Git hooks separate.
- Do not package `obsidian-*` into AiCoding.
- Do not hard-code personal absolute paths in plugin files, hooks, or scripts.
- Do not rebuild AiCoding plugin from inside the AiCoding submodule checkout; build in Codex-Skills, commit, then update the AiCoding submodule pointer.
- For kit maintenance tasks, follow `AGENTS.md` first, then `platform/aicoding-kit-maintenance/SKILL.md`, then `docs/ARCHITECTURE.md` and `docs/PLUGIN_DEVELOPMENT.md`.
