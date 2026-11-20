#!/usr/bin/env python3
"""Validate course pages, local navigation, evidence ledgers and lab reproducibility."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.refs: list[tuple[str, str]] = []
        self.counts: Counter[str] = Counter()
        self.img_alts: list[str | None] = []
        self.headings: list[int] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        self.counts[tag] += 1
        element_id = attrs_dict.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)
        if tag == "img":
            self.img_alts.append(attrs_dict.get("alt"))
        if tag in {f"h{i}" for i in range(1, 7)}:
            self.headings.append(int(tag[1]))
        for key in ("href", "src"):
            if attrs_dict.get(key):
                self.refs.append((key, attrs_dict[key] or ""))


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def parse_page(path: Path) -> PageParser:
    source = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(source)
    parser.close()
    check(parser.counts["h1"] == 1, f"{path.name}: expected exactly one H1")
    check(parser.counts["main"] == 1, f"{path.name}: expected exactly one main")
    check('lang="zh-CN"' in source, f"{path.name}: missing lang=zh-CN")
          f"{path.name}: missing lang=zh-CN")
    check(all(alt and alt.strip() for alt in parser.img_alts),
          f"{path.name}: image needs descriptive alt")
    check(not parser.duplicate_ids,
          f"{path.name}: duplicate ids: {', '.join(sorted(parser.duplicate_ids))}")
    check("javascript:void(0)" not in source, f"{path.name}: placeholder JavaScript link")
    check("class=\\"page-toc\\"" in source or path.name == "index.html",
          f"{path.name}: missing page section navigation")
    return parser


def main() -> int:
    meta = json.loads((ROOT / "courses.json").read_text(encoding="utf-8"))
    chapters = meta["chapters"]
    check(len(chapters) == 28 and meta["chapterCount"] == 28,
          "courses.json: expected 28 chapters")
    check([c["num"] for c in chapters] == [f"{i:02d}" for i in range(1, 29)],
          "courses.json: chapter order mismatch")

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
            target_path = unquote(url.path)
            target = (file.parent / target_path).resolve() if target_path else file
            check(target.exists(), f"{file.name}: broken {key} target {ref}")
            if url.fragment and target.suffix.lower() == ".html" and target in pages:
                check(unquote(url.fragment) in pages[target].ids,
                      f"{file.name}: missing fragment {ref}")

    index_text = (ROOT / "index.html").read_text(encoding="utf-8")
    for i, course in enumerate(chapters):
        filename = course["file"]
        chapter_path = ROOT / filename
        check(re.search(rf'href=["\\']{re.escape(filename)}["\\']', index_text) is not None,
              f"index.html: missing {filename}")
        if not chapter_path.exists():
            continue
        source = chapter_path.read_text(encoding="utf-8")
        check('aria-current="page"' in source, f"{filename}: missing current chapter marker")
        previous = chapters[i - 1]["file"] if i else None
        following = chapters[i + 1]["file"] if i < len(chapters) - 1 else None
        if previous:
            check(f'href="{previous}"' in source, f"{filename}: missing previous chapter")
        if following:
            check(f'href="{following}"' in source, f"{filename}: missing next chapter")

    for svg_path in sorted((ROOT / "assets" / "diagrams").glob("*.svg")):
        svg = svg_path.read_text(encoding="utf-8")
        check("<title" in svg and "<desc" in svg and "viewBox" in svg,
              f"{svg_path.name}: accessible SVG metadata missing")

    for number in range(1, 29):
        chapter_id = f"{number:02d}"
        evidence_path = ROOT / "evidence" / f"{chapter_id}.json"
        check(evidence_path.exists(), f"missing evidence ledger: {chapter_id}.json")
        if not evidence_path.exists():
            continue
        try:
            ledger = json.loads(evidence_path.read_text(encoding="utf-8"))
            check(ledger.get("chapter") == chapter_id,
                  f"{chapter_id}.json: chapter id mismatch")
            claims = ledger.get("claims", [])
            check(bool(claims), f"{chapter_id}.json: no claims recorded")
            for claim in claims:
                check(claim.get("status") in {"verified", "derived", "illustrative", "unverified"},
                      f"{chapter_id}.json: invalid evidence status")
                check(str(claim.get("source_url", "")).startswith("https://"),
                      f"{chapter_id}.json: claim needs an HTTPS source")
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"{chapter_id}.json: cannot parse evidence ledger ({exc})")

    required_files = [
        "evidence/README.md",
        "docs/reviews/chapters-01-07.md",
        "docs/reviews/chapters-08-14.md",
        "docs/reviews/chapters-15-21.md",
        "docs/reviews/chapters-22-28.md",
        "docs/guides/experiment-standard.md",
        "labs/EXPERIMENT_TEMPLATE.md",
        "labs/ch04-syscall/hello.c",
        "labs/ch04-syscall/README.md",
        "labs/ch06-hello-module/hello.c",
        "labs/ch06-hello-module/Makefile",
        "labs/ch06-hello-module/README.md",
        "labs/ch07-qemu/README.md",
        "labs/ch07-xv6/README.md",
        "tests/site.spec.mjs",
    ]
    for relative in required_files:
        check((ROOT / relative).exists(), f"missing reviewed resource: {relative}")

    for relative in [
        "labs/ch04-syscall/README.md",
        "labs/ch06-hello-module/README.md",
        "labs/ch07-qemu/README.md",
        "labs/ch07-xv6/README.md",
    ]:
        path = ROOT / relative
        if path.exists():
            text = path.read_text(encoding="utf-8")
            for heading in ("## 环境", "## 预期结果", "## 清理"):
                check(heading in text, f"{relative}: missing section {heading}")

    if errors:
        print(f"FAILED ({len(errors)} problems):")
        for item in errors:
            print(" -", item)
        return 1
    print(f"PASS: {len(chapters)} chapters, {len(pages)} pages, evidence ledgers and reproducible labs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
