#!/usr/bin/env python3
"""Validate local course navigation and HTML structure with Python stdlib only."""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.refs: list[tuple[str, str]] = []
        self.counts: dict[str, int] = {}
        self.img_alts: list[str | None] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        self.counts[tag] = self.counts.get(tag, 0) + 1
        if attrs_dict.get("id"):
            self.ids.add(attrs_dict["id"] or "")
        if tag == "img":
            self.img_alts.append(attrs_dict.get("alt"))
        for key in ("href", "src"):
            if attrs_dict.get(key):
                self.refs.append((key, attrs_dict[key] or ""))


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def parse_page(path: Path) -> PageParser:
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    check(parser.counts.get("h1", 0) == 1, f"{path.name}: expected exactly one H1")
    check(parser.counts.get("main", 0) == 1, f"{path.name}: expected exactly one main")
    check(bool(re.search(r"<html\b[^>]*lang=[\"']zh-CN[\"']", text)), f"{path.name}: missing lang=zh-CN")
    check(all(alt and alt.strip() for alt in parser.img_alts), f"{path.name}: image needs descriptive alt")
    check("javascript:void(0)" not in text, f"{path.name}: placeholder JavaScript link")
    return parser


def main() -> int:
    meta = json.loads((ROOT / "courses.json").read_text(encoding="utf-8"))
    chapters = meta["chapters"]
    check(len(chapters) == 28 and meta["chapterCount"] == 28, "courses.json: expected 28 chapters")
    ids = [c["num"] for c in chapters]
    check(ids == [f"{i:02d}" for i in range(1, 29)], "courses.json: chapter order mismatch")

    html_files = [ROOT / "index.html"] + [ROOT / c["file"] for c in chapters]
    pages: dict[Path, PageParser] = {}
    for file in html_files:
        check(file.exists(), f"missing page: {file.name}")
        if file.exists():
            pages[file.resolve()] = parse_page(file)

    for file, page in pages.items():
        for key, ref in page.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc or ref.startswith("//"):
                continue
            if ref.startswith("javascript:"):
                errors.append(f"{file.name}: unsafe link {ref}")
                continue
            dest = unquote(url.path)
            target = (file.parent / dest).resolve() if dest else file
            check(target.exists(), f"{file.name}: broken {key} target {ref}")
            if url.fragment and target.suffix.lower() == ".html" and target in pages:
                check(unquote(url.fragment) in pages[target].ids, f"{file.name}: missing fragment {ref}")

    index_text = (ROOT / "index.html").read_text(encoding="utf-8")
    for i, course in enumerate(chapters):
        file = course["file"]
        chapter_text = (ROOT / file).read_text(encoding="utf-8")
        check(re.search(rf'href="{re.escape(file)}"', index_text) is not None, f"index.html: missing {file}")
        check(f'aria-current="page"' in chapter_text, f"{file}: missing current chapter marker")
        previous = chapters[i - 1]["file"] if i > 0 else None
        following = chapters[i + 1]["file"] if i < len(chapters) - 1 else None
        if previous:
            check(f'href="{previous}"' in chapter_text, f"{file}: missing previous chapter")
        if following:
            check(f'href="{following}"' in chapter_text, f"{file}: missing next chapter")
        check("class=\"page-toc\"" in chapter_text, f"{file}: missing on-page section navigation")

    for path in sorted((ROOT / "assets" / "diagrams").glob("*.svg")):
        svg = path.read_text(encoding="utf-8")
        check("<title" in svg and "<desc" in svg and "viewBox" in svg, f"{path.name}: accessible SVG metadata missing")

    if errors:
        print(f"FAILED ({len(errors)} problems):")
        for item in errors:
            print(" -", item)
        return 1
    print(f"PASS: {len(chapters)} chapters, {len(pages)} pages, navigation and local assets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
