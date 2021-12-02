.. _submodule:

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

   export TEXMFHOME ?= lsst-texmf/texmf

.. note::

   Assignment using ``?=`` means you can choose another lsst-texmf tree by setting ``TEXMFHOME`` in your environment before running ``make``.

If your :file:`Makefile` uses scripts in the :file:`lsst-texmf/bin` directory, you can point to that script relative to the ``$TEXMFHOME`` directory.
For example:

.. code-block:: make

   acronyms.tex :$(tex) myacronyms.txt skipacronyms.txt
       python3 ${TEXMFHOME}/../bin/generateAcronyms.py -t "DM" $(tex)

Lastly, it's a good idea to include the ``git submodule`` code snippet from the next section in the document's README to remind others how to set up the submodule.

Cloning a document Git repository with a submodule
==================================================

When making a fresh clone of the repository, you will have to execute this within the repository:

.. code-block:: bash

    git submodule init
    git submodule update

Updating the submodule
======================

The lsst-texmf captures the state of the lsst-texmf project at the time the submodule was added to your document.
This is convenient: others can update lsst-texmf, change default options, adjust formatting options, and so on, without any risk of changes to your document.
Occasionally, though, you will need to update your submodule to match the latest version of lsst-texmf.
This is a two step process: you first need to fetch the latest changes, then you commit them to your own repository.
Proceed as follows:

.. code-block:: bash

   git subdmodule update --remote
   git commit lsst-texmf/ -m "Update to latest lsst-texmf"

Sometimes, of course, you don't want to just fetch the latest changes, but to commit your own changes to lsst-texmf.
Typically, this is because you want to add new entries to the included BibTeX database or to the glossary.
In general, it's easiest to use a local ``.bib`` file (see :ref:`the documentation on bibliographies <lsstdoc-bib>`) or ``myacronyms.txt``/``myglossarydefs.csv`` (:ref:`documentation <lsstdoc-acr>`) while you are working on the text of your document, and only make updates to lsst-texmf just before you are ready to merge your work to the document's ``main`` branch.
The following procedure, which assumes you are are working on ticket DM-ABCDE, should do the trick:

#. Ensure that your copy of lsst-texmf is fully updated, following the instructions above.
#. Change to the :file:`lsst-texmf` directory, and make a new ticket branch there:

   .. code-block:: bash

      cd lsst-texmf
      git checkout -b tickets/DM-ABCDE

#. Make the changes you need within the lsst-texmf tree.
   Refer to the documentation on :ref:`updating-bibliographies` for guidance.
#. Commit your changes, and push the ticket branch to the lsst-texmf repository:

   .. code-block:: bash

     git commit -a -m "Updated glossary and bibliography"
     git push origin tickets/DM-ABCDE

#. Go to GitHub, open a PR, and get your changes merged to ``main``.
   Note that changes to the bibliography files can be self-merged without review if all automated tests pass.
#. Go back to your main document (that is, leave the :file:`lsst-texmf` directory) and use the same procedure as above to update to the latest version of lsst-texmf's ``main`` branch.

Your document should now be updated to the latest version of lsst-texmf, including the changes you have just made.
You can remove any local bibliography files or acronym overrides, and then proceed as usual to push your changes and submit them for review.
