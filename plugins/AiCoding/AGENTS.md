# AiCoding Plugin Assembly Instructions

## Directory Role

This directory is the installable AiCoding Codex plugin assembly.

Human-maintained content:

- `.codex-plugin/plugin.json`
- `hooks/`
- `assets/`
- `README.md`

Generated content:

- `skills/`
- `BUILDINFO.json`

Never manually edit generated content.

## Plugin Rules

Keep plugin component paths relative to the plugin root.

Keep bundled skills flat under `skills/<aicoding-skill-name>/`.

Every bundled skill must be declared in `config/aicoding-plugin-pack.json`.

Do not include `obsidian-*`.

Do not copy `AiCoding/CodingKit/examples`, `modules`, `platforms`, `tests`, or `tools` into this plugin.

Plugin code must not assume that the source repository is adjacent to the installed plugin cache. External CodingKit assets must be resolved through the approved discovery protocol.

## External Asset Discovery

Use this resolution order:

1. `AICODING_HOME`
2. AiCoding installation-state file
3. tools available on `PATH`
4. approved project-root discovery
5. MCP
6. safe failure with actionable instructions

Do not navigate outside the installed plugin with hard-coded relative paths.

## Hook Rules

Hooks are lightweight lifecycle helpers. They must not be used as the only enforcement mechanism for repository safety, authorization, device flashing, destructive operations, or source-control protection.

After hook changes, ensure users are instructed to review the new definition through `/hooks`.

## Verification

Any change in this directory requires:

- plugin validation;
- generated-drift validation;
- hook validation when hooks changed;
- Markdown link validation;
- `git diff --check`.
