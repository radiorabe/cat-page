"""Set up cat-page."""

from setuptools import find_packages, setup

with open("requirements.txt") as file:
    requirements = file.read().splitlines()


setup(
    name="cat-page",
    description="RaBe Cat Landing Page",
    url="http://github.com/radiorabe/cat-page",
    author="RaBe IT-Reaktion",
    author_email="it@rabe.ch",
    license="AGPL-3",
    version_config=True,
    setup_requires=["setuptools-git-versioning"],
    install_requires=requirements,
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    entry_points={"console_scripts": ["catpage=app.server:main"]},
    zip_safe=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
)
