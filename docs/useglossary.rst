.. _useglossary:

###########################
Using the Glossary function
###########################

A global glossary and acronym files exists in ``lsst-texmf/etc/glossarydefs.csv``.
The ``generateAcronyms.py`` script uses this file to generate acronyms or glossaries for TeX documents.
The acronym function is on by default when you use sqrbot to create a new document.
It will scan the TeX files as part of the make and generate ``acronyms.tex`` containing a table of acronyms found int he document which may be included.
It will report any acronym type constructs which it could not match.

Switch to glossary
==================

To use the glossary a series of small changes need to be made, these are mostly commented out in
the relevant files.

Change Makefile
---------------

In the Makefile we need to make ``aglossary.tex`` rather than acronyms.tex.
You may copy the acronyms lines or replace them to get (in Makefile):

.. code-block:: sh

    aglossary.tex: $(tex) myacronyms.txt
	$(TEXMFHOME)/../bin/generateAcronyms.py -gt "DM" $(tex)

Also in the Makefile make sure your document depends on aglossary.tex and that wildcard listing excludes aglossary.
If you have the standard Makefile simply search for acronyms.tex and replace it with aglossary.tex, there should be two occurrences somewhat like this:

.. code-block:: sh

   tex = $(filter-out $(wildcard *aglossary.tex) , $(wildcard *.tex))

and

.. code-block:: sh

   $(DOCNAME).pdf: $(tex) meta.tex local.bib authors.tex aglossary.tex

The makeglossaries must also be invoked and an extra build is needed as follows:

.. code-block:: sh

   $(DOCNAME).pdf: $(tex) meta.tex local.bib authors.tex aglossary.tex
        xelatex  $(DOCNAME)
        makeglossaries $(DOCNAME)
        xelatex $(DOCNAME)

Depending on your document this may be latexmk or some other command but makeglossaries needs to be added in a similar manner.

Change the doc
--------------
If you are not using ``lsstdoc.cls`` you may need to include the glossary package:


.. code-block:: latex

 \usepackage[nonumberlist,nogroupskip,toc,numberedsection=autolabel,style=index]{glossaries}


Within the document some slight changes are needed.
Before ``\begin{document}`` the glossary file needs to be included and makeglossaries invoked, like this:

.. code-block:: latex

   \input{aglossary}
   \makeglossaries


If you have an ``\input{acronyms}`` anywhere it should be removed.

In the part of the document where you wish to see the glossary (an appendix perhaps)
include the glossary command:

.. code-block:: latex

   \printglossaries

Using update
============
If you have done the above steps and invoked make you probably have no glossary since no term is marked up with
``\gls{}``.
If you have the ``aglossary.tex`` the script may be invoked on a TeX file to adorn found definitions with ``\gls{}``.
This modifies your TeX file so make sure it is still ok after invoking the script.
You may manually mark up also without problem. But an example invocation would be.


.. code-block:: sh

   generateAcronyms.py -u body.tex

.. important::

   We do not suggest adding ``generateAcronyms.py`` with the ``-gu`` flags to Makefile as it occasionally does something unexpected so you should run it and check the result by building the document.

This will modify body.tex adding ``gls{}`` in appropriate places. It is imperfect and will not get all instances of a term, it may also do things you don't like hence check after running!

Tags
====
Tags may be used to differentiate terms which are overloaded.
You may specify multiple tags and they will be used in the order passed.
The default tag mode for new documents is 'DM'.

In the Makefile you may see:

.. code-block:: sh

   $(TEXMFHOME)/../bin/generateAcronyms.py -gt "DM" $(tex)


One could specify:

.. code-block:: sh

   $(TEXMFHOME)/../bin/generateAcronyms.py -gt "DM OPS" $(tex)

to take first DM definition and then the OPS definition



Other files
===========
``generateAcronyms.py``  script expects to find two text files in the directory with the tex:

:file:`skipacronyms.txt`
   Specifies abbreviations which should be omitted from the glossary.
   One line per abbreviation.

:file:`myacronyms.txt`
   Defines abbreviations which are specific to this document.
   One line per abbreviation, formatted as ``Abbreviation:Definition`` (e.g. ``CI:Continuous Integration``).

   **OR**

:file:`myglossarydefs.csv`
   Defines abbreviations and glossary entries which are specific to this document.
   One line per definition os the same format as glossarydefs.csv given above.
   Only read if myacronyms.txt does not exist.


.. note::
   Only one of myacronyms.txt or myglossarydefs.csv is used you should not have both files.
   If you have both only myacronyms.txt is used.


