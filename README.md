# Torus-Node Research Initiative

Public research portal for **Emergent Spacetime, Gravity, and Gauge Structure**, initiated by Youngik (Tom) Lee.

This repository is intentionally separate from [`torus-node-lean4`](https://github.com/s6ygleee/torus-node-lean4). It contains the public website, research roadmap, participation guidance, and GitHub community infrastructure. It does not duplicate or modify the Lean project.

## Research portal

- Public website: <https://s6ygleee.github.io/torus-node/>
- Research updates and UTC release history: <https://s6ygleee.github.io/torus-node/updates.html>
- Machine-readable Atom feed: <https://s6ygleee.github.io/torus-node/feed.xml>
- Versioned Research Record: <https://s6ygleee.github.io/torus-node/research-record.html>
- Publications and citation metadata: <https://s6ygleee.github.io/torus-node/publications.html>

Use these links when citing the portal. The preprint, Zenodo releases, and Lean repository remain the primary research and software records.
## Research status

The current manuscript describes a finite conditional model. The unrestricted Poisson-source-to-continuum identification and several physical hypotheses remain open. The Preprints.org version is a preprint and has not undergone peer review.

- Latest preprint: Version 2, posted 2026-11-16 (not peer reviewed): <https://www.preprints.org/manuscript/202611.0941>
- Lean 4 and reproducibility repository: <https://github.com/s6ygleee/torus-node-lean4>
- Archived Lean release: Version 1.1.0, published 2026-11-14 20:31 UTC: <https://doi.org/10.5281/zenodo.24229820>

The originally supplied Zenodo identifier `10.5281/zenodo.23819696` returned “persistent identifier is not registered” when checked on 2026-11-15, so it is not presented as a publication on this site.

## Weekly metadata automation

The workflow at .github/workflows/weekly-research-metadata.yml runs every Monday at 03:17 UTC and can also be started manually. It checks the official Zenodo API, the GitHub Releases API, and registered Preprints.org DOIs through Crossref. Verified newer records update the static publication cards, UTC timestamps, structured data, and sitemap. A source failure retains the last verified metadata rather than deleting or downgrading it.

Run the same update locally with these commands: python tools/update_research_metadata.py, python tools/sync_research_records.py, python tools/render_research_record.py, python tools/update_seo.py, and python tools/check_site.py.

## Local preview

No build step or package installation is required. Serve the repository root with any static HTTP server, for example:

```text
python -m http.server 8000
```

Then open `http://localhost:8000/`. Opening `index.html` directly also works for ordinary navigation.

## Structure

- HTML pages at the repository root
- `assets/css/styles.css`: shared responsive design system
- `assets/js/main.js`: navigation and progressive enhancement
- `assets/js/problems.js`: data-driven open-problem catalogue
- `assets/data/research-records.json`: versioned research series, authors, dates, and cross-reference relations
- `docs/`: research roadmap and theorem–assumption map
- `.github/ISSUE_TEMPLATE/`: scientific contribution forms
- `.github/DISCUSSION_TEMPLATE/`: structured forms for the seven research Discussion categories

## Deployment

The repository is deployment-ready from the `main` branch root. In repository settings, set **Pages → Build and deployment → Source** to **Deploy from a branch**, then choose **main** and **/(root)**. The expected URL is:

<https://s6ygleee.github.io/torus-node/>

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Errors, counterexamples, negative results, and independent reproductions are welcome when they are technically specific and reproducible.

## Content and code

No repository-wide license is inferred by this portal. Contributors retain rights to their contributions subject to the terms they explicitly provide. The separate Lean archive carries its own license information.
