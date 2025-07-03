#!/usr/bin/env python
"""Ensure that lsst-texmf authors file is ok in case an entry was added."""

import subprocess

import yaml
from authordb import AuthorDbYaml, load_authordb


def make_all(authordb: AuthorDbYaml) -> None:
    """Go through all authors and put in one big file so we can test."""
    allauthors = []
    for a in authordb.authors:
        allauthors.append(a)
    with open("authors.yaml", "w") as file:
        yaml.dump(allauthors, file)


def main() -> None:
    """Run script."""
    adb = load_authordb()

    make_all(adb)
    subprocess.call("bin/db2authors.py", shell=True)


if __name__ == "__main__":
    main()
