# Codex-Skills / AiCoding Architecture

## Repository Boundaries

`Codex-Skills` is the only source repository for maintained skills, plugin packaging, and Codex lifecycle hook source. `AiCoding` is the platform integration repository and new-machine entry point. It locks `Codex-Skills` through `CodingKit/agents/skills` as a Git submodule and must not copy or manually maintain skill source.

## Source And Generated Boundaries

Manual source:

- `embedded/`
- `platform/`
- `plugins/AiCoding/.codex-plugin/plugin.json`
- `plugins/AiCoding/hooks/`
- `plugins/AiCoding/README.md`
- `config/aicoding-plugin-pack.json`
- `scripts/*.ps1`

Generated output:

- `plugins/AiCoding/skills/`
- `plugins/AiCoding/BUILDINFO.json`

Generated files are created by `scripts/build-plugin.ps1`. They must not be edited manually. The build writes `plugins/AiCoding/skills/.generated` as a local marker.

## BUILDINFO Model

`BUILDINFO.json` is intentionally non-self-referential. `sourceCommit` records the input `HEAD` used for the build before the generated `BUILDINFO.json` is committed. `BUILDINFO.json` is excluded from package digests, and `buildInfoModel` records this rule explicitly.

To avoid repeated-build drift, `buildTimestampUtc` uses the input commit time instead of wall-clock time. A repeated build with unchanged inputs must leave `git status` unchanged.

## Plugin Installation And Cache Refresh

Formal installation is through a Codex Marketplace entry, not by manually editing the Codex plugin cache. The development marketplace is `.agents/plugins/marketplace.json`; the AiCoding platform marketplace lives in `AiCoding/.agents/plugins/marketplace.json` and points at the submodule package path.

Codex may load plugins from an installed/cache copy. Updating the AiCoding submodule does not automatically refresh an already installed local plugin. The platform update flow must explicitly:

1. update the submodule;
2. verify the packaged plugin;
3. refresh or reinstall the plugin through supported Codex plugin surfaces when available;
4. re-check `/hooks` because changed plugin-bundled hooks require review/trust again.

Scripts must check whether the local Codex CLI supports plugin commands before invoking them. If the CLI is unavailable, scripts report the next manual `/plugins` step instead of editing cache directories directly.

## CodingKit Asset Discovery Protocol

Plugin skills and hooks do not copy `CodingKit/examples`, `CodingKit/modules`, `CodingKit/platforms`, `CodingKit/tests`, or `CodingKit/tools`. External assets are discovered by protocol:

1. prefer `AICODING_HOME` when explicitly set;
2. otherwise walk upward from the active repository `cwd` until `config/codex-kit.json` is found;
3. validate that the manifest contains `codingKitRoot` and that expected asset directories exist;
4. treat missing assets as capability unavailable, not as plugin failure.

AiCoding owns `config/codex-kit.json`. Codex-Skills only documents the protocol and may provide helpers later.

## Hook Boundary

Codex lifecycle hooks are auxiliary workflow constraints. They can remind, block, or route based on local repository state, but they are not a complete security boundary and must not be treated as a replacement for Git hooks, CI, branch protection, code review, or human release approval.

Plugin hooks must:

- use `PLUGIN_ROOT` and `PLUGIN_DATA` when accessing plugin-local or writable plugin state;
- avoid personal absolute paths;
- fail with clear JSON output;
- avoid modifying business source code;
- remain conservative when input JSON is missing or malformed.

## AiCoding Submodule Rule

AiCoding must not rebuild `plugins/AiCoding` inside `CodingKit/agents/skills`. The correct flow is:

```text
Codex-Skills: edit source -> build plugin -> verify -> commit -> push
AiCoding: update submodule -> verify/install -> commit platform pointer
```

This keeps submodule content reproducible and avoids dirty submodule working trees.