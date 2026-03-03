# Agent Instructions: docs/

## Purpose

This directory contains the [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
source for the documentation site published to GitHub Pages as part of the release workflow.
The home page is auto-generated from `README.md` by `docs/gen_ref_pages.py`.

## Directory Layout

```
docs/
  gen_ref_pages.py    # Copies README.md → index.md and screenshot at build time
  screenshot.png      # Screenshot of the running app (used in README / docs)
  css/
    style.css         # Custom MkDocs theme overrides (primary colour, code selection)
```

## Key Conventions

- **Home page**: `gen_ref_pages.py` writes `README.md` content into `index.md` at build time
  using the `mkdocs-gen-files` plugin. Do **not** create a hand-written `docs/index.md` – it
  will be overwritten on build.
- **Navigation**: Defined in `mkdocs.yaml` at the repo root under `nav:`. Register any new
  pages there; the `literate-nav` plugin reads `SUMMARY.md` files for sub-navigation.
- **Theme colours**: The primary and accent colour is `#00C9BF` (RaBe teal), set in both
  `docs/css/style.css` and the `theme.palette` entries in `mkdocs.yaml`.
- **Plugins**: `gen-files`, `literate-nav`, `section-index`, `autorefs`, and `search` are
  configured in `mkdocs.yaml`. Do not remove them.

## Local Preview

```bash
pip install mkdocs-material mkdocs-section-index mkdocs-llmstxt
mkdocs serve
```

Open `http://127.0.0.1:8000` to preview changes before committing.

## Updating the Screenshot

Replace `docs/screenshot.png` with a new screenshot of the running application whenever the
UI changes significantly.

## llms.txt

- [squidfunk.github.io/mkdocs-material](https://squidfunk.github.io/mkdocs-material/) – MkDocs Material theme documentation
