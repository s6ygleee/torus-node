# Torus-Node Research Initiative

Public research portal for **Emergent Spacetime, Gravity, and Gauge Structure**, initiated by Youngik (Tom) Lee.

This repository is intentionally separate from [`torus-node-lean4`](https://github.com/s6ygleee/torus-node-lean4). It contains the public website, research roadmap, participation guidance, and GitHub community infrastructure. It does not duplicate or modify the Lean project.

## Research status

The current manuscript describes a finite conditional model. The unrestricted Poisson-source-to-continuum identification and several physical hypotheses remain open. The Preprints.org version is a preprint and has not undergone peer review.

- Paper: <https://doi.org/10.20944/preprints202611.0941.v1>
- Lean 4 and reproducibility repository: <https://github.com/s6ygleee/torus-node-lean4>
- Archived Lean release: <https://doi.org/10.5281/zenodo.23863514>

The originally supplied Zenodo identifier `10.5281/zenodo.23819696` returned “persistent identifier is not registered” when checked on 2026-11-15, so it is not presented as a publication on this site.

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
