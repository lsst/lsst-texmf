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

Some things to remember:

* LSST documents are added to :file:`lsst.bib`.
  Any document available on DocuShare should use the ``@DocuShare`` bib entry using the document handle as the key in the bib file.
  In the longer term, this file will be auto-generated from DocuShare and should always be up to date and should not require manual editing.
  Tech notes will also be defined in this file.
* Any reference that can be found on ADS should be stored in :file:`refs_ads.bib` using the standard ADS bibtex export.
  ADS entries should always be cited using the ADS Bibcode.
  This file should be used for arXiv entries obtained from ADS.
* :file:`refs.bib` should be used for non-LSST references that can not be located on ADS.
* :file:`books.bib` should be used for books that are not indexed by ADS.

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
The main site at https://lsst-texmf.lsst.io updates automatically once your PR is merged to ``master``.
