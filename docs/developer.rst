.. _developer:

#####################
Developing lsst-texmf
#####################

.. _editing-class-files:

Editing the class files
=======================

Changes can be made to any of the files in the ``lsst-texmf`` repository by submitting a pull request in the normal manner.
Travis jobs automatically run when a PR is created to ensure that nothing has been broken and a pull request can only be merged if these checks pass.
Please obtain reviews of any non-trivial changes to ``.cls`` and ``.sty`` files.

If new files are added to or old ones removed from the :file:`texmf` directory, please remember to run :command:`texhash` in that directory in order to update the :file:`ls-R` file.
This file is committed to the repository such that end users do not have to remember to update it themselves.

.. _updating-bibliographies:

Updating bibliographies
=======================

One goal of a shared repository containing the LSST LaTeX files, is to provide a shared source of truth for references to other documents.
If a document is being cited that is not part of the current list, a pull request should be made, preferably using a ticket branch related to the main document development.
If the automated tests pass, the PR can be self-merged without review.
In this way, we can ensure that all documents agree on references without duplication and with minimum overhead.
Reminder that author lists in bibliography entries should use and to separate authors thus "William O'Mullane and Tim Jenness".

For new documents made with sqrbot-jr a file will be created called ``bibentry.txt`` which will contain a bib entry for
the the document which could be added to the appropriate local bibfile.
This should be a temporary measure as the entry should appear in lsst.bib the next day.

A githubaction ``generatebib`` runs daily and gathers all the metadata from notes published on lsst.io and adds them to ``lsst.bib``.
This covers all notes created with sqrbot-jr.
Other documents from docushare still need to be manually added in ``etc/static-entries.bib``.
This action may also be manually run (for the impatient).
It results in a pull-request which may be merged after CI passes.

For older LaTeX documents a script ``lsstdoc2bib.py`` exists in the bin folder of lsst-texmf which attempts to get info from the
tex macros of the document. Run it with the main file and the meta file like:``lsstdoc2bib.py meta.tex DMTN-nnn.tex`` where DMTN-nnn is the tex of the document you want the entry for. Its not very robust but gives you a start.

Bibliography file organization
------------------------------

* :file:`lsst.bib` includes LSST documents (DocuShare documents and technical notes).
  Any document available on DocuShare should use the ``@DocuShare`` bib entry using the document handle as the key in the bib file.
  This file should never be edited  rather docushare entries should be added to ``etc/static-entries.bib`` this is merged with the generated entries from lsst.io with ``make lsst.bib``.
  One day DocuShare entries may also be auto-generated.
* :file:`lsst-dm.bib` includes LSST Data Management publications (ADS and non-ADS) and presentations.
  Do not include DocuShare items in this file.
  Presentations should use a key of form ``YYYYauthor-meeting``.
* :file:`refs_ads.bib` includes any reference that can be found on ADS (aside from those in :file:`lsst-dm.bib`).
  Entries must be the standard ADS bibtex export and use the ADS Bibcode.
  This file should be used for arXiv entries obtained from ADS.
* :file:`refs.bib` should be used for non-LSST references that can not be located on ADS.
* :file:`books.bib` should be used for books that are not indexed by ADS.
* :file:`ivoa.bib` should be used for IVOA specs indexed ADS.

%-escaping for Sphinx
---------------------

Sphinx documents also use ``lsst-texmf``\ ’s bibliographies through `sphinxcontrib-bibtex <http://sphinxcontrib-bibtex.readthedocs.io/en/latest/>`_.
The Sphinx workflow requires that any non-comment ``%`` character be escaped.
ADS includes un-escaped ``%`` characters in URLs for A&A journal articles, for instance.
To work around this for now, ensure that these URLs are escaped (that is: ``\%``).
Travis CI is testing bibliographies for Sphinx compatibility.

See :jira:`DM-11358` for progress towards resolving this issue.

.. _updating-examples:

Updating examples and tests
===========================

We welcome additional example files to be added to the :file:`examples` directory and test files to be added to the :file:`tests` directory.
If new features are added to class or style files, it is helpful to add example code that uses these features to allow them to be tested.
Once new files are added, ensure that they are built correctly by the :file:`Makefile` since that file is used to build the tests and examples on Travis.
Be sure to document your example in the :ref:`examples` page.

.. _contrib-docs:

Contributing documentation
==========================

This documentation site is produced by Sphinx from the :file:`docs/` repository directory, and published with LSST the Docs to https://lsst-texmf.lsst.io.
For more information on writing reStructuredText-formatted documentation, see `DM's reStructuredText Style Guide <https://developer.lsst.io/docs/rst_styleguide.html>`_.
You can contribute to the documentation using `DM's normal workflow <https://developer.lsst.io/processes/workflow.html>`_.
When you have pushed a ticket branch to GitHub, you can find a rendered draft at https://lsst-texmf.lsst.io/v.
The main site at https://lsst-texmf.lsst.io updates automatically once your PR is merged to ``main``.

.. _contrib-docker:

Maintaining the Docker distribution
===================================

Docker images are automatically published as `lsstsqre/lsst-texmf`_ on Docker Hub through Travis CI.
Contributors shouldn't need to worry about updating the Docker distribution.

The following tags are generated through Travis:

- ``latest`` corresponds to ``main`` on GitHub.
- Tags also correspond to git branches and tags on GitHub.
  The build system converts forward slashes in branch names to dashes in tags.
  For example, the ``tickets/DM-10642`` Git branch is published on Docker Hub as ``tickets-DM-10642``.
- ``travis-N`` tags correspond to individual Travis CI builds.

The following components are involved in the Docker toolchain:

- The ``Dockerfile`` defines the container.
  Note that ``lsst-texmf``\ ’s :file:`Dockerfile` is only concerned with installing ``lsst-texmf`` and setting :envvar:`TEXMFHOME`.
  The `lsstsqre/lsst-texlive`_ base image provides `TeX Live`_ and tools like :command:`make` and :command:`git`.
- The ``.travis.yml`` file runs the Docker image build and push in the Travis CI environment.
- The ``bin/travis-docker-deploy.sh`` script tags the images according to the above scheme and pushes those images to Docker Hub.

.. _`lsstsqre/lsst-texmf`: https://hub.docker.com/r/lsstsqre/lsst-texmf/
.. _`lsstsqre/lsst-texlive`: https://hub.docker.com/r/lsstsqre/lsst-texlive/
.. _`TeX Live`: http://tug.org/texlive/
