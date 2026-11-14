#!/usr/bin/env python3
"""Dependency-free integrity checks for the static research portal."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import sys

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.lang = False
        self.title = False
        self.description = False
        self.viewport = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "html" and data.get("lang"):
            self.lang = True
        if tag == "title":
            self.title = True
        if tag == "meta" and data.get("name") == "description" and data.get("content"):
            self.description = True
        if tag == "meta" and data.get("name") == "viewport":
            self.viewport = True
        if data.get("id"):
            self.ids.append(data["id"] or "")
        for key in ("href", "src"):
            if data.get(key):
                self.links.append((key, data[key] or ""))


def local_target(source: Path, raw: str) -> tuple[Path, str] | None:
    if raw.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
        return None
    parsed = urlparse(raw)
    path = unquote(parsed.path)
    if not path:
        target = source
    elif path.startswith("/"):
        prefix = "/torus-node/"
        relative = path[len(prefix):] if path.startswith(prefix) else path.lstrip("/")
        target = ROOT / relative
    else:
        target = source.parent / path
    if target.is_dir():
        target = target / "index.html"
    return target.resolve(), parsed.fragment


def main() -> int:
    errors: list[str] = []
    html_files = sorted(ROOT.glob("*.html"))
    parsed: dict[Path, Document] = {}

    expected = {
        "index.html", "research.html", "publications.html", "verification.html",
        "open-problems.html", "community.html", "contribute.html", "about.html", "404.html",
    }
    missing_pages = sorted(expected - {path.name for path in html_files})
    if missing_pages:
        errors.append(f"Missing required pages: {', '.join(missing_pages)}")

    for file in html_files:
        doc = Document()
        try:
            doc.feed(file.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - diagnostic path
            errors.append(f"{file.name}: HTML parse failed: {exc}")
            continue
        parsed[file.resolve()] = doc
        if not doc.lang:
            errors.append(f"{file.name}: missing html[lang]")
        if not doc.title:
            errors.append(f"{file.name}: missing title")
        if not doc.viewport:
            errors.append(f"{file.name}: missing viewport metadata")
        if file.name != "404.html" and not doc.description:
            errors.append(f"{file.name}: missing description metadata")
        duplicates = sorted({item for item in doc.ids if doc.ids.count(item) > 1})
        if duplicates:
            errors.append(f"{file.name}: duplicate ids: {duplicates}")

    for file, doc in parsed.items():
        for attr, raw in doc.links:
            target_info = local_target(file, raw)
            if target_info is None:
                continue
            target, fragment = target_info
            if not target.exists():
                errors.append(f"{file.name}: broken {attr} {raw!r}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_doc = parsed.get(target)
                if target_doc is None:
                    target_doc = Document()
                    target_doc.feed(target.read_text(encoding="utf-8"))
                    parsed[target] = target_doc
                # Dynamic problem-card anchors are declared in problems.js, not source HTML.
                if fragment not in target_doc.ids and target.name != "open-problems.html":
                    errors.append(f"{file.name}: missing fragment {raw!r}")

    required_files = [ROOT / ".nojekyll", ROOT / "robots.txt", ROOT / "sitemap.xml"]
    for required in required_files:
        if not required.exists():
            errors.append(f"Missing deployment file: {required.relative_to(ROOT)}")

    if errors:
        print("SITE CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    local_links = sum(1 for doc in parsed.values() for _, link in doc.links if not link.startswith(("http://", "https://")))
    print(f"SITE CHECK PASSED: {len(html_files)} HTML pages, {local_links} local references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
