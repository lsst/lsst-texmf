.. _install:

###################################
Using lsst-texmf as a Git submodule
###################################

Instead of a :doc:`centralized installation of lsst-texmf <install>`, many LSST documents include a specific copy of lsst-texmf as a Git submodule.
This page describes how to set up a document repository to use an lsst-texmf submodule, and how to work with these repositories.

Adding a lsst-texmf submodule
=============================

To install lsst-texmf as a Git submodule, execute this within your document's repository:

.. code-block:: bash

   git submodule add https://github.com/lsst/lsst-texmf
    
Add and commit as usual.

Second, ensure that the document's :file:`Makefile` uses the lsst-texmf submodule.
Typically, you can do this exporting the ``TEXMFHOME`` at the beginning of the Makefile:

.. code-block:: make

   export TEXMFHOME = lsst-texmf/texmf

If your :file:`Makefile` uses scripts in the :file:`lsst-texmf/bin` directory, you can point to that script relative to the ``$TEXMFHOME`` directory.
For example:

.. code-block:: make

   acronyms.tex :$(tex) myacronyms.txt skipacronyms.txt
       python3 ${TEXMFHOME}/../bin/generateAcronyms.py $(tex)

Lastly, it's a good idea to include the ``git submodule`` code snippet from the next section in the document's README to remind others how to set up the submodule.

Cloning a document Git repository with a submodule
==================================================

When making a fresh clone of the repository, you will have to execute this within the repository:

.. code-block:: bash

    git submodule init
    git submodule update
