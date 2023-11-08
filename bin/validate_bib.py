#!/usr/bin/env python
"""Ensure that lsst-texmf bibliographies can be opened by pybtex [1].

pybtex compatibility is required for Sphinx documentation workflows.  This also
helps us discover issues like unescaped ``%`` signs and duplicate keys.

[1] https://docs.pybtex.org/
"""

import argparse
import os
import sys

import latexcodec  # noqa provides the latex+latin codec
from pybtex.database.input import bibtex


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", help="Paths to bib files.")
    args = parser.parse_args()

    # Validate input paths
    for bibpath in args.paths:
        if not os.path.exists(bibpath):
            print("Cannot find bib for testing: {}".format(bibpath))
            sys.exit(1)

    parser = bibtex.Parser()
    for bibpath in args.paths:
        print("Parsing {}".format(bibpath))
        parser.parse_file(bibpath)


if __name__ == "__main__":
    main()
