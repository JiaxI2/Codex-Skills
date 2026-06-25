# Profile Catalog

Profiles are selectable defaults, not mandatory identities.

## Branch profiles

### github-flow-lite

- one long-lived stable branch;
- short-lived feature/fix branches;
- PR to stable branch;
- squash or rebase based on commit quality.

### embedded-git-flow-lite

- stable `main`;
- integration `develop`;
- short-lived feature/fix/release/hotfix;
- release and hotfix back-merge.

### environment-promotion

- long-lived environment branches only when real environments exist;
- selective feature promotion;
- preserve commit identity across environments.

### existing-custom

- document and retain a sound existing workflow.

## README profiles

### minimal-internal

Required:

```text
project identity
status
quick start
build
repository navigation
documentation/support links
CHANGELOG/Releases
```

### open-source-firmware

Adds:

```text
why/background
features
supported hardware/toolchain
usage/programming
contributing
maintainers
security
license
```

### firmware-library

Focuses on:

```text
purpose
API/module scope
supported platforms
integration
minimal example
compatibility
documentation
release policy
```

### product-delivery

Focuses on:

```text
product identity
stable version
supported hardware
firmware downloads
programming/upgrade
compatibility
known issues
customer support
```

## CHANGELOG modes

### unreleased

Update `[Unreleased]` during development.

### fragments

Create one change fragment per PR/change and aggregate at release.

### release-only

Curate the changelog in the release workflow.

### generated

Use PR labels or commits to generate a draft; curate before publishing.

## Version schemes

### semver

`MAJOR.MINOR.PATCH`.

### calendar

Date-based versioning.

### product-defined

Existing company/product scheme.

### component-matrix

Multiple independently versioned firmware components.

## Release profiles

### patch

Focus:

```text
fixes
compatibility
known issues
compare link
```

### minor

Focus:

```text
features
deprecations
compatibility
contributors
upgrade notes
```

### major

Focus:

```text
major changes
deprecations
breaking changes
migration
rollback
```

### prerelease

Focus:

```text
preview scope
known limitations
test instructions
feedback links
```

### firmware-minor

Minor profile plus:

```text
hardware compatibility
assets and checksums
programming/upgrade
validation
```

### customer-delivery

Focus:

```text
delivery scope
accepted functions
compatibility
assets/checksums
acceptance status
source traceability
```

### test-baseline

Focus:

```text
baseline purpose
included changes
test environment
assets/checksums
known limitations
source traceability
```

## Artifact storage

### github-release

Preferred for formal generated binaries in public or private GitHub projects.

### git-lfs

Use when binary history must remain repository-addressable.

### git

Use only for small, formal, infrequently changing baselines.

### external

Use when company systems own binary retention and access control.

### none

Source-only repository.
