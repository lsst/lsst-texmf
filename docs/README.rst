.. image:: https://img.shields.io/badge/lsst-texmf-lsst.io-brightgreen.svg
   :target: https://lsst-texmf.lsst.io
.. image:: https://travis-ci.org/lsst/lsst-texmf.svg
   :target: https://travis-ci.org/lsst/lsst-texmf
..
  Uncomment this section and modify the DOI strings to include a Zenodo DOI badge in the README
  .. image:: https://zenodo.org/badge/doi/10.5281/zenodo.#####.svg
     :target: http://dx.doi.org/10.5281/zenodo.#####

######################
The LSST Latex Classes
######################

How to use the LSST Latex classes.

View this guide at https://lsst-texmf.lsst.io or see a preview of the current version in `this repo`_.



Build this software guide
=========================

You can clone this repository and build the guide locally with `Sphinx`_

.. code-block:: bash

   git clone https://github.com/lsst/lsst-texmf
   cd lsst-texmf/docs
   pip install -r requirements.txt
   make html

.. note::

   In a Conda_ environment, ``pip install -r requirements.txt`` doesn't work as expected.
   Instead, ``pip`` install the packages listed in ``requirements.txt`` individually.

The built guide is located at ``docs/_build/html/index.html``.

Editing this software guide
===========================

You can edit the ``index.rst`` file, which is a reStructuredText document.
The `DM reStructuredText Style Guide`_ is a good resource for how we write reStructuredText.

Remember that images and other types of assets should be stored in the ``_static/`` directory of this repository.
See ``_static/README.rst`` for more information.

The published guide at https://lsst-texmf.lsst.io will be automatically rebuilt whenever you push your changes to the ``main`` branch on `GitHub <https://github.com/lsst/lsst-texmf>`_.

Updating metadata
=================

This guide's metadata is maintained in ``metadata.yaml``.
In this metadata you can edit the guide's title, authors, publication date, etc..
``metadata.yaml`` is self-documenting with inline comments.

****

Copyright 2017 Association of Universities for Research in Astronomy

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.

.. _Sphinx: http://sphinx-doc.org
.. _DM reStructuredText Style Guide: https://developer.lsst.io/docs/rst_styleguide.html
.. _this repo: ./index.rst
.. _Conda: http://conda.pydata.org/docs/
