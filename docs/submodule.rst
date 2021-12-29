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

   export TEXMFHOME = lsst-texmf/texmf

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

    git submodule update --init

Updating a submodule
====================

The lsst-texmf captures the state of the lsst-texmf project at the time the submodule was added to your document.
This is convenient: others can update lsst-texmf, change default options, adjust formatting options, and so on, without any risk of changes to your document.
Occasionally, though, you will need to update your submodule to match the latest version of lsst-texmf.
This is a two step process: you first need to fetch the latest changes, then you commit them to your own repository.
If you need to update your lsst-texmf submodule, for example to use a newly-available bibliography reference, you execute:

.. code-block:: bash

    git submodule update --remote lsst-texmf

Keep in mind that this will also update the texmf code, so you may have to resolve any incompatibilities.
This change (to the submodule hash) can then be added and commited to your repo like any other.

If you decide you want to revert this update before committing it, you execute:

.. code-block:: bash

    git submodule update lsst-texmf

If you last updated the submodule prior to the default branch transition, you will need to do this prior to the ``git submodule update``:

.. code-block:: bash

    cd lsst-texmf
    git branch -m master main
    git fetch origin
    git branch -u origin/main main
    git remote set-head origin -a
    cd ..

Editing a submodule
===================

In general, it's easiest to use a local ``.bib`` file (see :ref:`the documentation on bibliographies <lsstdoc-bib>`) or ``myacronyms.txt``/``myglossarydefs.csv`` (:ref:`documentation <lsstdoc-acr>`) while you are working on the text of your document, and only make updates to lsst-texmf just before you are ready to merge your work to the document's ``main`` branch.

If you would like to edit the lsst-texmf submodule in place, rather than cloning it separately, for example to add a bibliography reference, you execute:

.. code-block:: bash

    cd lsst-texmf
    git checkout main

Then pull, branch, edit, commit, push, and merge as usual within the submodule.
Again, when you commit any changes to your repo, the new submodule hash should be added and committed as well.

If you last updated the submodule prior to the default branch transition, you will need to do this first:

.. code-block:: bash

    cd lsst-texmf
    git branch -m master main
    git fetch origin
    git branch -u origin/main main
    git remote set-head origin -a
