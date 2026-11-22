#!/usr/bin/env python3
"""Render the public Updates page and Atom feed from the versioned research registry."""
from __future__ import annotations

from datetime import date, datetime, timezone
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets/data/research-records.json"
UPDATES = ROOT / "updates.html"
FEED = ROOT / "feed.xml"
BASE = "https://s6ygleee.github.io/torus-node/"


def parse_value(value: str) -> date | datetime:
    if "T" in value:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    return date.fromisoformat(value)


def sort_key(record: dict) -> tuple:
    value = parse_value(record["published_at"])
    return (value.year, value.month, value.day, getattr(value, "hour", 0), getattr(value, "minute", 0), getattr(value, "second", 0))


def display_time(value: str) -> str:
    parsed = parse_value(value)
    if isinstance(parsed, datetime):
        return f"{parsed.day} {parsed.strftime('%B %Y')}, {parsed.strftime('%H:%M')} UTC"
    return f"{parsed.day} {parsed.strftime('%B %Y')}"


def time_tag(value: str) -> str:
    return f'<time datetime="{html.escape(value, quote=True)}">{html.escape(display_time(value))}</time>'


def record_card(series: dict, record: dict) -> str:
    title = html.escape(series["title"])
    version = html.escape(record["version"])
    venue = html.escape(record["venue"])
    status = html.escape(record["status"])
    if series["record_type"] == "Scholarly preprint":
        label = f"Preprint · v{version}"
        note = "Not peer reviewed." if not record.get("peer_reviewed") else "Peer reviewed."
    else:
        label = f"Software · v{version}"
        note = "Immutable citable release."
    return (
        f'          <article class="card"><span class="tag established">{label}</span>'
        f'<h3>{title}</h3><p>{time_tag(record["published_at"])} · {venue} · {status}.</p>'
        f'<p>{note}</p><p><a href="{html.escape(record["url"], quote=True)}">Open the primary record</a></p></article>'
    )


def render_page(registry: dict) -> None:
    records = []
    for series in registry["series"]:
        for record in series["versions"]:
            records.append((series, record))
    records.sort(key=lambda item: sort_key(item[1]), reverse=True)
    cards = chr(10).join(record_card(series, record) for series, record in records)
    text = UPDATES.read_text(encoding="utf-8")
    pattern = r"<!-- AUTO:UPDATES_RECORDS:START -->.*?<!-- AUTO:UPDATES_RECORDS:END -->"
    replacement = "<!-- AUTO:UPDATES_RECORDS:START -->" + chr(10) + cards + chr(10) + "<!-- AUTO:UPDATES_RECORDS:END -->"
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("Updates record marker not found")
    UPDATES.write_text(text, encoding="utf-8")


def feed_entry(series: dict, record: dict, generated: str) -> str:
    title = f'{series["title"]} — version {record["version"]}'
    published = record["published_at"]
    if "T" in published:
        updated = published
        precision_note = ""
    else:
        updated = generated
        precision_note = " The source record provides a calendar date but no publication time."
    summary = f'{record["venue"]}; published {display_time(published)}. Status: {record["status"]}.{precision_note}'
    return chr(10).join([
        "  <entry>",
        f'    <title>{html.escape(title)}</title>',
        f'    <id>{html.escape(record["url"])}</id>',
        f'    <updated>{html.escape(updated)}</updated>',
        f'    <link href="{html.escape(record["url"], quote=True)}"/>',
        f'    <summary>{html.escape(summary)}</summary>',
        "  </entry>",
    ])


def render_feed(registry: dict) -> None:
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    entries = []
    for series in registry["series"]:
        for record in series["versions"]:
            entries.append((series, record))
    entries.sort(key=lambda item: sort_key(item[1]), reverse=True)
    body = chr(10).join(feed_entry(series, record, generated) for series, record in entries)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        "  <title>Torus-Node Research Updates</title>",
        "  <subtitle>UTC-dated publication, software, verification, and portal updates.</subtitle>",
        f"  <id>{BASE}updates.html</id>",
        f'  <link rel="alternate" href="{BASE}updates.html"/>',
        f'  <link rel="self" type="application/atom+xml" href="{BASE}feed.xml"/>',
        f"  <updated>{generated}</updated>",
        "  <author><name>Youngik (Tom) Lee</name></author>",
        body,
        "</feed>",
    ]
    FEED.write_text(chr(10).join(lines) + chr(10), encoding="utf-8")


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8-sig"))
    render_page(registry)
    render_feed(registry)
    count = sum(len(series["versions"]) for series in registry["series"])
    print(f"Rendered {count} research records and Atom feed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())