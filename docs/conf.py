#!/usr/bin/env python
#
# Sphinx configuration file
# see metadata.yaml in this repo for to update document-specific metadata

import os
from documenteer.designdocs import configure_sphinx_design_doc

# Ingest settings from metadata.yaml and use documenteer's
# configure_sphinx_design_doc to build a Sphinx configuration that is
# injected into this script's global namespace.
metadata_path = os.path.join(os.path.dirname(__file__), 'metadata.yaml')
with open(metadata_path, 'r') as f:
    confs = configure_sphinx_design_doc(f)
g = globals()
g.update(confs)
