# {{PROJECT_NAME}}

> {{ONE_LINE_DESCRIPTION}}

{{BADGES}}

{{NAVIGATION_LINKS}}

## {{STATUS_HEADING}}

{{STATUS_CONTENT}}

## {{OVERVIEW_HEADING}}

{{PROJECT_OVERVIEW}}

{{OPTIONAL_SECTIONS}}

## {{QUICK_START_HEADING}}

{{QUICK_START_CONTENT}}

## {{DOCUMENTATION_HEADING}}

{{DOCUMENTATION_LINKS}}

## {{RELEASES_HEADING}}

- [{{LATEST_RELEASE_LABEL}}][latest-release]
- [{{ALL_RELEASES_LABEL}}][releases]
- [{{CHANGELOG_LABEL}}][changelog]

{{FOOTER_SECTIONS}}

[repository]: {{REPOSITORY_URL}}
[documentation]: {{DOCUMENTATION_URL}}
[changelog]: {{CHANGELOG_URL}}
[latest-release]: {{LATEST_RELEASE_URL}}
[releases]: {{RELEASES_URL}}
[issues]: {{ISSUES_URL}}
[contributing]: {{CONTRIBUTING_URL}}
[security]: {{SECURITY_URL}}
[license]: {{LICENSE_URL}}
## Git Governance Standard

All AiCoding-governed Git repositories should document their branch, environment, commit type, and release-note rules here.

- Branches: `main` or `master` is the stable production branch and must not receive direct code edits except approved release or hotfix integration; `develop` is the DEV integration branch; `feature/<scope>` branches start from `develop`; `test` maps to FAT when a shared test environment exists; `release/<version>` maps to UAT/pre-production; `hotfix/<scope>` starts from `main` and is merged back to `main` and `develop`.
- Environments: `DEV` is developer debugging, `FAT` is functional acceptance testing, `UAT` is user acceptance/pre-production, and `PRO` is production.
- Commit types: `feat` adds functionality, `fix` repairs bugs, `docs` changes documentation only, `style` changes formatting without behavior impact, `refactor` restructures code without feature or bug-fix intent, `perf` improves performance, `test` adds or corrects tests, and `chore` changes build/supporting tools or maintenance files.
- Single commits: one commit should contain one category of change, no more than three tightly related topics, and a typed subject such as `feat(scope): summary`.
- Releases: Tag and GitHub Release notes must group every included commit by type, state the primary release type, and describe the concrete user-facing or maintenance impact.
