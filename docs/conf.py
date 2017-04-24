#!/usr/bin/env python
#
# Sphinx configuration file
# see metadata.yaml in this repo for to update document-specific metadata

import os

import sphinx_rtd_theme
from documenteer.sphinxconfig.utils import form_ltd_edition_name

from pybtex.style.formatting.plain import Style as PlainStyle
from pybtex.style.formatting import toplevel
from pybtex.plugin import register_plugin
from pybtex.style.template import (
    join, field, sentence, tag, optional_field, href, first_of, optional
)


extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx-prompt',
    'sphinxcontrib.bibtex',
    'documenteer.sphinxext'
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

copyright = '2017 Association of Universities for Research in Astronomy, Inc.'

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


class LSSTStyle(PlainStyle):
    """Add a new style that understands DocuShare entries"""

    def format_docushare(self, e):
        default_url = join['https://ls.st/', field('handle', raw=True)]

        template = toplevel[
            sentence[tag('b')['[', href[default_url, field('handle')], ']']],
            self.format_names('author'),
            self.format_title(e, 'title'),
            sentence[field('year')],
            sentence[optional_field('note')],
            # Use URL if we have it, else provide own
            first_of[
                optional[
                    self.format_url(e)
                ],
                # define our own URL
                sentence['URL', href[default_url, default_url]]
            ]
        ]
        return template.format_data(e)


register_plugin('pybtex.style.formatting', 'lsst_aa', LSSTStyle)

# Intersphinx configuration.
# http://www.sphinx-doc.org/en/stable/ext/intersphinx.html
intersphinx_mapping = {}
