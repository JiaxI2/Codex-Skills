# Evaluation Cases

## Quick Ref

Prompt:

```text
ref release firmware-minor
```

Expected:

- read-only;
- load release profile and template only;
- show required/optional sections and validation command;
- no repository edits.

## Standardize public firmware repository

Expected:

- ask/resolve audience, language, release consumers, artifacts, and version scheme;
- select composable profiles;
- create configuration only when authorized;
- render relevant templates;
- validate links and placeholders.

## Ordinary commit

Expected:

- evaluate README and CHANGELOG;
- no version, Tag, or Release;
- commit only if authorized.

## Linux-style repository

Expected:

- retain existing concise area-prefixed commit style;
- do not force Conventional Commits;
- retain existing release and branch process.

## GitHub-generated Release

Expected:

- use generated PR, contributor, and compare data as a draft;
- add project-specific compatibility/deprecation/known-issue/artifact content;
- never invent New Contributors.

## Minor firmware Release

Expected:

- explicit Deprecations section;
- What's Changed with PR links;
- Release Notes and exact compare link;
- hardware compatibility and checksums;
- Tag and Release treated separately.

## Internal private repository

Expected:

- choose minimal-internal README;
- omit irrelevant public badges/community sections;
- retain internal support and delivery links.

## Missing configuration

Expected:

- infer existing practice;
- propose configuration;
- do not silently add every template.
