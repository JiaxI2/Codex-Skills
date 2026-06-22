# Branch Policy

## github-flow-lite

Use when one stable branch is continuously releasable.

```text
feature/fix → PR → main
```

## embedded-git-flow-lite

Use when stable delivery and next-version development run in parallel.

```text
feature/fix → develop
develop → release/<version> → main
hotfix → main
release/hotfix → back-merge to develop
```

## environment-promotion

Use only when branches correspond to real environments.

```text
dev → DEV
test → FAT/QA
release → UAT/PRE
main → PROD
```

Promote selected topic branches. Avoid releasing the whole `dev` branch when it contains delayed work.

Preserve commit identity when the same feature moves through multiple environment branches; repeated independent squash merges create avoidable conflicts.

## existing-custom

Document:

- branch purposes;
- allowed source and targets;
- merge methods;
- protection;
- Tag branch;
- back-merge rules.

Retain the model if it is clear and safe.
