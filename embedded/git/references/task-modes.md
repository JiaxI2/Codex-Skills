# Task Modes

## inspect

Read-only. Report repository state, policy gaps, active profiles, and next steps.

## quick-ref

Read only the requested policy and template.

Examples:

```text
ref readme open-source-firmware
ref changelog unreleased
ref release firmware-minor
ref branch environment-promotion
ref tag
ref links
```

Return:

- when to use it;
- required and optional elements;
- minimal checklist;
- asset/reference path;
- application command.

Do not modify files unless the user says to apply it.

## standardize

1. Run the decision questionnaire.
2. Select profiles.
3. Create/update `.github/repository-governance.toml`.
4. Render only enabled templates.
5. Preserve accurate existing content.
6. Validate links and placeholders.
7. Show diff and migration impact before commit.

## commit

1. Inspect all changes.
2. Split unrelated logic.
3. Decide README impact.
4. Decide CHANGELOG impact.
5. Stage only selected files.
6. Validate changed Markdown.
7. Review staged diff.
8. Commit only when authorized.
9. Do not create a Tag for a normal commit.

## push

Confirm remote/upstream and push only the intended branch. No automatic merge, Tag, or Release.

## pull-request

Confirm source/target and selected profiles. Include documentation, changelog, release impact, verification, and rollback information.

## merge

Confirm checks, reviews, merge method, environment meaning, and required back-merge.

## release

1. Identify stable commit and previous Tag.
2. Select release profile.
3. Finalize CHANGELOG/version records.
4. Render/curate Release Notes.
5. Validate required headings, compare URL, links, assets, and contributors.
6. Update README stable/latest release references if policy requires it.
7. Verify artifacts and checksums.
8. Create release commit if needed.
9. Merge to stable branch.
10. Create annotated/signed Tag according to policy.
11. Push only the intended Tag.
12. Create GitHub Release and upload assets.
13. Complete back-merge.

## hotfix

Branch from the production baseline, update released-behavior notes, create a new patch baseline, and back-merge. Never move the old Tag.

## firmware-package

Require version, Tag, commit, target, configuration, checksums, compatibility, and validation. Avoid untraceable `final.bin` files.
