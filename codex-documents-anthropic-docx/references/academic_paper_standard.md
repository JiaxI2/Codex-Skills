# General Academic Paper Standard

Use this standard for a generic paper or research document when no institution, journal, conference, publisher, or user-supplied template is available. A supplied template always overrides this reference.

## Default Format

- Page: A4 portrait.
- Margins: 2.54 cm on all sides unless binding or submission requirements say otherwise.
- Main text: black on white; no decorative page background, colored body text, or commercial-report styling.
- Body: Chinese 宋体 12 pt, Latin Times New Roman 12 pt, justified, 1.5 line spacing, first-line indent of two Chinese characters, 0 pt before/after.
- Page number: Arabic numerals in the footer, centered or outside-aligned consistently.
- Header: omit unless the user or template requires one.
- Use real Word styles for every structural role.

## Structure

Use the lightest structure appropriate to the paper:

1. Title
2. Author and affiliation, when known
3. Abstract
4. Keywords
5. Main text with numbered headings
6. Acknowledgments, when requested
7. References
8. Appendices, when needed

Do not invent author, institution, funding, citations, DOI, dates, or publication metadata.

## Typography

- Title: 黑体 18 pt, bold, centered.
- Author and affiliation: 宋体 10.5 pt; Latin text Times New Roman 10.5 pt; centered.
- Abstract and keywords: 10.5 pt. Labels such as `摘要` and `关键词` use 黑体; content uses 宋体. English uses Times New Roman.
- Heading 1: 黑体 14 pt, bold.
- Heading 2: 黑体 12 pt, bold.
- Heading 3: 宋体 12 pt, bold.
- Body: 宋体 12 pt; Latin letters, numbers, and formulas use Times New Roman where practical.
- Figure/table captions: 宋体 10.5 pt; Latin text Times New Roman 10.5 pt.
- References: 宋体 10.5 pt; Latin text Times New Roman 10.5 pt.
- Footnotes: 宋体 9 pt; Latin text Times New Roman 9 pt.
- Code, commands, and file paths: Consolas 9 pt for Latin/code glyphs, with 微软雅黑 fallback for Chinese.

Every style that may contain Chinese must explicitly set `w:eastAsia`. Setting only `style.font.name` is a failed implementation.

## Headings And Numbering

- Use real multilevel numbering linked to Heading 1, Heading 2, and Heading 3.
- Default numbering: `1`, `1.1`, `1.1.1`.
- Do not type heading numbers manually.
- Keep headings with the following paragraph.
- Avoid leaving a heading alone at the bottom of a page.
- Do not use colored heading text in the generic academic profile.

## Paragraphs

- Use a two-character first-line indent for normal Chinese prose.
- Abstracts, block quotations, captions, list items, equations, references, and table cells do not inherit the body first-line indent unless appropriate.
- Do not use spaces or tabs to fake paragraph indentation.
- Do not insert blank paragraphs to create vertical spacing; encode spacing in styles.
- Avoid full justification for short labels, headings, captions, references, code, and narrow table cells.

## Figures And Tables

- Number figures and tables sequentially using fields or deterministic numbering.
- Put figure captions below figures.
- Put table titles above tables.
- Keep captions with their figure or table.
- Refer to every figure and table from the text when the content supports it.
- Use restrained table borders. Avoid colored fills unless the paper requires them.
- Use explicit DXA widths, readable cell padding, repeating header rows, and no fixed row heights that can clip text.
- Do not shrink table text below 9 pt to force content onto one page; redesign the table or use landscape orientation.

## Equations

- Center displayed equations.
- Place equation numbers at the right margin when numbering is needed.
- Keep the equation and its number on the same line.
- Define symbols in the surrounding text unless they are standard and obvious in context.

## Citations And References

- Never fabricate references.
- Preserve the citation style already used by the source document.
- If the user does not specify a style, use a consistent numeric citation form such as `[1]`, `[2]`, and format the reference list in citation order.
- Use real hanging indents for references; do not align references with spaces.
- Keep DOI and URL text as working hyperlinks when supplied.
- Do not silently convert between citation systems.

## Headers, Footers, And Pagination

- Use one consistent page-number style throughout the main text.
- Do not add decorative footer rules or document titles in headers unless requested.
- If front matter uses different numbering, implement separate sections with correct page-number restarts.

## Academic QA Gate

Before final delivery, verify:

- A4 page geometry and margins are explicit.
- Chinese styles contain the expected `w:eastAsia` font.
- Latin text does not randomly fall back to Calibri or another theme font.
- Title, abstract, keywords, body, headings, captions, references, and footnotes use their assigned style.
- Body paragraphs use real first-line indentation and correct line spacing.
- Heading numbering is automatic and TOC-compatible.
- Captions are positioned correctly and stay with their figures/tables.
- Reference indentation and numbering are consistent.
- No invented citations or publication metadata appear.
- Rendered pages show no fallback-font mismatch, clipped glyphs, isolated headings, cramped tables, or excessive blank space.
