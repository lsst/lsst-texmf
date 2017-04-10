..
  Technote content.

  See https://developer.lsst.io/docs/rst_styleguide.html
  for a guide to reStructuredText writing.

  Do not put the title, authors or other metadata in this document;
  those are automatically added.

  Use the following syntax for sections:

  Sections
  ========

  and

  Subsections
  -----------

  and

  Subsubsections
  ^^^^^^^^^^^^^^

  To add images, add the image file (png, svg or jpeg preferred) to the
  _static/ directory. The reST syntax for adding the image is

  .. figure:: /_static/filename.ext
     :name: fig-label
     :target: http://target.link/url

     Caption text.

   Run: ``make html`` and ``open _build/html/index.html`` to preview your work.
   See the README at https://github.com/lsst-sqre/lsst-technote-bootstrap or
   this repo's README for more info.

   Feel free to delete this instructional comment.

:tocdepth: 1

.. Please do not modify tocdepth; will be fixed when a new Sphinx theme is shipped.

.. sectnum::

.. Add content below. Do not include the document title.

The LSST Latex Support Files
============================

The LSST `lsst-texmf <https://github.com/lsst/lsst-texmf>`_ package contains Latex document classes, style files, and bibliographies that can be used to help you write LSST documentation in Latex to match the project style.
You can get the LSST Latex classes and style files from Github:

.. code-block:: bash

   git clone https://github.com/lsst/lsst-texmf

To enable Latex to find the style files the :envvar:`TEXMFHOME` environment variable can be set to the :file:`texmf` subdirectory.
For example, the following can be used if you are in the directory from which you cloned the repository:

.. code-block:: bash

   export TEXMFHOME=`pwd`/lsst-texmf/texmf

A single :file:`texmf` directory can be reused for multiple documents, or else, it is possible to have separate :file:`texmf` directories for each document, having the environment variable set by a make file.
If you do not want to override this environment setting but wish to have the files always available you can move the entire :file:`texmf` tree to the default home location which can be found using:

.. code-block:: bash

   kpsewhich -var-value TEXMFHOME

which on a Mac reports :file:`~/Library/texmf`.

Once this environment variable is set, :command:`xelatex` and :command:`pdflatex` will find the relevant files automatically.

.. note::

  :command:`xelatex` is the modern version of :command:`pdflatex` that has support for more modern native fonts and Unicode.
  The :file:`lsstdoc.cls` class and the :file:`LSST-beamer.sty` adjust correctly when :command:`xelatex` is being used.
  More information on :command:`xelatex` can be found at https://en.wikipedia.org/wiki/XeTeX.
  Consider using :command:`xelatex` for all documents.
  Use the ``-xelatex`` option for the :command:`latexmk` command, rather than ``-pdf``.



Using the lsstdoc document class
================================

The :file:`lsstdoc` document class should be used for all Latex LSST documents.
The class file defines the document fonts and page dimensions, imports commonly used packages, defines journal macros and other common commands and defines the main title page and the page headers and footers.
In this section we will explain how to create a document using the LSST document class.
A full example can be seen in the :file:`examples` directory in the repository.

.. Consider moving the macros into a separate style file in order to make it easier to document them.

Document Preamble
-----------------

A Latex document begins with a preamble that sets up the document.
The first step is to define the class:

.. code-block:: latex

  \documentclass[DM,lsstdraft,toc]{lsstdoc}

The options for the document class control some of the layout:

* ``DM`` defines the document type to be a "Data Management" document.
  Other options include ``MN`` for minutes and ``CP`` for conference proceedings but these are holdovers from the original Gaia class file and currently have no effect on the document output.
  They are considered optional, but descriptive, at this time.
* ``lsstdraft`` declares that the document is a draft and results in a back ground image.
  For controlled documents this mode also disables the titlepage text indicating the document has been approved.
  Remove this option when the document is finalized and is ready to be released by merging to the ``master`` branch.
* ``toc`` enables a full table of contents to be included.
  This also results in the page style being reset to ``arabic``.
  For backwards compatibility reasons this is not the default, and furthermore, without this option the page style must be explicitly set to ``arabic`` by the document author.
  Leaving out this option enables the author to have more control over page counts and when the document properly begins.
  It is expected that most new documents written will enable this option.

This can be followed by any document-specific package imports and macros.
The document metadata must then be defined.
Title, author, and date match the standard commands required for ``\maketitle``, although a short title can be specified if a different title is to be used in the page headers.
The date for a draft document can float during development, but should be fixed once the document has been finalized and is to be merged to master.

.. code-block:: latex

  \title[Short title]{Title of document}

  \author{
    A.~Author,
    B.~Author,
    and
    C.~Author}

  \date{\today}

The document reference ("document handle" in DocuShare) is set next.
The ``\setDocRef`` command controls whether the document will be include change control messaging.
``LDM`` and ``LSE`` documents are in this category, but a ``DMTN`` will not display change control statements.


.. code-block:: latex

  \setDocRef{LDM-nnn}

The document status and revision number are not usually required for LSST documentation matching the project style, but currently must be set in the class as a holdover from the Gaia original.
The document revision is normally included in the change record, and the document status is currently draft (indicated by the use of the ``lsstdraft`` class option), or released (not in draft, change record indicating so).

.. code-block:: latex

  \setDocRevision{TBD}
  \setDocStatus{draft}

The abstract can be defined with this command and will be inserted in the correct place in the document preamble.

.. code-block:: latex

  \setDocAbstract{%
    This is an example abstract.
  }


The change record should be updated whenever a document is to be released (by a merge to ``master``).
For change-controlled documents, the change record should include the relevant RFC or LCR number.

.. code-block:: latex

  % Change history defined here. Will be inserted into
  % correct place with \maketitle
  % OLDEST FIRST: VERSION, DATE, DESCRIPTION, OWNER NAME
  \setDocChangeRecord{%
    \addtohist{1}{2017-09-10}{Initial release.}{A. Author}
    \addtohist{2}{yyyy-mm-dd}{Future changes}{Future person}
  }




Document Body
-------------

Once the preamble has been completed the document itself can begin and the title page created:

.. code-block:: latex

   \begin{document}
   \maketitle

This assumes that the ``toc`` option was given above.

After this the document can be written


Bibliographies
--------------

In :file:`lsstdoc.cls` the bibliography style is forced to use :file:`lsst_aa.bst` to ensure that all documents look the same.
A number of standard bibliography database files are available from this package and can be added to the search path in addition to local bibliography files:

.. code-block:: latex

  \bibliography{lsst,refs,books,refs_ads}

The descriptions of these different files can be found below in :ref:`updating-bibliographies`.
References should be placed at the end of the document but can come before any appendices.

During development, a local ``.bib`` file can be used in addition to the standard files.

.. code-block:: latex

  \bibliography{ldm-nnn,lsst,refs,books,refs_ads}

When a document has been finalized and ready for release, those entries should be moved out of the local file and added to the relevant files in the global database.
This enables a single known set of references to exist.

.. note::

  Should we cull the current ``.bib`` files (the non-lsst ones) so that they only include the references we are using?
  There are many Gaia entries in the current database that are never going to be cited by LSST docs.
  There are many ADS entries that are not used by LSST.
  Should ADS entries be kept up to date by querying ADS for the bibcodes?
  Sometimes information is updated (in particular SPIE entries).

References can be cited using the following commands:

* ``\citell`` should be used for LSST references (DocuShare and tech note).
  The output will show the document handle rather than the reference number.
* ``\citellp`` is the same as ``\citell`` but adds parentheses around the document handle.
* ``\citep`` should be used for non-LSST references.

.. note::

  Currently the class file enforces number mode for citations.
  I'm not entirely sure we've really thought about this much.

Writing Presentations
=====================

.. note::

  Initial text should be the README from the beamer directory written by Robert.


Editing the class files
=======================

Changes can be made to any of the files in the ``lsst-texmf`` repository by submitting a pull request in the normal manner.
Travis jobs automatically run when a PR is created to ensure that nothing has been broken and a pull request can only be merged if these checks pass.
Please obtain reviews of any non-trivial changes to ``.cls`` and ``.sty`` files.

If new files are added to or old ones removed from the :file:`texmf` directory, please remember to run :command:`texhash` in that directory in order to update the :file:`ls-R` file.
This file is committed to the repository such that end users do not have to remember to update it themselves.

Updating Examples and Tests
---------------------------

We welcome additional example files to be added to the :file:`examples` directory and test files to be added to the :file:`tests` directory.
If new features are added to class or style files, it is helpful to add example code that uses these features to allow them to be tested.
Once new files are added, ensure that they are built correctly by the :file:`Makefile` since that file is used to build the tests and examples on Travis.

.. _updating-bibliographies:

Updating Bibliographies
-----------------------

One goal of a shared repository containing the LSST Latex files, is to provide a shared source of truth for references to other documents.
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
