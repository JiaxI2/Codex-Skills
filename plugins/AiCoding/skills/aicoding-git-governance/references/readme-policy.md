# README and Link Policy

## Principle

README is the project entrance and navigation layer. Move detailed procedures to linked documents when the README becomes hard to scan.

README should show the current repository shape, not historical diffs. Keep dated diff summaries, release-note fragments, and raw change lists in CHANGELOG, Tag messages, or GitHub Release notes.

## Adapt the structure

Select sections from the configured README profile. Do not retain empty sections or irrelevant public-project sections in a private repository.

## Link standards

### Repository files

Use relative links:

```markdown
[构建说明](docs/BUILD.md)
[贡献指南](CONTRIBUTING.md)
[变更日志](CHANGELOG.md)
```

### Headings

Use anchor links for navigation:

```markdown
[快速开始](#快速开始)
```

Revalidate anchors after renaming headings.

### External URLs

Use descriptive labels and HTTPS:

```markdown
[在线文档](https://example.com/docs)
```

Avoid unexplained raw URLs in prose.

### Reference-style links

Use for repeated or variable destinations:

```markdown
[最新版本][latest-release]
[问题反馈][issues]

[latest-release]: https://github.com/OWNER/REPO/releases/latest
[issues]: https://github.com/OWNER/REPO/issues
```

### GitHub links

```text
latest release:
https://github.com/<owner>/<repo>/releases/latest

specific release:
https://github.com/<owner>/<repo>/releases/tag/<tag>

compare:
https://github.com/<owner>/<repo>/compare/<old-tag>...<new-tag>

issue:
https://github.com/<owner>/<repo>/issues/<number>

pull request:
https://github.com/<owner>/<repo>/pull/<number>
```

## README update decisions

Update for changes to:

- purpose, status, audience, support scope;
- setup/build/use/programming/upgrade;
- documentation locations;
- repository navigation;
- downloads and stable-release entry;
- contribution, issue, security, or license entry.

Do not update for every implementation-level fix.

## Validation

Before commit or release:

- relative targets exist;
- referenced anchors exist;
- reference definitions exist;
- no unresolved `{{PLACEHOLDER}}`;
- branch names and release URLs are current;
- direct asset links match actual assets;
- Chinese and English README files do not contradict each other;
- badges are accurate and maintained.
