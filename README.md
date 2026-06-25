# Codex-Skills

`Codex-Skills` is the source repository for reusable Codex skills, AiCoding plugin sources, Codex lifecycle hooks, and standalone personal skills.

## Repository Role

- Source of truth for maintained skills and plugin package sources.
- Build source for `plugins/AiCoding`, the deployable AiCoding Codex plugin.
- Home for standalone personal skills such as `obsidian-markdown`, `obsidian-cli`, and `obsidian-bases`.
- Migration source for the current local checkout at `C:\Users\24322\.codex\skills`; this path is retained during migration and should not be deleted automatically.

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

## Maintenance Rules

- Keep each skill source in one place; generated plugin copies are not source.
- Update `CHANGELOG.md` for every normal commit and mark the commit type explicitly.
- Keep Codex hooks and Git hooks separate.
- Do not package `obsidian-*` into AiCoding.
- Do not hard-code personal absolute paths in plugin files, hooks, or scripts.
- Do not rebuild AiCoding plugin from inside the AiCoding submodule checkout; build in Codex-Skills, commit, then update the AiCoding submodule pointer.
- For kit maintenance tasks, follow `AGENTS.md` first, then `platform/aicoding-kit-maintenance/SKILL.md`, then `docs/ARCHITECTURE.md` and `docs/PLUGIN_DEVELOPMENT.md`.
