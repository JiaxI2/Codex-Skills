---
name: codex-documents-anthropic-docx
description: Use this bridge whenever the user asks Codex to create, rewrite, polish, or substantially format a DOCX/Word document and typography, font choice, heading hierarchy, spacing, page geometry, tables, table of contents, headers/footers, images, tracked changes, comments, or Word/Google Docs compatibility matter. It tells Codex to use the native Documents skill as the delivery and render-QA authority, while also applying the local anthropic-docx formatting reference.
---

# Codex Documents + Anthropic DOCX Bridge

This is a routing and precedence bridge, not a replacement document builder.

When this skill triggers:

1. Use Codex's native `documents` skill for the main workflow, workspace dependencies, design presets, Google Docs sanitization/import expectations, and render-to-PNG QA.
2. Also read or search `C:\Users\24322\.codex\skills\anthropic-docx\SKILL.md` before implementing layout-sensitive DOCX work.
3. Read this bridge's persistent references `references/typography_standards.md` and, for papers/research documents, `references/academic_paper_standard.md`.
4. Apply Anthropic DOCX formatting guidance for explicit page geometry, professional fonts, built-in heading style IDs, real numbering, DXA table widths, cell padding, TOC-compatible headings, image sizing, comments, tracked changes, and OOXML formatting preservation.
5. For Chinese or bilingual DOCX files, explicitly set Word `w:eastAsia`, `w:ascii`, and `w:hAnsi` fonts in core styles. Do not rely on Word theme-font fallback.
6. For a generic Chinese paper without a supplied template, use the native `academic_paper_general` preset and `zh_cn_academic_general` typography profile.
7. Before render QA, run `python C:\Users\24322\.codex\skills\codex-documents-anthropic-docx\scripts\typography_audit.py output.docx --profile zh_cn_academic_general`.
8. Do not follow Anthropic examples that assume global installs such as `npm install -g docx`; use Codex workspace dependencies and the native Documents skill's bundled helpers.

Conflict order:

1. Explicit user instruction
2. Codex Documents render/QA and Google Docs sanitizer requirements
3. Selected Codex Documents design preset tokens
4. Anthropic DOCX formatting reference
5. Implementation-library examples
