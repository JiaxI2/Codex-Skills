---
name: embedded-git-workflow
description: >
  Configurable Git, GitHub, documentation, version, tag, release, and firmware-governance workflow
  for embedded repositories. Use for branch, commit, push, pull request, merge, README, CHANGELOG,
  version files, Git tags, GitHub Releases, release notes, firmware artifacts, test baselines,
  production baselines, customer deliveries, or requests such as "ref readme", "ref changelog",
  "ref release", "ref tag", and "ref branch". First resolve repository needs, then select and apply
  an appropriate profile instead of forcing one Linux, OpenAI, PX4, Git Flow, or README style.
---

# Embedded Git Workflow

## Purpose

Apply a selectable, repository-specific Git and release standard.

This skill combines mainstream engineering ideas without copying one project wholesale:

- Linux/Git: logical commits, clear motivation, reviewable history, trailers, backport awareness;
- GitHub: Pull Requests, branch protection, generated release notes, contributors, compare links;
- OpenAI/Codex: small routing file with references, assets, scripts, and explicit evaluation cases;
- mature firmware projects: compatibility, deprecations, migration, artifacts, checksums, baselines;
- strong README practices: navigable structure, relative links, external URLs, version and release links.

The skill must choose a fit-for-purpose profile. It must not impose every section or workflow on every repository.

## Operating model

The workflow has four layers:

1. **Questions** — resolve what this repository actually needs.
2. **Profiles** — select branch, README, changelog, version, release, and artifact policies.
3. **Actions** — inspect, standardize, commit, merge, release, or package.
4. **Verification** — validate links, required sections, version consistency, and actual Git results.

## Step 1: Read repository policy

Read applicable files:

```text
AGENTS.md
AGENTS.override.md
CONTRIBUTING.md
README.md
README.zh-CN.md
CHANGELOG.md
VERSION
VERSION.txt
version.h
docs/VERSION_RECORDS.md
.github/repository-governance.toml
.github/release.yml
.github/
firmware/
```

If `.github/repository-governance.toml` exists, use it as the repository's selectable-policy configuration.

This file is a convention used by this skill, not a built-in GitHub file.

If it does not exist:

- infer current practice from the repository;
- for ordinary work, propose a configuration but do not create one silently;
- when the user asks to establish or standardize policy, create it from
  `assets/REPOSITORY_GOVERNANCE_TEMPLATE.toml`;
- replace or remove every unresolved placeholder before committing.

Repository-specific explicit rules override this skill when safe. Report conflicts before write or publish actions.

## Step 2: Inspect state

Use read-only checks appropriate to the task:

```bash
git rev-parse --show-toplevel
git status --short --branch
git branch -vv
git log --oneline --decorate --graph -15
git remote -v
git tag --sort=-version:refname
git diff --stat
git diff
git diff --cached
```

When remote freshness matters and network access is allowed:

```bash
git fetch --prune --tags
```

State when remote branch, contributor, PR, or Tag information may be stale.

## Step 3: Resolve the decision questions

Read `references/decision-questionnaire.md`.

Resolve only questions material to the request. Do not interrogate the user about values that can be determined from the repository.

Key decisions:

```text
repository audience
repository visibility
release consumers
branch/environment model
README profile and language
CHANGELOG mode
version scheme
Tag policy
Release Notes profile
release notes language
firmware artifact policy
automation level
permission boundary
```

If a missing answer would change a destructive or externally visible action, ask before acting.

## Step 4: Select profiles

Select one value for each applicable policy:

```text
branch.profile
readme.profile
changelog.mode
version.scheme
release.profile
release.notes_mode
firmware.storage
```

Profiles are defined in `references/profile-catalog.md`.

Use `existing-custom` when the repository already has a sound model that does not match a supplied profile.

Profiles are composable. For example:

```text
branch.profile = github-flow-lite
readme.profile = open-source-firmware
changelog.mode = unreleased
release.profile = firmware-minor
firmware.storage = github-release
```

Do not add unused long-lived branches, README sections, changelog categories, or release sections.

## Step 5: Classify the primary mode

Choose one:

```text
inspect
quick-ref
standardize
commit
push
pull-request
merge
release
hotfix
firmware-package
```

Read `references/task-modes.md` for the selected mode.

### Quick Ref commands

Treat these forms as quick-reference requests:

```text
ref readme [profile]
ref changelog [mode]
ref commit
ref branch [profile]
ref tag
ref release [profile]
ref firmware
ref links
```

For a Quick Ref request:

- remain read-only unless the user also asks to apply it;
- load only the named reference;
- show the decision rules, minimal checklist, and relevant asset;
- do not dump every policy file;
- offer the exact path or command needed to apply the profile.

Quick Ref routing is in `references/quick-ref-index.md`.

## Step 6: Output the governance decision

Before write actions, output:

```text
Git Governance Decision
- Mode:
- Branch profile:
- README profile:
- CHANGELOG mode:
- Version scheme:
- Release profile:
- Release language:
- Artifact storage:
- Current branch:
- Source branch:
- Target branch:
- README:
- README LINKS:
- CHANGELOG:
- VERSION:
- VERSION RECORD:
- COMMIT:
- PUSH:
- PULL REQUEST:
- MERGE:
- BACK-MERGE:
- TAG:
- TAG PUSH:
- RELEASE NOTES:
- FIRMWARE PACKAGE:
- GITHUB RELEASE:
- Reason:
```

Use:

```text
REQUIRED
NOT REQUIRED
RELEASE ONLY
PROPOSE
BLOCKED
NOT APPLICABLE
```

Do not omit README, CHANGELOG, version, Tag, or Release decisions merely because the user did not mention them.

## Step 7: Respect separate permissions

Treat these independently:

```text
edit files
stage
commit
push branch
create PR
merge
create Tag
push Tag
create GitHub Release
upload assets
```

Examples:

- “提交修改” authorizes commit, not push, merge, Tag, or Release.
- “提交并推送” authorizes commit and branch push, not merge or Tag.
- “创建 Tag” does not authorize pushing it.
- “发布版本” selects release mode but remains subject to repository approval rules.

## Step 8: Apply only relevant references

| Need | Reference |
|---|---|
| resolve requirements | `references/decision-questionnaire.md` |
| choose profiles | `references/profile-catalog.md` |
| task actions | `references/task-modes.md` |
| branch/merge | `references/branch-policy.md` |
| README/links | `references/readme-policy.md` |
| commit/changelog | `references/commit-changelog-policy.md` |
| version/Tag/Release | `references/release-tag-policy.md` |
| firmware artifacts | `references/firmware-policy.md` |
| quick reference | `references/quick-ref-index.md` |
| behavior tests | `references/eval-cases.md` |

Do not load every reference by default.

## Commit governance gate

For every commit managed by this skill, classify the commit before staging or committing.

Allowed commit types:

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

Rules:

- each commit must have one primary type;
- one commit should contain one logical purpose and no more than three tightly related change topics;
- the commit subject should use `<type>(<scope>): <summary>` when the repository has no stricter convention;
- `CHANGELOG.md` must be evaluated for every commit;
- when `changelog.mode = "unreleased"`, every non-release commit must update `[Unreleased]` with entries that explicitly name the commit type, for example `- **docs**: ...`;
- if a commit is intentionally not user-notable, record the type and reason in the changelog or in the repository's configured release-note exclusion mechanism;
- repository lint and Git hooks must enforce the typed commit subject and required CHANGELOG update whenever the repository has hooks enabled.

Before committing, run the repository's configured lint or hook-equivalent checks. Do not bypass hooks unless the user explicitly approves the bypass and the completion report names the skipped check.
## Core defaults

For an ordinary development commit:

```text
VERSION: RELEASE ONLY
VERSION RECORD: RELEASE ONLY
TAG: NOT REQUIRED
TAG PUSH: NOT REQUIRED
RELEASE NOTES: NOT REQUIRED
FIRMWARE PACKAGE: RELEASE ONLY
GITHUB RELEASE: NOT REQUIRED
```

README and CHANGELOG must still be evaluated.

### README changes are normally required when

- project purpose, audience, support scope, or status changes;
- setup, build, usage, programming, upgrade, or download instructions change;
- repository navigation or documentation locations change;
- stable-release, issue, contribution, security, or license links change.

README is normally not changed for an internal bug fix with no effect on project entry or usage.

README must describe current, durable repository identity, navigation, and usage. Do not add dated diff summaries, raw release notes, or changelog-style change lists to README. Put change summaries in CHANGELOG during development, and in Tag/GitHub Release notes for formal releases.

### CHANGELOG changes are normally required when

- users, testers, integrators, operators, production, or customers need to know;
- behavior, defaults, compatibility, procedures, deprecations, removals, security, packaging, or notable limitations change.

Do not copy raw `git log` into CHANGELOG.

### Release language

GitHub Release notes support Chinese, English, or bilingual content.

- Infer the default from the repository's README and CHANGELOG language.
- For Chinese-first repositories, default to Chinese.
- For the first GitHub Release in a repository, ask for the release language when the user has not specified it; present Chinese as the default.
- If bilingual notes are selected, write Chinese first and keep the canonical English section name after a slash, for example `摘要 / Summary`, so tooling can still validate required sections.
- Do not silently publish English-only release notes for a Chinese-first repository.
### Tag and Release
A Tag identifies one commit. A GitHub Release presents detailed notes and assets for a Tag.

If `GITHUB RELEASE` is `REQUIRED`, then `RELEASE NOTES` is also `REQUIRED`. Do not downgrade a GitHub Release to `TAG MESSAGE ONLY`; the release body must be curated before publishing or editing.

Keep annotated Tag messages short:

```text
Release v1.2.0
```

Place detailed content in Release Notes.

Formal Release Notes normally include:

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

Selectively include:

```text
Highlights / Major Changes
Deprecations
Breaking Changes / Migration
New Contributors
Assets / Checksums
Upgrade / Programming
Rollback
Security
```

For configured minor/major/formal firmware releases, make `Deprecations` explicit. Write `None` when there are no deprecations.

For any GitHub Release, include explicit `Deprecations` and `New Contributors` headings. If they do not apply, write `None`. Never publish a GitHub Release body that contains only `Summary` or a generated stub.

Derive `New Contributors` from real PR/contributor data. Never invent it.

Generated GitHub notes are a draft source for merged PRs, contributors, and compare links. Curate them and add compatibility, deprecation, migration, known-issue, and firmware information as needed.

## Standardization tools

### Create a repository policy

Copy and fill:

```text
assets/REPOSITORY_GOVERNANCE_TEMPLATE.toml
→ .github/repository-governance.toml
```

### Render selected templates

```bash
python scripts/render_governance_templates.py \
  --config .github/repository-governance.toml \
  --output-dir .
```

The script creates only files enabled by the configuration and refuses to overwrite existing files unless `--force` is supplied.

### Validate Markdown

```bash
python scripts/validate_markdown_links.py README.md CHANGELOG.md
```

### Validate a Release Notes draft

```bash
python scripts/validate_release_notes.py \
  --config .github/repository-governance.toml \
  RELEASE_NOTES.md
```

Scripts do not replace review. They only make selected standards reproducible.

## Safety

Never do these without explicit authorization and a recovery explanation:

```bash
git reset --hard
git clean -fd
git clean -fdx
git push --force
git push --force-with-lease
git branch -D
git tag -d
git push origin --delete <branch>
git push origin :refs/tags/<tag>
git rebase <shared-branch>
git commit --amend
```

Also:

- do not discard user changes;
- do not rewrite shared history;
- do not move a published Tag;
- do not bypass branch protection;
- do not use `git push --tags` as the default;
- do not publish unresolved template placeholders;
- do not invent contributors, tests, compatibility, or release status;
- do not commit private signing keys, credentials, or secrets.

## Completion report

After acting, report actual results:

```text
Git Result
- Profiles selected:
- README created/updated:
- README links validated:
- CHANGELOG updated:
- VERSION updated:
- VERSION RECORD updated:
- Commit created:
- Branch pushed:
- Pull request created:
- Merge completed:
- Back-merge completed:
- Tag created:
- Tag pushed:
- Release Notes created:
- Firmware package updated:
- GitHub Release created:
- Verification performed:
- Remaining work:
```

## Definition of done

Applicable items must be true:

- repository rules and required questions were resolved;
- profiles were selected and recorded;
- only relevant sections and files were created;
- local Markdown links and placeholders were validated;
- CHANGELOG decision was applied;
- Tag and Release remained distinct;
- Release Notes met the selected profile;
- contributor and compare information came from real data;
- only authorized operations were executed;
- blockers and remaining work were reported.
