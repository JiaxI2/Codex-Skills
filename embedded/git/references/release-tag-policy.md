# Version, Tag, and Release Policy

## Objects

- Commit: one logical repository change.
- Tag: immutable name for one commit baseline.
- GitHub Release: human-facing notes and downloadable assets attached to a Tag.

## Mainstream composition

Use project needs to combine:

- concise Git/Linux-style commit history;
- versioned CHANGELOG where useful;
- GitHub-generated PR/contributor/compare draft;
- curated engineering release notes;
- firmware compatibility and asset traceability.

No single project style is mandatory.

## Tag configuration

Selectable values:

```text
version.scheme = semver | calendar | product-defined | component-matrix
tag.pattern
tag.annotated
tag.signed
tag.stable_branch
tag.prerelease_pattern
```

Typical:

```text
v1.2.0
v1.2.0-rc.1
```

Use a short Tag message:

```text
Release v1.2.0
```

Push only the intended Tag:

```bash
git push origin v1.2.0
```

## Release Notes sections

Always required for formal releases:

```text
Summary
What's Changed
Compatibility
Release Notes
Full Changelog
Known Issues
Traceability
```

Profile-dependent:

```text
Highlights / Major Changes
Deprecations
Breaking Changes / Migration
Security
New Contributors
Assets / Checksums
Upgrade / Programming
Rollback
```

## Deprecations

For profiles configured to require it:

- include the heading;
- list deprecated behavior and replacement;
- include removal target when known;
- link migration details;
- write `None` when no deprecations exist.

## What's Changed

Use categorized PR links, not raw commit dumps.

Possible categories:

```text
Features
Fixes
Compatibility
Build and Tooling
Documentation
Dependencies
Other
```

## Release Notes

This section may summarize or link a larger document.

## Full Changelog

Use exact previous and current tags:

```markdown
[v1.1.0...v1.2.0](https://github.com/OWNER/REPO/compare/v1.1.0...v1.2.0)
```

## New Contributors

Derive from actual contributors or merged PRs. Do not infer from names in documentation.

## GitHub-generated notes

They can provide:

- merged PR list;
- contributor list;
- compare link.

Use `.github/release.yml` to categorize by labels.

Treat output as a draft. Curate compatibility, deprecations, migration, known issues, firmware, and validation manually.

## Release readiness

Before Tag creation:

- stable commit known;
- worktree clean;
- tests/approvals complete;
- versions consistent;
- changelog/release notes complete;
- assets traceable;
- Tag unused locally and remotely.

Do not move a published Tag. Create a new version.
