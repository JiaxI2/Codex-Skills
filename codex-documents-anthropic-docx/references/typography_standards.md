# Typography Standards

Use this reference for DOCX/Word documents whenever font quality matters, especially for Chinese or bilingual deliverables. The goal is deterministic Word output, not approximate visual polish.

## Profile Selection

Pick exactly one typography profile before drafting. Encode it in Word styles, not scattered direct formatting.

### `zh_cn_academic_general`

Use as the default for Chinese papers, research reports, course papers, literature reviews, technical papers, and thesis-like documents when the user does not provide a university, journal, conference, or publisher template.

```yaml
profile: zh_cn_academic_general
language: zh-CN
page:
  size: A4
  margins: 2.54cm
body:
  east_asia_font: 宋体
  latin_font: Times New Roman
  size: 12pt
  alignment: justified
  first_line_indent: 2ch
  line_spacing: 1.5
  before: 0pt
  after: 0pt
title:
  east_asia_font: 黑体
  latin_font: Times New Roman
  size: 18pt
  weight: bold
  alignment: center
  before: 0pt
  after: 12pt
author_and_affiliation:
  east_asia_font: 宋体
  latin_font: Times New Roman
  size: 10.5pt
  alignment: center
abstract:
  label_east_asia_font: 黑体
  body_east_asia_font: 宋体
  latin_font: Times New Roman
  size: 10.5pt
  line_spacing: 1.25
keywords:
  label_east_asia_font: 黑体
  body_east_asia_font: 宋体
  latin_font: Times New Roman
  size: 10.5pt
heading_1:
  east_asia_font: 黑体
  latin_font: Times New Roman
  size: 14pt
  weight: bold
  before: 12pt
  after: 6pt
heading_2:
  east_asia_font: 黑体
  latin_font: Times New Roman
  size: 12pt
  weight: bold
  before: 10pt
  after: 4pt
heading_3:
  east_asia_font: 宋体
  latin_font: Times New Roman
  size: 12pt
  weight: bold
  before: 8pt
  after: 3pt
table:
  east_asia_font: 宋体
  latin_font: Times New Roman
  body_size: 10.5pt
  header_size: 10.5pt
  header_weight: bold
caption:
  east_asia_font: 宋体
  latin_font: Times New Roman
  size: 10.5pt
  alignment: center
references:
  east_asia_font: 宋体
  latin_font: Times New Roman
  size: 10.5pt
  line_spacing: 1.0
  hanging_indent: 2ch
footnotes:
  east_asia_font: 宋体
  latin_font: Times New Roman
  size: 9pt
header_footer:
  east_asia_font: 宋体
  latin_font: Times New Roman
  size: 9pt
code_or_paths:
  east_asia_font: 微软雅黑
  latin_font: Consolas
  size: 9pt
```

For this profile, use black text on a white background, avoid decorative cover treatments and colored headings, and follow `academic_paper_standard.md` for document structure and caption/reference rules.

### `zh_cn_formal`

Use for Chinese formal reports, memos, proposals, notices, SOPs, contracts, and business documents.

```yaml
profile: zh_cn_formal
language: zh-CN
body:
  east_asia_font: SimSun
  latin_font: Times New Roman
  size: 12pt
  line_spacing: 1.5
  after: 0pt
title:
  east_asia_font: Microsoft YaHei
  latin_font: Arial
  size: 22pt
  weight: bold
heading_1:
  east_asia_font: SimHei
  latin_font: Arial
  size: 16pt
  weight: bold
  before: 12pt
  after: 6pt
heading_2:
  east_asia_font: SimHei
  latin_font: Arial
  size: 14pt
  weight: bold
  before: 10pt
  after: 4pt
heading_3:
  east_asia_font: SimHei
  latin_font: Arial
  size: 12pt
  weight: bold
  before: 8pt
  after: 3pt
table:
  east_asia_font: SimSun
  latin_font: Arial
  body_size: 10.5pt
  header_size: 10.5pt
  header_weight: bold
caption:
  east_asia_font: SimSun
  latin_font: Arial
  size: 10pt
header_footer:
  east_asia_font: SimSun
  latin_font: Arial
  size: 9pt
code_or_paths:
  east_asia_font: Microsoft YaHei UI
  latin_font: Consolas
  size: 9.5pt
```

### `zh_cn_modern_business`

Use for polished Chinese business briefs, product docs, strategy notes, and modern internal documents where readability is more important than traditional Songti formality.

```yaml
profile: zh_cn_modern_business
language: zh-CN
body:
  east_asia_font: Microsoft YaHei
  latin_font: Arial
  size: 10.5pt
  line_spacing: 1.25
  after: 6pt
title:
  east_asia_font: Microsoft YaHei
  latin_font: Arial
  size: 24pt
  weight: bold
heading_1:
  east_asia_font: Microsoft YaHei
  latin_font: Arial
  size: 16pt
  weight: bold
  before: 14pt
  after: 7pt
heading_2:
  east_asia_font: Microsoft YaHei
  latin_font: Arial
  size: 13pt
  weight: bold
  before: 10pt
  after: 5pt
heading_3:
  east_asia_font: Microsoft YaHei
  latin_font: Arial
  size: 11.5pt
  weight: bold
  before: 8pt
  after: 4pt
table:
  east_asia_font: Microsoft YaHei
  latin_font: Arial
  body_size: 9.5pt
  header_size: 9.5pt
  header_weight: bold
caption:
  east_asia_font: Microsoft YaHei
  latin_font: Arial
  size: 9pt
header_footer:
  east_asia_font: Microsoft YaHei
  latin_font: Arial
  size: 8.5pt
code_or_paths:
  east_asia_font: Microsoft YaHei UI
  latin_font: Consolas
  size: 9pt
```

### `en_business`

Use for English-only business documents.

```yaml
profile: en_business
language: en-US
body:
  latin_font: Aptos
  fallback_latin_font: Arial
  size: 11pt
  line_spacing: 1.10
  after: 6pt
title:
  latin_font: Aptos Display
  fallback_latin_font: Arial
  size: 24pt
  weight: bold
heading_1:
  latin_font: Aptos Display
  fallback_latin_font: Arial
  size: 16pt
  weight: bold
  before: 14pt
  after: 7pt
heading_2:
  latin_font: Aptos
  fallback_latin_font: Arial
  size: 13pt
  weight: bold
  before: 10pt
  after: 5pt
heading_3:
  latin_font: Aptos
  fallback_latin_font: Arial
  size: 11.5pt
  weight: bold
  before: 8pt
  after: 4pt
table:
  latin_font: Aptos
  fallback_latin_font: Arial
  body_size: 9.5pt
  header_size: 9.5pt
  header_weight: bold
caption:
  latin_font: Aptos
  fallback_latin_font: Arial
  size: 9pt
header_footer:
  latin_font: Aptos
  fallback_latin_font: Arial
  size: 8.5pt
code_or_paths:
  latin_font: Consolas
  size: 9pt
```

### `google_docs_native`

Use for Google Docs-targeted documents unless the user asks for a different visual system.

```yaml
profile: google_docs_native
language: multilingual
body:
  latin_font: Arial
  east_asia_font: Arial
  size: 11pt
  line_spacing: 1.15
  after: 8pt
title:
  latin_font: Arial
  east_asia_font: Arial
  size: 26pt
  weight: normal
heading_1: {latin_font: Arial, east_asia_font: Arial, size: 20pt, weight: normal}
heading_2: {latin_font: Arial, east_asia_font: Arial, size: 16pt, weight: normal}
heading_3: {latin_font: Arial, east_asia_font: Arial, size: 14pt, weight: normal}
table:
  latin_font: Arial
  east_asia_font: Arial
  body_size: 10pt
  header_size: 10pt
caption:
  latin_font: Arial
  east_asia_font: Arial
  size: 9pt
header_footer:
  latin_font: Arial
  east_asia_font: Arial
  size: 9pt
```

## Implementation Rules

- Never leave fonts to Word defaults. Every core style must explicitly set both Latin and East Asian fonts when Chinese text may appear.
- In `python-docx`, setting `style.font.name` is not enough for Chinese. Also patch `w:rFonts` with `w:eastAsia`, plus `w:ascii` and `w:hAnsi` for Latin text.
- Do not mix SimSun, Microsoft YaHei, Calibri, Arial, and Aptos randomly in one document. Choose one profile and keep it stable.
- Do not use Calibri for Chinese body text. It does not control Chinese glyphs and often falls back inconsistently.
- For Chinese formal documents, prefer SimSun body text and SimHei or Microsoft YaHei headings. For modern business documents, prefer Microsoft YaHei for both body and headings.
- Tables may use slightly smaller type than body text, but never below 9 pt for user-facing deliverables unless the user explicitly requests a dense technical appendix.
- Header/footer text should be smaller than body text but still readable after PDF export.
- For mixed Chinese and English runs, do not split every word into manual direct formatting. Set the style's East Asian and Latin fonts correctly, then use direct formatting only for semantic exceptions.
- For render QA, fail the typography audit if Chinese text appears in an unintended fallback font, if headings use body fonts without hierarchy, or if table text is visibly cramped.

## Python DOCX Helper Pattern

Use this helper pattern or equivalent OOXML patching when creating styles with `python-docx`:

```python
from docx.oxml.ns import qn

def _set_rpr_fonts(rpr, latin=None, east_asia=None):
    rfonts = rpr.get_or_add_rFonts()
    for theme_attr in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
        rfonts.attrib.pop(qn(f"w:{theme_attr}"), None)
    if latin:
        rfonts.set(qn("w:ascii"), latin)
        rfonts.set(qn("w:hAnsi"), latin)
    if east_asia:
        rfonts.set(qn("w:eastAsia"), east_asia)

def set_style_fonts(style, latin=None, east_asia=None):
    _set_rpr_fonts(style.element.get_or_add_rPr(), latin, east_asia)

def set_run_fonts(run, latin=None, east_asia=None):
    _set_rpr_fonts(run._element.get_or_add_rPr(), latin, east_asia)
```

Apply `set_style_fonts(...)` to `document.styles["Normal"]`, `Heading 1`, `Heading 2`, table styles, caption styles, header/footer paragraph styles, and any custom callout styles. Use `set_run_fonts(...)` only for deliberate direct-formatting exceptions.
