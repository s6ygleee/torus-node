#!/usr/bin/env python3
"""Render the versioned, multi-author Research Record from verified JSON data."""
from __future__ import annotations

import datetime as dt
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/research-records.json"
PAGE = ROOT / "research-record.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def format_date(value: str, precision: str) -> tuple[str, str]:
    if "T" in value:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        label = f"{parsed.day} {parsed.strftime('%B %Y')}, {parsed.strftime('%H:%M')} UTC"
        return value, label
    parsed_date = dt.date.fromisoformat(value)
    label = f"{parsed_date.day} {parsed_date.strftime('%B %Y')}"
    if precision == "date":
        label += " (date supplied by source)"
    return value, label


def render_version(version: dict, primary: bool) -> str:
    published_value, published_label = format_date(version["published_at"], version.get("date_precision", "date"))
    authors = ", ".join(version["authors"])
    classes = ["version-node"]
    if version.get("current"):
        classes.append("is-current")
    if primary and version.get("current"):
        classes.append("is-primary")
    badges = [f'<span class="relation-badge">{esc(version["status"])}</span>']
    if "peer_reviewed" in version:
        review = "Peer reviewed" if version["peer_reviewed"] else "Not peer reviewed"
        badges.append(f'<span class="relation-badge review-status">{review}</span>')
    submitted = ""
    if version.get("submitted_date"):
        submitted_value, submitted_label = format_date(version["submitted_date"], "date")
        submitted = f'<dt>Submitted</dt><dd><time datetime="{esc(submitted_value)}">{esc(submitted_label)}</time></dd>'
    doi = f'<dt>DOI</dt><dd><a href="https://doi.org/{esc(version["doi"])}">{esc(version["doi"])}</a></dd>' if version.get("doi") else '<dt>DOI</dt><dd>Awaiting verified registration</dd>'
    release_button = ""
    if version.get("release_url"):
        release_button = f'<a class="version-link secondary" href="{esc(version["release_url"])}">GitHub release</a>'
    note = f'<p class="version-note">{esc(version["note"])}</p>' if version.get("note") else ""
    current_label = '<span class="current-marker">Current</span>' if version.get("current") else ""
    return f'''<li class="{" ".join(classes)}" id="{esc(version["id"])}">
      <div class="version-heading"><span class="version-number">v{esc(version["version"])}</span>{current_label}</div>
      <div class="version-badges">{"".join(badges)}</div>
      <dl class="version-meta">
        <dt>Author</dt><dd>{esc(authors)}</dd>
        {submitted}
        <dt>Published</dt><dd><time datetime="{esc(published_value)}">{esc(published_label)}</time></dd>
        <dt>Host</dt><dd>{esc(version["venue"])}</dd>
        {doi}
      </dl>
      {note}
      <div class="version-actions"><a class="version-link" href="{esc(version["url"])}">Open record</a>{release_button}</div>
    </li>'''


def render_series(series: dict) -> str:
    versions = "\n".join(render_version(item, bool(series.get("primary"))) for item in series["versions"])
    primary_class = " primary-series" if series.get("primary") else ""
    return f'''<article class="record-series{primary_class}" id="{esc(series["id"])}">
      <header class="series-header">
        <span class="record-type">{esc(series["label"])}</span>
        <h2>{esc(series["title"])}</h2>
        <p>{esc(series["description"])}</p>
        <span class="series-count">{len(series["versions"])} verified versions</span>
      </header>
      <ol class="version-timeline">{versions}</ol>
    </article>'''


def render_external_work(work: dict) -> str:
    published_value, published_label = format_date(work["published_at"], work.get("date_precision", "date"))
    relations = "".join(f'<span class="relation-badge">{esc(item["type"])} → {esc(item["target"])}</span>' for item in work.get("relations", []))
    version = f' · v{esc(work["version"])}' if work.get("version") else ""
    doi = f'<p class="external-doi">DOI: {esc(work["doi"])}</p>' if work.get("doi") else ""
    return f'''<article class="external-work" id="{esc(work["id"])}">
      <div class="version-badges">{relations}</div>
      <h3>{esc(work["title"])}</h3>
      <p><strong>{esc(", ".join(work["authors"]))}</strong>{version}</p>
      <p>{esc(work["venue"])} · <time datetime="{esc(published_value)}">{esc(published_label)}</time></p>
      {doi}
      <a class="version-link" href="{esc(work["url"])}">Open independent record</a>
    </article>'''


def render(data: dict) -> str:
    series_html = "\n".join(render_series(series) for series in data["series"])
    relation = data["series_relations"][0]
    series_labels = {series["id"]: series["label"] for series in data["series"]}
    if data["external_works"]:
        external_html = '<div class="external-grid">' + "\n".join(render_external_work(work) for work in data["external_works"]) + "</div>"
    else:
        external_html = '''<div class="reference-empty">
          <span class="empty-symbol" aria-hidden="true">+</span>
          <div><h3>No independently authored records are listed yet</h3><p>This area is reserved for verified papers, formal checks, extensions, critiques, and counterexamples by other researchers. No researcher or publication is added without a traceable public record.</p></div>
          <a class="button" href="https://github.com/s6ygleee/torus-node/issues/new?template=independent-research-result.yml">Submit a research record</a>
        </div>'''
    return f'''<section class="record-network section compact" aria-labelledby="record-network-title">
      <div class="shell">
        <div class="section-head">
          <div><span class="kicker">Versioned research network</span><h2 id="record-network-title">Series, versions, authors, and reference relations</h2></div>
          <p>Each node is a specific public version. Arrows within a series indicate revision order; the cross-series relation describes scope, not identity.</p>
        </div>
        <div class="series-grid">{series_html}</div>
        <div class="series-relation" aria-label="Relation between the software and manuscript series">
          <span>{esc(series_labels[relation["source"]])}</span><strong>{esc(relation["type"])}</strong><span>{esc(series_labels[relation["target"]])}</span>
          <p>{esc(relation["label"])}</p>
        </div>
      </div>
    </section>
    <section class="section external-records" aria-labelledby="external-records-title">
      <div class="shell">
        <div class="section-head">
          <div><span class="kicker">Independent and related research</span><h2 id="external-records-title">Research by other authors</h2></div>
          <p>Future records can reference any version above and one another. Inclusion records provenance and relevance; it is not an endorsement of a conclusion.</p>
        </div>
        {external_html}
        <div class="relation-legend" aria-label="Supported reference relation types">
          <strong>Supported relations</strong>
          {"".join(f"<span>{esc(relation_type)}</span>" for relation_type in data["relation_types"])}
        </div>
      </div>
    </section>'''


def validate_data(data: dict) -> None:
    version_ids = [version["id"] for series in data["series"] for version in series["versions"]]
    external_ids = [work["id"] for work in data["external_works"]]
    all_ids = version_ids + external_ids
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("Research record IDs must be unique")
    for series in data["series"]:
        for version in series["versions"]:
            if not version.get("authors") or not version.get("published_at") or not version.get("url"):
                raise ValueError(f"Incomplete version record: {version.get('id')}")
    known_targets = set(all_ids)
    for work in data["external_works"]:
        if not work.get("authors") or not work.get("published_at") or not work.get("url"):
            raise ValueError(f"Incomplete external work: {work.get('id')}")
        for relation in work.get("relations", []):
            if relation.get("type") not in data["relation_types"]:
                raise ValueError(f"Unsupported relation type: {relation.get('type')}")
            if relation.get("target") not in known_targets:
                raise ValueError(f"Unknown relation target: {relation.get('target')}")


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    validate_data(data)
    page = PAGE.read_text(encoding="utf-8")
    generated = render(data)
    block = f"<!-- AUTO:RESEARCH_NETWORK:START -->\n{generated}\n<!-- AUTO:RESEARCH_NETWORK:END -->"
    pattern = r"<!-- AUTO:(?:RESEARCH_NETWORK|RECORD_MAP):START -->.*?<!-- AUTO:(?:RESEARCH_NETWORK|RECORD_MAP):END -->"
    page, count = re.subn(pattern, block, page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("Research Record render target was not found")
    PAGE.write_text(page, encoding="utf-8")
    print(f"Rendered {sum(len(series['versions']) for series in data['series'])} version nodes and {len(data['external_works'])} external works")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
