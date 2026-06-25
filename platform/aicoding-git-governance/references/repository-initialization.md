# Repository Initialization Workflow

Use this reference when creating, standardizing, or binding a Git repository.

## Required baseline

Every initialized repository must define or explicitly defer these files:

```text
README.md
CHANGELOG.md
.gitignore
.github/repository-governance.toml
.githooks/pre-commit
.githooks/commit-msg
scripts/<repo-specific lint command>
```

If a file is deferred, record the reason in the completion report and in the repository governance file when applicable.

## Hook installation

Configure hooks through Git, not through a user's global shell profile:

```bash
git config core.hooksPath .githooks
```

Hook checks must be runnable without waiting for a commit:

```bash
.githooks/pre-commit
.githooks/commit-msg .git/COMMIT_EDITMSG
```

On Windows repositories, provide a hook wrapper that can call PowerShell or another declared project CLI. On cross-platform repositories, prefer a POSIX shell wrapper that delegates to the project lint command.

## Initialization modes

### local-to-empty-remote

Use when local files already exist and the remote repository is empty.

Checklist:

```bash
git init -b main
git remote add origin <remote-url>
git add README.md CHANGELOG.md .gitignore .github .githooks scripts <project-files>
git commit -m "chore(git): initialize repository baseline"
git push -u origin main
```

Before commit, install hooks and run the hook-equivalent lint command.

### remote-first-bind-local

Use when the remote repository was created first, then local files are bound to it.

Checklist:

```bash
git ls-remote <remote-url> refs/heads/main refs/heads/master
git init -b main
git remote add origin <remote-url>
# if remote is non-empty, fetch and integrate before committing
git fetch origin --prune
git status --short --branch
```

If the remote has commits, do not overwrite them. Fetch, inspect, and merge or rebase only with explicit approval.

### clone-existing-remote

Use when the remote already contains the source of truth.

Checklist:

```bash
git clone --recurse-submodules <remote-url> <path>
git -C <path> status --short --branch
git -C <path> submodule update --init --recursive
git -C <path> config core.hooksPath .githooks
```

Run the configured lint command after clone.

### local-only-bootstrap

Use when no remote exists yet.

Checklist:

```bash
git init -b main
git config core.hooksPath .githooks
git add README.md CHANGELOG.md .gitignore .github .githooks scripts <project-files>
git commit -m "chore(git): initialize repository baseline"
```

Record that push is blocked until a remote is selected.

### template-bootstrap

Use when initializing from a company or project template.

Checklist:

```bash
git clone <template-url> <path>
# remove or replace template placeholders before first project commit
git config core.hooksPath .githooks
```

Do not publish unresolved placeholders.

### submodule-aware-bootstrap

Use when the repository contains external source trees that must track their own remotes.

Checklist:

```bash
git submodule add -b <branch> <remote-url> <path>
git submodule status
```

Do not commit an embedded Git repository as an anonymous gitlink. Either convert it to a declared submodule or exclude it from the parent repository.

## Required verification

Before reporting completion:

```bash
git status --short --branch
git remote -v
git submodule status
# repository-specific lint command
git ls-remote <remote-url> refs/heads/main
```

Report the exact initialization mode used, hook path configured, commit created, branch pushed, and any deferred files.