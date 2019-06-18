.. _lsstdoc:

################################
Using the lsstdoc document class
################################

The :file:`lsstdoc` document class should be used for all LaTeX LSST documents.
The class file defines the document fonts and page dimensions, imports commonly used packages, defines journal macros and other common commands and defines the main title page and the page headers and footers.
In this section we will explain how to use ``lsstdoc``.

.. seealso::

   - :ref:`document-template`
   - :ref:`examples`

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

.. _lsstdoc-macros:

Class-specific Macros
---------------------

This class defines a number of macros that can be used in LSST documents.

Class-specific Environments
---------------------------

The ``note``, ``warning`` and ``draftnote`` environments are used to call out text into colored boxes for extra emphasis.
They each take an optional argument that can be used to title the box.
For ``note`` environments this title overrides the default text, for the other environments this optional argument augments the text.

.. code-block:: latex

   \begin{note}[Note title]
     Text for display in box goes here.
   \end{note}

The ``draftnote`` environment is special in that the contents of these notes only appear when a document is in draft mode.

.. _lsstdoc-bib:

Bibliographies
==============

In :file:`lsstdoc.cls` the bibliography style is forced to use :file:`lsst_aa.bst` to ensure that all documents look the same.
A number of standard bibliography database files are available from this package and can be added to the search path in addition to local bibliography files:

.. code-block:: latex

  \bibliography{lsst,lsst-dm,refs,books,refs_ads}

Detailed descriptions of these different files can be found below in :ref:`updating-bibliographies`, but can be summarized as:

lsst
    LSST DocuShare entries and tech notes.
lsst-dm
    Publications relating to LSST by members of the Data Management team.
    This includes unpublished presentations.
refs_ads
    Entries obtained from ADS, including arXiv.
refs
    Miscellaneous non-LSST documents which have no entry on ADS.
books
    Books which have no entry on ADS.

References should be placed at the end of the document but can come before any appendices.

During development, a local ``.bib`` file can be used in addition to the standard files.

.. code-block:: latex

  \bibliography{ldm-nnn,lsst,refs,books,refs_ads}

When a document has been finalized and ready for release, those entries should be moved out of the local file and added to the relevant files in the global database.
This enables a single known set of references to exist.

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
   \citep[e.g.,][]{LSE-163}

results in this output:

::

  LDM-151, SRD, [LDM-151], [DMSR], [1], [e.g., 3]

where the final two examples would be the reference number.
If the ``authoryear`` class option is enabled the resulting output is:

::

  LDM-151, SRD, [LDM-151], [DMSR], (Jurić et al., LDM-151), (e.g., Juric et al., LSE-163)

Where the author is used rather than a number but for ``@DocuShare`` Bibtex entries the year is replaced by the document handle.
This is indicative of DocuShare documents evolving over time, such that the handle is more relevant than the particular year.

Acronyms or Glossaries
======================
A global glossary and acronym files exists in ``lsst-texmf/etc/glossarydefs.csv``.   This file has the follwing format:

.. code-block:: latex
   Term,Description,Subsystem Tags,Documentation Tags,Associated Acronyms and Alternative Terms

One should not particulalry the Subsystem Tags which may be used to diffentiate acronyms which are overloaded. 

This file is read and processed in conjunction with your tex files by ``bin/generateAcronyms.py``. 
This script expects to find two txt files in the directory with the tex:
* ``skipacronyms.txt`` :  one item per liine which should be ignored.

It has two modes of operation:

Acronyms
--------
calling ``generateAcronyms.py`` with a list of tex files will parse the tex files looking for acronyms which exist in ``lsst-texmf/etc/glossarydefs.csv``

Glossary
--------
