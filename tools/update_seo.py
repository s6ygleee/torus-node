#!/usr/bin/env python3
"""Render consistent discoverability metadata into the static pages."""
from __future__ import annotations
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://s6ygleee.github.io/torus-node/"
IMAGE = BASE + "assets/images/torus-node-social.png"
DATA = json.loads((ROOT / "assets/data/research-metadata.json").read_text(encoding="utf-8-sig"))

PAGES = {
    "index.html": ("Torus-Node Research Initiative", "An independent research portal for the Torus-Node program on emergent spacetime, gravity, gauge structure, and formal verification.", ""),
    "research.html": ("Research Framework · Torus-Node", "Research framework, assumptions, conditional results, and open interfaces of the Torus-Node program.", "research.html"),
    "publications.html": ("Publications · Torus-Node", "Verified publication metadata, software records, and citation guidance for the Torus-Node research program.", "publications.html"),
    "research-record.html": ("Research Record · Torus-Node", "A provenance map connecting Torus-Node preprint versions, Lean 4 formalisation, Zenodo archives, authorship, release dates, and update policy.", "research-record.html"),
    "verification.html": ("Verification · Torus-Node", "Verification scope, Lean 4 resources, reproducibility workflow, and limitations for the Torus-Node research program.", "verification.html"),
    "open-problems.html": ("Open Research Problems · Torus-Node", "Open mathematical and physical research problems in continuum reconstruction, reflection positivity, gauge structure, gravity, and phenomenology.", "open-problems.html"),
    "community.html": ("Research Community · Torus-Node", "GitHub Discussions, Issues, Pull Requests, and evidence-based scientific exchange for the Torus-Node research program.", "community.html"),
    "contribute.html": ("Contribute · Torus-Node", "How to reproduce results, report errors, submit counterexamples, contribute Lean code, and propose research collaboration.", "contribute.html"),
    "about.html": ("About · Torus-Node", "About the independent Torus-Node Research Initiative and its initiating researcher, Youngik (Tom) Lee.", "about.html"),
}

def graph(filename: str, title: str, description: str, url: str) -> dict:
    person = {
        "@type": "Person",
        "@id": BASE + "#youngik-tom-lee",
        "name": "Youngik (Tom) Lee",
        "url": "https://github.com/s6ygleee",
        "sameAs": ["https://github.com/s6ygleee"],
    }
    website = {
        "@type": "WebSite",
        "@id": BASE + "#website",
        "url": BASE,
        "name": "Torus-Node Research Initiative",
        "description": "Emergent Spacetime, Gravity, and Gauge Structure",
        "inLanguage": "en",
        "publisher": {"@id": BASE + "#youngik-tom-lee"},
    }
    webpage = {
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": title,
        "description": description,
        "isPartOf": {"@id": BASE + "#website"},
        "about": {"@id": BASE + "#initiative"},
        "dateModified": DATA["last_content_update"],
        "inLanguage": "en",
    }
    initiative = {
        "@type": "ResearchProject",
        "@id": BASE + "#initiative",
        "name": "Torus-Node Research Initiative",
        "description": "Independent theoretical research on emergent spacetime, gravity, gauge structure, and formal verification.",
        "url": BASE,
        "founder": {"@id": BASE + "#youngik-tom-lee"},
    }
    items = [website, webpage, initiative, person]
    p = DATA["preprint"]
    s = DATA["software"]
    if filename == "publications.html":
        article = {
            "@type": "ScholarlyArticle",
            "@id": p["landing_url"] + f"#v{p['version']}",
            "headline": p["title"],
            "name": p["title"],
            "author": {"@id": BASE + "#youngik-tom-lee"},
            "url": p["landing_url"],
            "datePublished": p["posted_date"],
            "version": str(p["version"]),
            "isAccessibleForFree": True,
            "inLanguage": "en",
            "creativeWorkStatus": "Preprint; not peer reviewed",
        }
        if p.get("doi"):
            article["identifier"] = "https://doi.org/" + p["doi"]
        items.append(article)
    if filename in {"publications.html", "verification.html"}:
        items.append({
            "@type": "SoftwareSourceCode",
            "@id": "https://doi.org/" + s["doi"],
            "name": s["title"],
            "author": {"@id": BASE + "#youngik-tom-lee"},
            "codeRepository": s["repository_url"],
            "downloadUrl": "https://doi.org/" + s["doi"],
            "identifier": "https://doi.org/" + s["doi"],
            "version": s["version"],
            "datePublished": s["published_at"],
            "dateModified": s["modified_at"],
            "programmingLanguage": "Lean",
            "license": "https://opensource.org/license/mit",
            "isAccessibleForFree": True,
        })
    return {"@context": "https://schema.org", "@graph": items}

def render(filename: str, title: str, description: str, suffix: str) -> None:
    path = ROOT / filename
    text = path.read_text(encoding="utf-8")
    url = BASE + suffix
    text = re.sub(r'\s*<meta property="og:[^>]+>', "", text)
    text = re.sub(r'\s*<meta name="twitter:[^>]+>', "", text)
    marker_pattern = r'\s*<!-- SEO:START -->.*?<!-- SEO:END -->'
    text = re.sub(marker_pattern, "", text, flags=re.S)
    structured = json.dumps(graph(filename, title, description, url), ensure_ascii=False, separators=(",", ":"))
    block = f'''
  <!-- SEO:START -->
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta property="og:site_name" content="Torus-Node Research Initiative">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Torus-Node Research Initiative: Emergent Spacetime, Gravity, and Gauge Structure">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title, quote=True)}">
  <meta name="twitter:description" content="{html.escape(description, quote=True)}">
  <meta name="twitter:image" content="{IMAGE}">
  <script type="application/ld+json">{structured}</script>
  <!-- SEO:END -->'''
    description_tag = re.search(r'<meta name="description"[^>]*>', text)
    if not description_tag:
        raise RuntimeError(f"Description tag not found in {filename}")
    position = description_tag.end()
    text = text[:position] + block + text[position:]
    path.write_text(text, encoding="utf-8")

for filename, config in PAGES.items():
    render(filename, *config)
print(f"Rendered SEO metadata for {len(PAGES)} pages")
