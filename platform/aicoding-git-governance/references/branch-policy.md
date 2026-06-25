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

## factory-style branch names

Use this model when the repository follows a factory-style development, test, prerelease, and production flow.

| Branch | Purpose | Environment | Directly accessible |
|---|---|---|---|
| `main` or legacy `master` | stable production baseline | `PRO` | yes |
| `develop` | integration branch with latest accepted development | `DEV` | yes |
| `feature/<scope>` | isolated feature work branched from `develop` | none | no |
| `test` or `test/<scope>` | functional acceptance test baseline | `FAT` or `QA` | yes |
| `release/<version>` | prerelease and user acceptance baseline | `UAT` or `PRE` | yes |
| `hotfix/<scope>` | urgent production fix branched from `main` | none until merged | no |

Rules:

- prefer `main` for new repositories; keep `master` only for existing repositories that already use it;
- create `feature/*` from `develop` and merge back through review;
- do not commit normal feature work directly to `release/*` or `main`;
- create `hotfix/*` from the production baseline, then merge the fix back to `main` and `develop`;
- keep branch names lowercase and descriptive, for example `feature/user-module` or `hotfix/login-timeout`;
- use environment branches only when they map to real deployment or test environments.

## existing-custom

Document:

- branch purposes;
- allowed source and targets;
- merge methods;
- protection;
- Tag branch;
- back-merge rules.

Retain the model if it is clear and safe.
