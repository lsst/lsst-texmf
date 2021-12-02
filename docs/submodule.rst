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

If you need to update your lsst-texmf submodule, for example to use a newly-available bibliography reference, you execute:

.. code-block:: bash

    git submodule update --remote lsst-texmf

Keep in mind that this will also update the texmf code, so you may have to resolve any incompatibilities.
When you commit any changes to your repo, the new submodule hash will be committed as well.

If you decide you want to revert this update before committing it, you execute:

.. code-block:: bash

    cd lsst-texmf
    git checkout $(cat ../.git/modules/lsst-texmf/HEAD)
    cd ..

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

If you would like to edit the lsst-texmf submodule in place, rather than cloning it separately, for example to add a bibliography reference, you execute:

.. code-block:: bash

    cd lsst-texmf
    git checkout main

Then pull, edit, commit, push, and merge as usual within the submodule.
Again, when you commit any changes to your repo, the new submodule hash will be committed as well.

If you last updated the submodule prior to the default branch transition, you will need to do this first:

.. code-block:: bash

    cd lsst-texmf
    git branch -m master main
    git fetch origin
    git branch -u origin/main main
    git remote set-head origin -a
