# Codex-Skills Agent Instructions

## Repository Role

This repository is the authoritative source for Codex skills, the AiCoding plugin package, and plugin-bundled Codex hooks.

AiCoding consumes this repository through a Git submodule. Never treat AiCoding as a second skill source.

Before making changes, read:

- `docs/ARCHITECTURE.md`
- `docs/PLUGIN_DEVELOPMENT.md`
- `config/aicoding-plugin-pack.json`
- `plugins/AiCoding/AGENTS.md` when modifying the plugin
- the closest nested `AGENTS.md` for the target directory

## Source Ownership

Human-maintained canonical sources:

- `embedded/`
- `platform/`
- root standalone skills such as `obsidian-markdown/`
- `plugins/AiCoding/.codex-plugin/`
- `plugins/AiCoding/hooks/`
- `plugins/AiCoding/assets/`
- `config/`
- `scripts/`
- `tests/`
- `docs/`

Generated files:

- `plugins/AiCoding/skills/`
- `plugins/AiCoding/BUILDINFO.json`

Do not manually edit generated files. Regenerate them through repository build scripts.

## Skill Classification

Use `embedded/` for skills directly related to firmware, MCU, DSP, motor control, embedded debugging, communication, boot, OTA, real-time constraints, MATLAB, or Simulink embedded workflows.

Use `platform/` for cross-domain engineering capabilities such as Git governance, repository governance, release workflows, CI, documentation standards, agent workflow governance, and general code review.

Keep `obsidian-*` and other personal general-purpose skills as standalone root skills unless a separate plugin is explicitly approved. Do not package Obsidian skills into the AiCoding plugin.

## Plugin Packaging

`config/aicoding-plugin-pack.json` is the only authority for which canonical skills are packaged into the AiCoding plugin.

Plugin skills must:

- use the `aicoding-` namespace;
- use the flat structure `plugins/AiCoding/skills/<skill-name>/SKILL.md`;
- have a directory name matching the `SKILL.md` front matter name;
- be generated from canonical sources;
- not contain personal absolute paths.

When adding or removing a bundled skill:

1. Modify the canonical source.
2. Modify `config/aicoding-plugin-pack.json`.
3. Run the plugin build.
4. Run plugin verification.
5. Run generated-drift verification.
6. Update documentation and `CHANGELOG.md`.

## BUILDINFO Constraints

`BUILDINFO.json` must remain deterministically generated. Do not add unstable values such as build timestamps, usernames, machine names, absolute local paths, random identifiers, or the commit containing `BUILDINFO.json` itself.

Git source identity is provided by the repository commit and the AiCoding submodule gitlink.

## Hook Constraints

Codex hooks are maintained under `plugins/AiCoding/hooks/`.

Hooks:

- are auxiliary checks and context helpers, not complete security boundaries;
- must use `PLUGIN_ROOT` for read-only plugin resources;
- must use `PLUGIN_DATA` or an approved temporary directory for writable data;
- must not contain personal absolute paths;
- must define bounded timeouts;
- must fail safely without modifying the business repository;
- must not automatically commit, push, flash devices, or rewrite business code;
- require user review through `/hooks` after relevant definition changes.

## Required Workflow

For a canonical skill change:

1. Modify only the canonical skill.
2. Run skill-specific validation.
3. Rebuild the plugin when the skill is bundled.
4. Run plugin validation.
5. Run generated-drift checks.
6. Run repository-wide skill validation.
7. Update `CHANGELOG.md` when behavior changes.

For a plugin manifest, hook, or asset change:

1. Modify the human-maintained plugin source.
2. Regenerate deterministic package metadata.
3. Run plugin validation.
4. Run hook tests where applicable.
5. Run generated-drift checks.
6. Update documentation and `CHANGELOG.md`.

## Required Verification

Before considering work complete, run the repository-provided equivalents of:

- plugin build;
- plugin verification;
- generated-drift check;
- skill verification;
- official plugin validation when available;
- relevant skill quick/gate validation;
- Markdown link validation;
- `git diff --check`.

Do not claim completion if required validation failed.

## Cross-Repository Release Order

When changes must reach AiCoding:

1. Complete and verify Codex-Skills.
2. Commit Codex-Skills.
3. Push Codex-Skills when requested.
4. Optionally create the approved release tag.
5. Only then update the AiCoding submodule.

Never make AiCoding depend on uncommitted Codex-Skills files.

## Prohibited Actions

Do not:

- edit generated plugin skills manually;
- rebuild the plugin from inside AiCoding;
- add Obsidian skills to the AiCoding plugin;
- put Git governance under `embedded/`;
- introduce personal absolute paths;
- bypass Hook trust;
- directly edit the Codex plugin cache;
- discard uncommitted work with destructive Git commands;
- update the AiCoding submodule before the Codex-Skills commit exists.

## Definition Of Done

Work is complete only when canonical source is correct, generated output matches the source and package manifest, required validation passes, documentation is updated, the working tree contains no unexplained generated drift, and any cross-repository dependency update follows the required release order.
