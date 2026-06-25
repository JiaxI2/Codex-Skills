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

## Release language

GitHub Release notes may be Chinese, English, or bilingual.

Default language comes from repository evidence. If README and CHANGELOG are Chinese-first, use Chinese by default. For the first GitHub Release in a repository, ask the user to confirm the release language when it is not already specified; the default choice is Chinese.

Bilingual releases are supported. Use Chinese first and keep the canonical English section name after a slash, for example:

```markdown
## 摘要 / Summary
## 变更内容 / What's Changed
## 兼容性 / Compatibility
## 废弃项 / Deprecations
## 发布说明 / Release Notes
## 完整变更 / Full Changelog
## 新贡献者 / New Contributors
## 已知问题 / Known Issues
## 可追溯性 / Traceability
```
## Release Notes sections
Always required for formal releases:

```text
Summary
What's Changed
Compatibility
Deprecations
Release Notes
Full Changelog
New Contributors
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

For GitHub Releases and profiles configured to require it:

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

Include the heading in GitHub Releases. Derive entries from actual contributors or merged PRs. Do not infer from names in documentation. Write `None` when there are no new contributors.

## Minimum body quality

Do not publish a GitHub Release body that contains only `Summary` or a generated stub. If a section is not applicable, keep the heading and write `None` or `Not applicable`.

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
