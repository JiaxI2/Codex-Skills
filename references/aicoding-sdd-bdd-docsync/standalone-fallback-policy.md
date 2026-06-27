# Standalone Fallback Policy

AiCoding skills must not depend on Superpowers for correctness.

## Required behavior

- If Superpowers is installed, compatible skills may be reused.
- If Superpowers is missing, use AiCoding local skills and references.
- If no external TDD skill exists, use `aicoding-tdd-fallback`.
- If no external planning skill exists, use `aicoding-sdd-spec-driven-development` and `aicoding-mvp-planning`.
- If no external review skill exists, use the gate checklist in the top-level flow skill.

## Reporting

Every implementation report must state:

- execution mode;
- external skills used;
- local fallback skills used;
- verification completed;
- docs synchronization result.
