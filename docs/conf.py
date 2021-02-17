#!/usr/bin/env python
#
# Sphinx configuration file
# see metadata.yaml in this repo for to update document-specific metadata

import os

import sphinx_rtd_theme
from documenteer.sphinxconfig.utils import form_ltd_edition_name


extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx-prompt',
    'sphinxcontrib.bibtex',
    'documenteer.sphinxext',
    'documenteer.sphinxext.bibtex',
]

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

version = form_ltd_edition_name(
    git_ref_name=os.getenv('TRAVIS_BRANCH', default='master'))
# The full version, including alpha/beta/rc tags.
release = version

project = 'lsst-texmf: The LSST LaTeX Classes'
html_title = project
html_short_title = 'lsst-texmf'

author = 'LSST Data Management'

copyright = '2017-2021 Association of Universities for Research in Astronomy (AURA), Inc.'

master_doc = 'index'

html_context = {
    # Enable "Edit in GitHub" link
    'display_github': True,
    'github_user': 'lsst',
    'github_repo': 'lsst-texmf',
    # TRAVIS_BRANCH is available in CI, but master is a safe default
    'github_version': os.getenv('TRAVIS_BRANCH', default='master') + '/docs/'
}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/lsst-logo-dark.svg'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['README.rst', '_build']

source_encoding = 'utf-8'

# BibTeX configuration
bibtex_bibfiles = [
    '../texmf/bibtex/bib/lsst.bib',
    '../texmf/bibtex/bib/books.bib',
    '../texmf/bibtex/bib/lsst-dm.bib',
    '../texmf/bibtex/bib/refs.bib',
    '../texmf/bibtex/bib/refs_ads.bib',
]

# Intersphinx configuration.
# http://www.sphinx-doc.org/en/stable/ext/intersphinx.html
intersphinx_mapping = {}
