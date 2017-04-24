.. _lsstdoc:

################################
Using the lsstdoc document class
################################

The :file:`lsstdoc` document class should be used for all LaTeX LSST documents.
The class file defines the document fonts and page dimensions, imports commonly used packages, defines journal macros and other common commands and defines the main title page and the page headers and footers.
In this section we will explain how to create a document using the LSST document class.
A full example can be seen in the :file:`examples` directory in the repository.

.. Consider moving the macros into a separate style file in order to make it easier to document them.

.. _lsstdoc-preamble:

Document Preamble
=================

A LaTeX document begins with a preamble that sets up the document.
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
* ``authoryear`` enables author/year citations for the ``natbib`` package.
  The default is to use numbered citations.
  DocuShare references (via :command:`\citeds`) will still report the handle.

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

Some documents, have a secondary title that can be included as follows.
This is optional.

.. code-block:: latex

   \setDocSubtitle{A subtitle}

The document reference ("document handle" in DocuShare) is set next.
The ``\setDocRef`` command controls whether the document will be include change control messaging.
``LDM`` and ``LSE`` documents are in this category, but a ``DMTN`` will not display change control statements.

.. code-block:: latex

   \setDocRef{LDM-nnn}

Optionally, the document curator can be defined here.
LSST change-controlled documents do not require this information, but sometimes it is beneficial to indicate a point of contact who is not necessarily the person listed as author or the person most recently mentioned in the change record.

.. code-block:: latex

   \setDocCurator{A Person}

The abstract can be defined with this command and will be inserted in the correct place in the document preamble.

.. code-block:: latex

   \setDocAbstract{%
     This is an example abstract.
   }


The change record should be updated whenever a document is to be released (by a merge to ``master``).
For change-controlled documents, the change record should include the relevant RFC or LCR number.
The revision number should follow the policy defined in :cite:`LPM-51`.

.. code-block:: latex

   % Change history defined here. Will be inserted into
   % correct place with \maketitle
   % OLDEST FIRST: VERSION, DATE, DESCRIPTION, OWNER NAME
   \setDocChangeRecord{%
     \addtohist{1}{2017-09-10}{Initial release.}{A. Author}
     \addtohist{2}{yyyy-mm-dd}{Future changes}{Future person}
   }

.. _lsstdoc-body:

Document Body
=============

Once the preamble has been completed the document itself can begin and the title page created:

.. code-block:: latex

   \begin{document}
   \maketitle

This assumes that the ``toc`` option was given above.

After this the document can be written

.. _lsstdoc-bib:

Bibliographies
==============

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

* ``\citeds`` should be used for LSST DocuShare documents (and in the future tech notes).
  The output will show the document handle rather than the reference number.
* ``\citedsp`` is the same as ``\citeds`` but adds parentheses around the document handle.
* ``\citep`` should be used for non-LSST references.

The following LaTeX,

.. code-block:: latex

   \citeds{LDM-151},
   \citeds[SRD]{LPM-17},
   \citedsp{LDM-151},
   \citedsp[DMSR]{LSE-61},
   \citep{LDM-151},
   \citep[e.g.,]{LSE-163}

results in this output:

::

  LDM-151, SRD, [LDM-151], [DMSR], [1], [e.g., 3]

where the final two examples would be the reference number.

.. note::

   Currently the class file enforces number mode for citations.
   I'm not entirely sure we've really thought about this much.
