# Git, documentation, and release governance

- Invoke `$embedded-git-workflow` before changing branches, commits, pushes, Pull Requests, merges,
  README, CHANGELOG, versions, Tags, GitHub Releases, firmware packages, or delivery baselines.
- Use `.github/repository-governance.toml` when present; do not force every available profile.
- Treat edit, stage, commit, branch push, PR creation, merge, Tag creation, Tag push, Release
  creation, and asset upload as separate permissions.
- Every commit task reports README, CHANGELOG, VERSION, TAG, and Release decisions.
- Every formal release validates selected Release Notes sections and required back-merges.
- Never publish unresolved `{{PLACEHOLDER}}` values or invented contributor/test information.
