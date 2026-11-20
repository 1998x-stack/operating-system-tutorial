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

    # Validate chapter evidence ledgers introduced in the technical review batches.
    for number in range(1, 15):
        chapter_id = f"{number:02d}"
        evidence_path = ROOT / "evidence" / f"{chapter_id}.json"
        check(evidence_path.exists(), f"missing evidence ledger: {chapter_id}.json")
        if evidence_path.exists():
            try:
                ledger = json.loads(evidence_path.read_text(encoding="utf-8"))
                check(ledger.get("chapter") == chapter_id, f"{chapter_id}.json: chapter id mismatch")
                claims = ledger.get("claims", [])
                check(bool(claims), f"{chapter_id}.json: no claims recorded")
                for claim in claims:
                    check(claim.get("status") in {"verified", "derived", "illustrative", "unverified"},
                          f"{chapter_id}.json: invalid evidence status")
                    check(str(claim.get("source_url", "")).startswith("https://"),
                          f"{chapter_id}.json: claim needs an HTTPS source")
                    check(bool(claim.get("locator")), f"{chapter_id}.json: claim needs a source locator")
                    check(bool(claim.get("claim")), f"{chapter_id}.json: empty claim")
            except (json.JSONDecodeError, OSError) as exc:
                errors.append(f"{chapter_id}.json: cannot parse evidence ledger ({exc})")

    for relative in [
        "evidence/README.md",
        "docs/reviews/chapters-01-07.md",
        "docs/reviews/chapters-08-14.md",
        "labs/ch04-syscall/hello.c",
        "labs/ch04-syscall/README.md",
        "labs/ch06-hello-module/hello.c",
        "labs/ch06-hello-module/Makefile",
        "labs/ch06-hello-module/README.md",
        "labs/ch07-qemu/README.md",
        "labs/ch07-xv6/README.md",
        "labs/ch08-process/cow.c",
        "labs/ch08-process/exec_demo.c",
        "labs/ch08-process/README.md",
        "labs/ch09-threads/counter.c",
        "labs/ch09-threads/Makefile",
        "labs/ch09-threads/README.md",
        "labs/ch10-scheduler/observe.sh",
        "labs/ch10-scheduler/README.md",
        "labs/ch11-sync/counter.c",
        "labs/ch11-sync/Makefile",
        "labs/ch11-sync/README.md",
        "labs/ch12-vm/cow_mmap.c",
        "labs/ch12-vm/README.md",
        "labs/ch13-memory/inspect.sh",
        "labs/ch13-memory/README.md",
        "labs/ch14-filesystem/durable_replace.c",
        "labs/ch14-filesystem/README.md",
    ]:
        check((ROOT / relative).exists(), f"missing reviewed resource: {relative}")

    # Each reviewed chapter must link its evidence ledger.
    for number in range(1, 15):
        chapter_id = f"{number:02d}"
        page = ROOT / f"{chapter_id}.html"
        if page.exists():
            html = page.read_text(encoding="utf-8")
            check(f'href="evidence/{chapter_id}.json"' in html,
                  f"{chapter_id}.html: missing evidence link")

    if errors:
        print(f"FAILED ({len(errors)} problems):")
        for item in errors:
            print(" -", item)
        return 1
    print(f"PASS: {len(chapters)} chapters, {len(pages)} pages, navigation and local assets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
