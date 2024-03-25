"""Generate the code reference pages and navigation.

From https://mkdocstrings.github.io/recipes/
"""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

path = Path("app/")
module_path = path.relative_to(".").with_suffix("")
doc_path = path.relative_to(".").with_suffix(".md")
full_doc_path = Path("reference", doc_path)

parts = tuple(module_path.parts)

nav[parts] = doc_path.as_posix()

full_doc_path.parent.mkdir(parents=True, exist_ok=True)
with mkdocs_gen_files.open(full_doc_path, "w") as fd:
    ident = ".".join(parts)
    fd.write(f"::: {ident}")

mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())

with Path("README.md").open("r") as readme, mkdocs_gen_files.open(
    "index.md",
    "w",
) as index_file:
    index_file.writelines(readme.read())

with Path("docs/screenshot.png").open("rb") as orig, mkdocs_gen_files.open(
    "docs/screenshot.png", "wb"
) as screenshot:
    screenshot.write(orig.read())
