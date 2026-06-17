#!/usr/bin/env python3
"""Audit deterministic DOCX typography for supported document profiles."""

from __future__ import annotations

import argparse
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"


@dataclass(frozen=True)
class StyleExpectation:
    aliases: tuple[str, ...]
    east_asia: str
    latin: str
    size_half_points: int
    required: bool = True


PROFILES = {
    "zh_cn_academic_general": {
        "Normal": StyleExpectation(("normal",), "宋体", "Times New Roman", 24),
        "Title": StyleExpectation(("title",), "黑体", "Times New Roman", 36),
        "Heading 1": StyleExpectation(("heading1", "heading 1", "1"), "黑体", "Times New Roman", 28),
        "Heading 2": StyleExpectation(("heading2", "heading 2", "2"), "黑体", "Times New Roman", 24),
        "Heading 3": StyleExpectation(("heading3", "heading 3", "3"), "宋体", "Times New Roman", 24),
        "Caption": StyleExpectation(("caption",), "宋体", "Times New Roman", 21, required=False),
        "Footnote Text": StyleExpectation(
            ("footnotetext", "footnote text"), "宋体", "Times New Roman", 18, required=False
        ),
    }
}


def attr(element: ET.Element | None, name: str) -> str | None:
    if element is None:
        return None
    return element.get(f"{W}{name}")


def normalize(value: str | None) -> str:
    return (value or "").strip().lower()


def load_part(docx: Path, part: str) -> ET.Element:
    with zipfile.ZipFile(docx) as archive:
        try:
            data = archive.read(part)
        except KeyError as exc:
            raise ValueError(f"missing DOCX part: {part}") from exc
    return ET.fromstring(data)


def style_identity(style: ET.Element) -> set[str]:
    identities = {normalize(attr(style, "styleId"))}
    name = style.find(f"{W}name")
    identities.add(normalize(attr(name, "val")))
    return {item for item in identities if item}


def find_style(styles_root: ET.Element, expectation: StyleExpectation) -> ET.Element | None:
    aliases = {normalize(alias) for alias in expectation.aliases}
    for style in styles_root.findall(f"{W}style"):
        if style_identity(style) & aliases:
            return style
    return None


def audit_style(label: str, style: ET.Element, expected: StyleExpectation) -> list[str]:
    errors: list[str] = []
    rpr = style.find(f"{W}rPr")
    rfonts = rpr.find(f"{W}rFonts") if rpr is not None else None
    size = rpr.find(f"{W}sz") if rpr is not None else None

    east_asia = attr(rfonts, "eastAsia")
    ascii_font = attr(rfonts, "ascii")
    hansi_font = attr(rfonts, "hAnsi")
    actual_size = attr(size, "val")

    if east_asia != expected.east_asia:
        errors.append(
            f"{label}: w:eastAsia expected {expected.east_asia!r}, got {east_asia!r}"
        )
    if ascii_font != expected.latin:
        errors.append(f"{label}: w:ascii expected {expected.latin!r}, got {ascii_font!r}")
    if hansi_font != expected.latin:
        errors.append(f"{label}: w:hAnsi expected {expected.latin!r}, got {hansi_font!r}")
    if actual_size != str(expected.size_half_points):
        errors.append(
            f"{label}: w:sz expected {expected.size_half_points} half-points, got {actual_size!r}"
        )

    if rfonts is not None:
        for theme_attr in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
            if attr(rfonts, theme_attr):
                errors.append(f"{label}: theme font {theme_attr} must not override explicit fonts")

    return errors


def audit_direct_fonts(document_root: ET.Element, profile: dict[str, StyleExpectation]) -> list[str]:
    warnings: list[str] = []
    allowed_east_asia = {item.east_asia for item in profile.values()} | {"微软雅黑"}
    allowed_latin = {item.latin for item in profile.values()} | {"Consolas"}
    unexpected: set[str] = set()

    for rfonts in document_root.findall(f".//{W}rFonts"):
        east_asia = attr(rfonts, "eastAsia")
        ascii_font = attr(rfonts, "ascii")
        hansi_font = attr(rfonts, "hAnsi")
        if east_asia and east_asia not in allowed_east_asia:
            unexpected.add(f"eastAsia={east_asia}")
        if ascii_font and ascii_font not in allowed_latin:
            unexpected.add(f"ascii={ascii_font}")
        if hansi_font and hansi_font not in allowed_latin:
            unexpected.add(f"hAnsi={hansi_font}")

    if unexpected:
        warnings.append("unexpected direct font overrides: " + ", ".join(sorted(unexpected)))
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path)
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILES),
        default="zh_cn_academic_general",
    )
    args = parser.parse_args()

    if not args.docx.is_file():
        print(f"ERROR: file not found: {args.docx}", file=sys.stderr)
        return 2

    try:
        styles_root = load_part(args.docx, "word/styles.xml")
        document_root = load_part(args.docx, "word/document.xml")
    except (OSError, zipfile.BadZipFile, ET.ParseError, ValueError) as exc:
        print(f"ERROR: cannot inspect DOCX: {exc}", file=sys.stderr)
        return 2

    profile = PROFILES[args.profile]
    errors: list[str] = []
    for label, expectation in profile.items():
        style = find_style(styles_root, expectation)
        if style is None:
            if expectation.required:
                errors.append(f"{label}: required style not found")
            continue
        errors.extend(audit_style(label, style, expectation))

    warnings = audit_direct_fonts(document_root, profile)

    print(f"Typography profile: {args.profile}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAIL: {len(errors)} typography issue(s)")
        return 1

    print("PASS: required styles use explicit academic fonts and sizes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
