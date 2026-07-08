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

## Bilingual README policy

For AiCoding-governed repositories, use the user standard: Chinese-first GitHub default README with file-level bilingual entries:

- `README.md`: Chinese-first GitHub default entry with concise repository identity, environment badges, quick start, install/update/status commands, and links.
- `README_CN.md`: explicit Chinese file-level entry for language switching and GitHub About/Homepage links.
- `README_EN.md`: explicit English file-level entry.
- `README.md` must include visible top-of-file links to both `README_CN.md` and `README_EN.md`.
- `README.md` must include Release, PowerShell, Python, and License badges with explicit HTTPS URLs by default; add repository-specific tool badges when applicable.
- `.github/repository-governance.toml` must include `[governance_standard]` with the canonical standard URL and raw URL so repositories can stay synchronized.
- Keep language files consistent on repository role, install commands, update commands, support boundary, and release links.
- Do not copy raw CHANGELOG entries into either README.
- Do not use dated diff summaries in README files; release summaries belong in CHANGELOG, Tag messages, or GitHub Release notes.

`README.zh-CN.md` remains acceptable only for existing repositories that already use that name. New AiCoding-governed repositories should use `README_CN.md` and `README_EN.md`.

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
