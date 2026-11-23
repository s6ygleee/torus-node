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
    "index.html": ("Torus-Node Model Research | Emergent Spacetime & Quantum Gravity", "Independent Torus-Node model and torus theory research on emergent spacetime, quantum gravity, gauge structure, grand unified theory (GUT), and theory of everything (TOE).", ""),
    "research.html": ("Torus-Node Theory | Torus Theory, GUT & TOE", "Torus theory and the Torus-Node theory framework: emergent spacetime, quantum gravity, gauge structure, grand unified theory (GUT), and theory of everything (TOE) research boundaries.", "research.html"),
    "research-briefs.html": ("Research Briefs | Torus-Node Model, D4 Stability & GUT/TOE Context", "Short, testable research briefs for the Torus-Node model: D4 spectral stability, finite reflection positivity, S4 gauge representations, Lean 4 verification, and carefully bounded GUT and TOE context.", "research-briefs.html"),
    "publications.html": ("Publications · Torus-Node", "Verified publication metadata, software records, and citation guidance for the Torus-Node research program.", "publications.html"),
    "research-record.html": ("Research Record · Torus-Node", "A versioned provenance network connecting Torus-Node publications, formal releases, and independent research by other authors through explicit references.", "research-record.html"),
    "verification.html": ("Verification · Torus-Node", "Verification scope, Lean 4 resources, reproducibility workflow, and limitations for the Torus-Node research program.", "verification.html"),
    "open-problems.html": ("Open Research Problems · Torus-Node", "Open mathematical and physical research problems in continuum reconstruction, reflection positivity, gauge structure, gravity, and phenomenology.", "open-problems.html"),
    "community.html": ("Research Community · Torus-Node", "GitHub Discussions, Issues, Pull Requests, and evidence-based scientific exchange for the Torus-Node research program.", "community.html"),
    "contribute.html": ("Contribute · Torus-Node", "How to reproduce results, report errors, submit counterexamples, contribute Lean code, and propose research collaboration.", "contribute.html"),
    "updates.html": ("Research Updates · Torus-Node", "UTC-dated publication, software, verification, and portal updates for the Torus-Node research initiative.", "updates.html"),
    "about.html": ("About · Torus-Node", "About the independent Torus-Node Research Initiative and its initiating researcher, Youngik (Tom) Lee.", "about.html"),
}

PAGE_KEYWORDS = {
    "index.html": ["Torus-Node", "Torus-Node model", "Torus-Node theory", "torus theory", "emergent spacetime", "quantum gravity", "grand unified theory", "GUT", "theory of everything", "TOE", "Lean 4 formal verification"],
    "research.html": ["torus theory", "Torus-Node model", "Torus-Node theory", "discrete geometry", "D4 spatial moves", "S4 ordered-history algebra", "emergent gravity", "quantum gravity", "grand unified theory", "GUT", "theory of everything", "TOE", "gauge theory", "chiral matter"],
    "research-briefs.html": ["Torus-Node model", "Torus-Node theory", "torus theory", "D4 spectral stability", "reflection positivity", "S4 gauge representations", "Lean 4 formal verification", "emergent spacetime", "quantum gravity", "grand unified theory", "GUT", "theory of everything", "TOE"],
    "publications.html": ["Torus-Node preprint", "Youngik Tom Lee", "Lean 4 archive", "formal verification"],
    "research-record.html": ["research provenance", "versioned publications", "independent verification", "research citations"],
    "verification.html": ["Lean 4", "formal verification", "reproducibility", "axiom audit"],
    "open-problems.html": ["quantum gravity open problems", "continuum limit", "reflection positivity", "grand unification research"],
    "community.html": ["open science", "independent verification", "mathematical research collaboration"],
    "contribute.html": ["research reproducibility", "counterexamples", "Lean 4 contributions"],
    "updates.html": ["Torus-Node research updates", "preprint version 2", "Lean 4 release", "Zenodo v1.1.0", "UTC publication dates"],
    "about.html": ["Torus-Node Research Initiative", "Torus-Node model", "Torus-Node theory", "torus theory", "grand unified theory", "GUT", "theory of everything", "TOE", "Youngik Tom Lee", "independent theoretical physics research"],
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
        "keywords": PAGE_KEYWORDS[filename],
        "isPartOf": {"@id": BASE + "#website"},
        "about": {"@id": BASE + "#initiative"},
        "dateModified": DATA["last_content_update"],
        "inLanguage": "en",
    }
    initiative = {
        "@type": "ResearchProject",
        "@id": BASE + "#initiative",
        "name": "Torus-Node Research Initiative",
        "description": "Independent Torus-Node model and torus theory research on emergent spacetime, quantum gravity, gauge structure, grand unified theory, and theory of everything questions. The project does not claim a completed GUT or TOE.",
        "keywords": PAGE_KEYWORDS["index.html"],
        "alternateName": ["Torus-Node model", "Torus-Node theory", "Torus theory research"],
        "url": BASE,
        "sameAs": [DATA["preprint"]["landing_url"], DATA["software"]["repository_url"], "https://doi.org/" + DATA["software"]["doi"]],
        "founder": {"@id": BASE + "#youngik-tom-lee"},
    }
    items = [website, webpage, initiative, person]
    breadcrumb_names = {
        "research.html": "Research",
        "research-briefs.html": "Research briefs",
        "publications.html": "Publications",
        "research-record.html": "Research Record",
        "updates.html": "Updates",
        "verification.html": "Verification",
        "open-problems.html": "Open Research Problems",
        "community.html": "Research Community",
        "contribute.html": "Contribute",
        "about.html": "About",
    }
    if filename in breadcrumb_names:
        items.append({
            "@type": "BreadcrumbList",
            "@id": url + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                {"@type": "ListItem", "position": 2, "name": breadcrumb_names[filename], "item": url},
            ],
        })
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
    if filename == "research-record.html":
        registry = json.loads((ROOT / "assets/data/research-records.json").read_text(encoding="utf-8-sig"))
        list_items = []
        position = 1
        for series in registry["series"]:
            schema_type = "ScholarlyArticle" if series["record_type"] == "Scholarly preprint" else "SoftwareSourceCode"
            for version_record in series["versions"]:
                work = {
                    "@type": schema_type,
                    "name": f"{series['title']} — version {version_record['version']}",
                    "author": [{"@type": "Person", "name": author} for author in version_record["authors"]],
                    "datePublished": version_record["published_at"],
                    "version": version_record["version"],
                    "url": version_record["url"],
                    "isAccessibleForFree": True,
                }
                if version_record.get("doi"):
                    work["identifier"] = "https://doi.org/" + version_record["doi"]
                list_items.append({"@type": "ListItem", "position": position, "item": work})
                position += 1
        items.append({
            "@type": "ItemList",
            "@id": url + "#versioned-records",
            "name": "Torus-Node versioned research records",
            "numberOfItems": len(list_items),
            "itemListElement": list_items,
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
