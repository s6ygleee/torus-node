#!/usr/bin/env python3
"""Synchronize newly verified primary-series versions into the research registry."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / "assets/data/research-metadata.json"
REGISTRY = ROOT / "assets/data/research-records.json"


def version_key(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"d+", value))


def upsert(series: dict, item: dict) -> None:
    for existing in series["versions"]:
        existing["current"] = False
        if existing["version"] == item["version"]:
            existing.update(item)
            existing["current"] = True
            return
    item["current"] = True
    series["versions"].append(item)
    series["versions"].sort(key=lambda value: version_key(value["version"]))


def main() -> int:
    latest = json.loads(LATEST.read_text(encoding="utf-8-sig"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8-sig"))
    by_id = {series["id"]: series for series in registry["series"]}

    preprint = latest["preprint"]
    preprint_version = str(preprint["version"])
    preprint_doi = preprint.get("doi")
    upsert(by_id["torus-node-preprint"], {
        "id": f"preprint-v{preprint_version}",
        "version": preprint_version,
        "authors": preprint["authors"],
        "submitted_date": preprint.get("submitted_date"),
        "published_at": preprint["posted_date"],
        "date_precision": "date",
        "venue": "Preprints.org",
        "doi": preprint_doi,
        "url": f"https://doi.org/{preprint_doi}" if preprint_doi else preprint["landing_url"],
        "status": "Current version",
        "peer_reviewed": bool(preprint.get("peer_reviewed", False)),
        "note": None if preprint_doi else "The version-specific DOI is not shown until it resolves through a DOI metadata service.",
    })
    for item in by_id["torus-node-preprint"]["versions"][:-1]:
        item["status"] = f"Superseded by Version {preprint_version}"

    software = latest["software"]
    software_version = str(software["version"])
    upsert(by_id["torus-node-lean"], {
        "id": "lean-v" + software_version,
        "version": software_version,
        "authors": software["authors"],
        "published_at": software["published_at"],
        "date_precision": "second",
        "venue": "Zenodo",
        "doi": software["doi"],
        "url": f"https://doi.org/{software['doi']}",
        "release_url": software["github_release_url"],
        "status": "Current archived release",
    })
    for item in by_id["torus-node-lean"]["versions"][:-1]:
        item["status"] = "Archived release"

    registry["last_content_update"] = latest["last_content_update"]
    rendered = json.dumps(registry, indent=2, ensure_ascii=False) + "\n"
    current = REGISTRY.read_text(encoding="utf-8-sig")
    if current != rendered:
        REGISTRY.write_text(rendered, encoding="utf-8")
        print("Research registry synchronized")
    else:
        print("Research registry already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
