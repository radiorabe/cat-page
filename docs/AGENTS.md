# Agent Instructions: docs/

## Purpose

This directory contains the [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
source for the documentation site published to GitHub Pages as part of the release workflow.

## Directory Layout

```
docs/
  index.md            # Static landing page (uses template: home.html)
  getting-started.md  # Quick-start guide
  configuration.md    # Full PAGE_* configuration reference
  contributing.md     # Contributing and development guide
  llms.txt            # LLMs-friendly project description (served at /llms.txt)
  gen_ref_pages.py    # No-op placeholder (kept for compatibility)
  screenshot.png      # Screenshot of the running app (used in docs)
  css/
    style.css         # Custom MkDocs theme overrides (colours, hero, feature grid)
  overrides/
    home.html         # Custom landing page template (hero + feature grid)
```

## Key Conventions

- **Home page**: `docs/index.md` is a **static** file with `template: home.html` front matter.
  The actual landing-page content (hero section and feature grid) lives in
  `docs/overrides/home.html`. Do **not** regenerate `index.md` from `README.md`.
- **Landing page template**: `docs/overrides/home.html` extends `main.html` and overrides
  the `tabs` block (hero section) and `content` block (feature grid). Follow the same
  pattern as the other RaBe projects.
- **Navigation**: Defined in `mkdocs.yaml` under `nav:`. Register any new pages there.
- **Theme colours**: The primary and accent colour is `#00C9BF` (RaBe teal), set in both
  `docs/css/style.css` and the `theme.palette` entries in `mkdocs.yaml`.
- **Plugins**: `search`, `section-index`, and `autorefs` are configured in
  `mkdocs.yaml`. Do not remove them.
- **llms.txt**: `docs/llms.txt` is a **static** file that MkDocs copies verbatim to
  `/llms.txt` in the built site. Edit it directly to update the LLMs-friendly description.

## Local Preview

```bash
pip install mkdocs-material mkdocs-section-index mkdocs-autorefs
mkdocs serve
```

Open `http://127.0.0.1:8000` to preview changes before committing.

## Updating the Screenshot

Replace `docs/screenshot.png` with a new screenshot of the running application whenever the
UI changes significantly.

## llms.txt

- [squidfunk.github.io/mkdocs-material](https://squidfunk.github.io/mkdocs-material/) – MkDocs Material theme documentation
