# Firmware Artifact Policy

## When enabled

Use for formal releases, customer deliveries, production programming, test baselines, or multiple hardware variants.

## Storage choices

### github-release

Preferred for generated formal binaries and checksums.

### git-lfs

Use when versioned binary history must be repository-addressable.

### git

Use only for small, formal, infrequently changing artifacts.

### external

Use company artifact storage when access control or retention requires it.

## Traceability

Each formal artifact records:

```text
product
target
hardware revision
version
Tag
commit
configuration
toolchain
SHA-256
compatibility
validation
```

## Naming

```text
<product>-<target>-<version>-<configuration>.<ext>
```

Avoid:

```text
final.bin
latest.bin
new.bin
final_v2.bin
```

## Suggested metadata tree

```text
firmware/
├── README.md
└── releases/
    └── <version>/
        ├── README.md
        ├── manifest.json
        └── SHA256SUMS
```

Generated binaries may remain only in GitHub Release assets.

Never archive private signing keys.
