# Quick Ref Index

## `ref readme`

Read:

```text
references/readme-policy.md
references/profile-catalog.md
```

Asset:

```text
assets/README_TEMPLATE.md
```

Apply:

```bash
python scripts/render_governance_templates.py \
  --config .github/repository-governance.toml \
  --only readme
```

## `ref changelog`

Read:

```text
references/commit-changelog-policy.md
```

Asset:

```text
assets/CHANGELOG_TEMPLATE.md
```

## `ref commit`

Read:

```text
references/commit-changelog-policy.md
```

Show the atomic-commit and changelog checklist.

## `ref branch`

Read:

```text
references/branch-policy.md
references/profile-catalog.md
```

## `ref tag`

Read:

```text
references/release-tag-policy.md
```

Explain commit vs Tag vs GitHub Release and the authorization boundaries.

## `ref release [profile]`

Read:

```text
references/release-tag-policy.md
references/profile-catalog.md
```

Asset:

```text
assets/RELEASE_NOTES_TEMPLATE.md
```

Validate:

```bash
python scripts/validate_release_notes.py \
  --config .github/repository-governance.toml \
  RELEASE_NOTES.md
```

## `ref firmware`

Read:

```text
references/firmware-policy.md
```

Asset:

```text
assets/FIRMWARE_RELEASE_README_TEMPLATE.md
```

## `ref links`

Read:

```text
references/readme-policy.md
```

Validate:

```bash
python scripts/validate_markdown_links.py README.md CHANGELOG.md
```
