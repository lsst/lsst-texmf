#!/usr/bin/env python
"""Ensure that lsst-texmf authors file is ok in case an entry was added.
"""

import os
import yaml
import subprocess


def make_all(authordb):
    """Go through all authors and put in one big file so we can test"""
    allauthors = []
    for a in authordb["authors"]:
        allauthors.append(a)
    with open("authors.yaml", "w") as file:
        yaml.dump(allauthors, file)


def main():
    dbfile = os.path.normpath(os.path.join(".", "etc", "authordb.yaml"))

    with open(dbfile, "r") as fh:
        authordb = yaml.safe_load(fh)

    make_all(authordb)
    subprocess.call("bin/db2authors.py", shell=True)


if __name__ == '__main__':
    main()
