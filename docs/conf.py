#!/usr/bin/env python
#
# Sphinx configuration file
# see metadata.yaml in this repo for to update document-specific metadata

import os
from documenteer.designdocs import configure_sphinx_design_doc

from pybtex.style.formatting.plain import Style as PlainStyle
from pybtex.style.formatting import toplevel
from pybtex.plugin import register_plugin
from pybtex.style.template import (
    join, field, sentence, tag, optional_field, href, first_of, optional
)


# Ingest settings from metadata.yaml and use documenteer's
# configure_sphinx_design_doc to build a Sphinx configuration that is
# injected into this script's global namespace.
metadata_path = os.path.join(os.path.dirname(__file__), 'metadata.yaml')
with open(metadata_path, 'r') as f:
    confs = configure_sphinx_design_doc(f)
g = globals()
g.update(confs)


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
