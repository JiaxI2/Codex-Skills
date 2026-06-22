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
