"""Generate the docs page.

From https://mkdocstrings.github.io/recipes/
"""

from pathlib import Path

import mkdocs_gen_files

with (
    Path("README.md").open("r") as readme,
    mkdocs_gen_files.open(
        "index.md",
        "w",
    ) as index_file,
):
    index_file.writelines(readme.read())

with (
    Path("docs/screenshot.png").open("rb") as orig,
    mkdocs_gen_files.open("docs/screenshot.png", "wb") as screenshot,
):
    screenshot.write(orig.read())
