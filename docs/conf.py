#!/usr/bin/env python
#
# Sphinx configuration file
# see metadata.yaml in this repo for to update document-specific metadata

from documenteer.conf.guide import *  # noqa


# BibTeX configuration
bibtex_bibfiles = [
    '../texmf/bibtex/bib/lsst.bib',
    '../texmf/bibtex/bib/books.bib',
    '../texmf/bibtex/bib/lsst-dm.bib',
    '../texmf/bibtex/bib/refs.bib',
    '../texmf/bibtex/bib/refs_ads.bib',
]

# Feel free to experiment with other options
bibtex_default_style = "lsst_aa"
bibtex_reference_style = "author_year"
