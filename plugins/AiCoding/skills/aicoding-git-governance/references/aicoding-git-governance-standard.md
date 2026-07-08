# AiCoding Git Governance Standard

Standard ID: `aicoding-git-governance`
Standard version: `2026.07`
Canonical source: https://github.com/JiaxI2/Codex-Skills/blob/main/platform/aicoding-git-governance/references/aicoding-git-governance-standard.md
Raw source: https://raw.githubusercontent.com/JiaxI2/Codex-Skills/main/platform/aicoding-git-governance/references/aicoding-git-governance-standard.md

## Repository Policy Contract

Every AiCoding-governed repository must keep `.github/repository-governance.toml` as the local policy instance and must include a `[governance_standard]` section pointing back to this canonical standard.

Required fields:

```toml
[governance_standard]
id = "aicoding-git-governance"
version = "2026.07"
source_url = "https://github.com/JiaxI2/Codex-Skills/blob/main/platform/aicoding-git-governance/references/aicoding-git-governance-standard.md"
raw_url = "https://raw.githubusercontent.com/JiaxI2/Codex-Skills/main/platform/aicoding-git-governance/references/aicoding-git-governance-standard.md"
sync_policy = "track-canonical-url"
```

Repositories may pin a version for a release branch, but normal active repositories should track the canonical URL and update local lint/templates when the standard changes.

## README Standard

Default README governance for the user's repositories is Chinese-first and bilingual:

- `README.md` is the GitHub default entry and must be Chinese-first. English text may appear after a slash in headings.
- `README_CN.md` is the Chinese file-level entry for explicit language switching and GitHub About/Homepage links.
- `README_EN.md` is the English file-level entry.
- The top of `README.md` must include visible links to `README_CN.md` and `README_EN.md`.
- `README.md` must keep an environment badge preview near the top.
- Required baseline badges: latest Release, PowerShell, Python, and License.
- Add repository-specific badges such as Go, Taskfile, CMake, MATLAB, or toolchain badges when those tools are part of the default workflow.
- Badge links must use explicit HTTPS URLs to the tool or GitHub resource.
- README content must describe current durable repository identity and navigation. Dated diff summaries belong in `CHANGELOG.md`, annotated Tag messages, or GitHub Release notes, not README.

## GitHub About Standard

Repositories should expose bilingual metadata:

- `.github/repository-governance.toml` should include `[github_about]`.
- `require_bilingual = true` is the default.
- `homepage` should point to the Chinese-first README entry, usually `README_CN.md` or the default `README.md` when `README.md` is Chinese-first.
- Topics should describe stable repository purpose, not temporary implementation details.

## Branch and Commit Standard

- `main` or `master`: stable production branch.
- `develop`: DEV integration branch when a separate integration branch exists.
- `feature/<scope>`: feature branch.
- `test` or `test/<scope>`: FAT or shared test work.
- `release/<version>`: UAT or pre-production hardening.
- `hotfix/<scope>`: urgent production fix from stable branch.
- Standard commit types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
- A commit should contain one category of change and no more than three tightly related topics.

## CHANGELOG Standard

- Evaluate `CHANGELOG.md` for every normal commit.
- Entries should be Chinese-first with concise English meaning for externally visible changes.
- Do not paste raw `git log` into CHANGELOG.
- Diff summaries are permitted in CHANGELOG and Release notes, not README.

## Tag and GitHub Release Standard

- Tag identifies one commit; GitHub Release contains curated notes.
- Annotated tag messages should be short and bilingual when the repository is Chinese-first.
- GitHub Release notes must be curated, not a stub.
- Required release headings: Summary, What's Changed, Compatibility, Deprecations, Release Notes, Full Changelog, New Contributors, Known Issues, Traceability.
- Chinese-first releases should use bilingual headings such as `摘要 / Summary` while preserving canonical English names.
- `Deprecations` and `New Contributors` must be explicit. Write `None` when not applicable.
- New Contributors must come from real contributor data. Never invent contributors.

## Local Gate Standard

Each repository should keep local hook-equivalent checks:

- `.githooks/pre-commit` calls the configured governance lint.
- `.githooks/commit-msg` enforces typed commit subjects.
- The lint must check README language switching, required badges, canonical governance URL, CHANGELOG typing, release-note policy, placeholders, and markdown links when configured.
