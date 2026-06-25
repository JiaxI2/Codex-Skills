# Commit and CHANGELOG Policy

## Commit style

Use the repository's existing convention. Without one, choose a simple style such as:

```text
<area>: <imperative summary>
```

or:

```text
<type>(<scope>): <imperative summary>
```

The message must explain motivation and effect. For bug fixes, link the introducing commit when known.

## Typed commit taxonomy

Use Conventional Commit-style types unless the repository defines a stricter local taxonomy:

```text
feat     user-visible feature or capability
fix      bug fix
docs     documentation-only change
style    formatting or whitespace change with no meaning change
refactor code restructuring without feature or bug-fix intent
perf     performance improvement
test     test addition or correction
build    build system or dependency change
ci       CI or automation workflow change
chore    repository maintenance, tooling, hooks, or auxiliary files
```

Every commit must choose one primary type. Keep a commit to one logical purpose and no more than three tightly related change topics.

## Mandatory CHANGELOG linkage

For repositories using `changelog.mode = "unreleased"`, every non-release commit must stage a CHANGELOG update unless the repository policy defines a specific exclusion mechanism. The changelog entry must explicitly name the commit type:

```markdown
- **docs**: Add repository usage and submodule initialization instructions.
- **chore**: Install Git hooks that enforce typed commits and changelog updates.
```

For commits that are not user-notable, write the type and exclusion reason in the configured changelog or release-note exclusion path instead of silently omitting it.

## Hook and lint enforcement

Repositories with hook management enabled should enforce:

- commit message subject matches `<type>(<scope>): <summary>` or the configured stricter pattern;
- staged changes include the configured CHANGELOG file for every normal commit;
- required README, CHANGELOG, governance, and release-note files have no unresolved placeholders;
- repository-specific Markdown or release-note validators pass.

Do not use `--no-verify` unless explicitly approved. If a hook is bypassed, report the skipped check and reason.
## Atomicity

One commit represents one logical purpose. Include required test, documentation, and changelog changes for that purpose.

Avoid unrelated formatting, generated files, and another feature.

## CHANGELOG modes

### unreleased

Add notable changes to `[Unreleased]` during development.

### fragments

Create the configured fragment and aggregate at release.

### release-only

Record release-note eligibility in the PR; edit the main changelog in release mode.

### generated

Generate a draft from PR metadata and curate it.

## Categories

Core categories:

```text
Added
Changed
Deprecated
Removed
Fixed
Security
```

Optional categories:

```text
Compatibility
Build
Documentation
Firmware
Known Issues
```

Keep only useful categories.

## Compare links

Recommended:

```markdown
[Unreleased]: https://github.com/OWNER/REPO/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/OWNER/REPO/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/OWNER/REPO/releases/tag/v1.0.0
```

## Entry style

Write effect and impact:

```markdown
- Preserve the reported firmware version after an upgrade ([#123](...)).
```

Do not write:

```markdown
- Modified app.c.
- Updated code.
- Merged branch.
```

## Normal inclusion

- externally meaningful feature;
- released-behavior fix;
- default/compatibility/procedure change;
- deprecation/removal/security;
- artifact naming or delivery change;
- notable known limitation.

## Normal exclusion

- internal refactor with unchanged external behavior;
- formatting;
- typo-only comments;
- merge-only changes;
- internal test cleanup.
