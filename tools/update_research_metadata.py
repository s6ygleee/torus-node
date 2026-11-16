#!/usr/bin/env python3
"""Refresh verified Torus-Node publication metadata and render static HTML.

Only official machine-readable records are accepted automatically. A source
failure never downgrades or erases the last verified version.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/research-metadata.json"
USER_AGENT = "torus-node-portal-metadata/1.0 (+https://github.com/s6ygleee/torus-node)"
ZENODO_LATEST = "https://zenodo.org/api/records/23863513/versions/latest"
GITHUB_LATEST = "https://api.github.com/repos/s6ygleee/torus-node-lean4/releases/latest"
CROSSREF_WORK = "https://api.crossref.org/works/"

def get_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)

def iso_z(value: str) -> str:
    return value.replace("+00:00", "Z").split(".")[0] + ("Z" if not value.endswith("Z") and "+" not in value else "")

def refresh(data: dict) -> tuple[dict, list[str]]:
    notes: list[str] = []
    current = json.loads(json.dumps(data))

    try:
        record = get_json(ZENODO_LATEST)
        meta = record["metadata"]
        published = record["created"].replace("+00:00", "Z")
        modified = record["modified"].replace("+00:00", "Z")
        current["software"].update({
            "title": meta["title"],
            "authors": [creator["name"] for creator in meta.get("creators", [])],
            "version": str(meta["version"]),
            "doi": record["doi"],
            "concept_doi": record["conceptdoi"],
            "published_at": published,
            "modified_at": modified,
            "github_release_url": f"https://github.com/s6ygleee/torus-node-lean4/releases/tag/v{meta['version']}",
            "repository_url": "https://github.com/s6ygleee/torus-node-lean4",
        })
        notes.append(f"Zenodo {meta['version']} verified")
    except Exception as exc:
        notes.append(f"Zenodo retained: {exc}")

    try:
        release = get_json(GITHUB_LATEST)
        tag = release["tag_name"]
        github_version = tag[1:] if tag.startswith("v") else tag
        if github_version == current["software"]["version"]:
            current["software"]["github_release_url"] = release["html_url"]
        notes.append(f"GitHub {tag} verified")
    except Exception as exc:
        notes.append(f"GitHub retained: {exc}")

    preprint = current["preprint"]
    found = None
    for version in range(1, int(preprint["version"]) + 6):
        doi = f"10.20944/preprints202611.0941.v{version}"
        try:
            message = get_json(CROSSREF_WORK + urllib.parse.quote(doi, safe=""))["message"]
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                continue
            notes.append(f"Crossref v{version} unavailable: HTTP {exc.code}")
            continue
        except Exception as exc:
            notes.append(f"Crossref v{version} unavailable: {exc}")
            continue
        found = (version, doi, message)

    if found and found[0] >= int(preprint["version"]):
        version, doi, message = found
        posted_parts = message.get("posted", message.get("published", {})).get("date-parts", [[]])[0]
        posted = "-".join(f"{part:02d}" if index else str(part) for index, part in enumerate(posted_parts)) if posted_parts else preprint["posted_date"]
        title = message.get("title", [preprint["title"]])[0]
        submitted_parts = message.get("accepted", {}).get("date-parts", [[]])[0]
        submitted = "-".join(f"{part:02d}" if index else str(part) for index, part in enumerate(submitted_parts)) if submitted_parts else preprint.get("submitted_date")
        authors = [" ".join(part for part in (author.get("given"), author.get("family")) if part) for author in message.get("author", [])]
        preprint.update({"version": version, "doi": doi, "posted_date": posted, "submitted_date": submitted, "title": title, "authors": authors})
        notes.append(f"Preprints v{version} DOI verified by Crossref")
    else:
        notes.append(f"Preprints v{preprint['version']} retained; no newer registered DOI")

    if current != data:
        current["last_content_update"] = dt.datetime.now(dt.timezone.utc).date().isoformat()
    return current, notes

def marked(text: str, key: str, content: str, fallback: str | None = None) -> str:
    block = f"<!-- AUTO:{key}:START -->\n{content}\n<!-- AUTO:{key}:END -->"
    pattern = rf"<!-- AUTO:{re.escape(key)}:START -->.*?<!-- AUTO:{re.escape(key)}:END -->"
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, block, text, count=1, flags=re.S)
    if fallback:
        updated, count = re.subn(fallback, block, text, count=1, flags=re.S)
        if count:
            return updated
    raise RuntimeError(f"Could not locate render target {key}")

def display_date(iso_date: str) -> str:
    value = dt.date.fromisoformat(iso_date[:10])
    return f"{value.day} {value.strftime('%B %Y')}"

def render(data: dict) -> None:
    p = data["preprint"]
    s = data["software"]
    preprint_link = f"https://doi.org/{p['doi']}" if p.get("doi") else p["landing_url"]
    preprint_link_label = "Open version DOI" if p.get("doi") else "Open latest version"
    software_doi_url = f"https://doi.org/{s['doi']}"
    published = dt.datetime.fromisoformat(s["published_at"].replace("Z", "+00:00"))
    software_date = f"{published.day} {published.strftime('%B %Y')}"
    software_time = published.strftime("%H:%M UTC")
    title_html = html.escape(p["title"]).replace("D4", "D<sub>4</sub>").replace("S4", "S<sub>4</sub>")

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    index_preprint = f'''          <article class="card reveal"><span class="tag preprint">Preprint · v{p["version"]}</span><h3 style="margin-top:1rem">{title_html}</h3><p>Youngik (Tom) Lee · Preprints.org · posted <time datetime="{p["posted_date"]}">{display_date(p["posted_date"])}</time> · not peer reviewed.</p><p><a href="{preprint_link}">{preprint_link_label}</a></p></article>'''
    index = marked(index, "INDEX_PREPRINT", index_preprint, r'\s*<article class="card reveal"><span class="tag preprint">Preprint.*?</article>')
    index_software = f'''          <article class="card reveal"><span class="tag preprint">Software &amp; data · v{s["version"]}</span><h3 style="margin-top:1rem">Lean 4 formalisation and reproducibility data</h3><p>Youngik (Tom) Lee · Zenodo · released <time datetime="{s["published_at"]}">{software_date}, {software_time}</time> · open verification archive.</p><p><a href="{software_doi_url}">DOI {s["doi"]}</a></p></article>'''
    index = marked(index, "INDEX_SOFTWARE", index_software, r'\s*<article class="card reveal"><span class="tag preprint">Software.*?</article>')
    index = index.replace("https://doi.org/10.20944/preprints202611.0941.v1\">Read the preprint", f"{preprint_link}\">Read the preprint")
    (ROOT / "index.html").write_text(index, encoding="utf-8")

    pubs = (ROOT / "publications.html").read_text(encoding="utf-8")
    doi_note = "" if p.get("doi") else f'<p class="scope-note">The Version {p["version"]} DOI is not linked until its registration resolves through a DOI metadata service. The verified manuscript landing page is used meanwhile.</p>'
    pub_preprint = f'''  <article class="publication"><div><span class="pub-kind">Preprint · v{p["version"]}</span></div><div><div class="meta"><span class="tag preprint">Not peer reviewed</span></div><h2>{title_html}</h2><p><strong>Youngik (Tom) Lee</strong><br>Preprints.org · submitted <time datetime="{p["submitted_date"]}">{display_date(p["submitted_date"])}</time> · posted <time datetime="{p["posted_date"]}">{display_date(p["posted_date"])}</time> · Version {p["version"]}.</p><p>The paper distinguishes finite-model results from conditional continuum and physical conclusions. The unrestricted source-to-continuum identification and stated mass-gap and source-reflection-positivity questions remain open.</p><div class="actions"><a class="button primary" href="{preprint_link}">{preprint_link_label}</a><a class="button" href="{p["landing_url"]}">Publication page</a></div>{doi_note}<p class="citation">Lee, Y. (Tom). “A Torus-Node Model for Emergent Spacetime, Gravity, and Gauge Structure.” Preprints 2026, 2026110941, Version {p["version"]}.</p></div></article>'''
    pub_software = f'''  <article class="publication"><div><span class="pub-kind">Software &amp; data</span></div><div><div class="meta"><span class="tag established">Published archive</span><span class="tag preprint">Version {s["version"]}</span></div><h2>{html.escape(s["title"])}</h2><p><strong>Youngik (Tom) Lee</strong><br>Zenodo · released <time datetime="{s["published_at"]}">{software_date}, {software_time}</time> · Software · MIT-licensed code with accompanying verification material described in the record.</p><p>The archive contains Lean 4 sources, statement-to-declaration tables, certificate records, retained calculation scripts, fixed outputs, and interval fixtures. Its metadata states that continuum interfaces remain conditional.</p><div class="actions"><a class="button primary" href="{software_doi_url}">Open version DOI</a><a class="button" href="{s["repository_url"]}">GitHub repository</a><a class="button" href="{s["github_release_url"]}">Release v{s["version"]}</a></div><p class="citation">Lee, Youngik (Tom). (2026). {html.escape(s["title"])} ({s["version"]}). Zenodo. https://doi.org/{s["doi"]}</p></div></article>'''
    rendered_publications = (
        "<!-- AUTO:PUBLICATIONS_PREPRINT:START -->\n" + pub_preprint +
        "\n<!-- AUTO:PUBLICATIONS_PREPRINT:END -->\n" +
        "<!-- AUTO:PUBLICATIONS_SOFTWARE:START -->\n" + pub_software +
        "\n<!-- AUTO:PUBLICATIONS_SOFTWARE:END -->\n"
    )
    pubs, count = re.subn(
        r'(<section class="section"><div class="shell">).*?(?=<div class="callout warning">)',
        lambda match: match.group(1) + "\n" + rendered_publications + "  ",
        pubs,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError("Could not rebuild publications section")
    (ROOT / "publications.html").write_text(pubs, encoding="utf-8")

    verification = (ROOT / "verification.html").read_text(encoding="utf-8")
    archive = f'''  <div class="callout"><strong>Archive identity.</strong> Cite the immutable Zenodo v{s["version"]} record <a href="{software_doi_url}">{s["doi"]}</a>, published <time datetime="{s["published_at"]}">{software_date}, {software_time}</time>, when reporting reproduction results.</div>'''
    verification = marked(verification, "VERIFICATION_ARCHIVE", archive, r'\s*<div class="callout"><strong>Archive identity\.</strong>.*?</div>')
    verification = re.sub(r'<a href="https://doi.org/10\.5281/zenodo\.\d+">Zenodo archive(?: v[^<]+)?</a>', f'<a href="{software_doi_url}">Zenodo archive v{s["version"]}</a>', verification)
    (ROOT / "verification.html").write_text(verification, encoding="utf-8")

    about = (ROOT / "about.html").read_text(encoding="utf-8")
    identifiers = f'''<p>GitHub: <a href="https://github.com/s6ygleee">@s6ygleee</a><br>Latest preprint: <a href="{preprint_link}">Version {p["version"]}</a> (not peer reviewed)<br>Lean repository: <a href="{s["repository_url"]}">torus-node-lean4</a><br>Lean archive: <a href="{software_doi_url}">v{s["version"]}, {s["doi"]}</a></p>'''
    about = marked(about, "ABOUT_IDENTIFIERS", identifiers, r'<p>GitHub:.*?</p>')
    (ROOT / "about.html").write_text(about, encoding="utf-8")

    for relative in ("README.md", "docs/theorem-assumption-map.md"):
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        text = re.sub(r'https://doi\.org/10\.20944/preprints202611\.0941\.v\d+', preprint_link, text)
        text = re.sub(r'https://doi\.org/10\.5281/zenodo\.\d+', software_doi_url, text)
        path.write_text(text, encoding="utf-8")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sitemap = re.sub(r'<lastmod>[^<]+</lastmod>', f'<lastmod>{data["last_content_update"]}</lastmod>', sitemap)
    if "<lastmod>" not in sitemap:
        sitemap = sitemap.replace("</loc><priority>", f'</loc><lastmod>{data["last_content_update"]}</lastmod><priority>')
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="Render the checked-in metadata without network access")
    args = parser.parse_args()
    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    if args.offline:
        updated, notes = data, ["offline render"]
    else:
        updated, notes = refresh(data)
    DATA.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    render(updated)
    print("; ".join(notes))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
