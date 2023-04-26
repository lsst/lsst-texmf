.. _overleaf:

##############################
Using lsst-texmf with Overleaf
##############################

If you wish to edit a ``lsst-texmf`` document such as a technote on Overleaf, some modifications are required.
The recommended procedure is detailed below.

First, create a fork of the document repository on GitHub to your local GitHub account.
Working from a locally forked version of the repository is desirable as the Overleaf Git system does not support branches.
Any edits made and pushed back to Overleaf will therefore live on the ``main`` branch of whatever repository you're pushing back to.
If you're comfortable with incremental edits being pushed to the main repo, then you do not need to fork the repository.

Once you have a repository in place, clone the repository and all submodules to your local machine:

.. code-block:: bash

   git clone --recurse-submodules git@github.com/USERNAME/MYREPO.git

Submodules are not recognized by the Overleaf Git system.
To work around this, the necessary components of the ``lsst-texmf`` submodule must be copied into a stand-alone directory:

.. code-block:: bash

   cp -av lsst-texmf/texmf texmf

.. note::
   This may require periodic manual updates to the ``texmf`` directory if the ``lsst-texmf`` submodule is updated.

A final limitation of the Overleaf Git system is that symbolic links are not supported.
Fortunately, the one symbolic link in the ``lsst-texmf`` submodule is not required for document compilation and can safely be removed:

.. code-block:: bash

   rm texmf/tex/LSST-themes/default

To support use of the ``lsst-texmf`` document class in Overleaf, we need to define a number of environment variables.
Create a file named ``latexmkrc`` in the root of the repository with the following contents:

.. code-block:: bash

   $ENV{'TZ'}='America/Los_Angeles';
   $ENV{'TEXMFHOME'}='./texmf';
   $ENV{'TEXINPUTS'}='./texmf//:' . $ENV{'TEXINPUTS'};
   $ENV{'BSTINPUTS'}='./texmf//:' . $ENV{'BSTINPUTS'};

At this point, the repository should be ready to compile locally.
To build the document locally, run ``make``.
This will create the document PDF and a number of ancilliary files.
We will need to add two of these ancilliary files to the repository to support Overleaf:

.. code-block:: bash

      git add -f meta.tex
      git add -f acronyms.tex

You may now also git commit the other remaining files in the repository.

.. note::
   If you wish to clean up the temporary files created by ``make``, run ``make clean``.
   This step is not necessary, but may be desirable for some users.
   Make sure not to run this until after you have pushed your commit to GitHub, as ``make clean`` will remove the ``meta.tex`` file.

Once the changes above are made, the repository can be pushed to GitHub.

Next, create a new project on Overleaf and choose ``Import from GitHub``.
Select the repository from the list and allow Overleaf to import the project.

Once the project has been imported, in the Overleaf menu under Settings switch the compiler to ``LuaLaTex``.
In the same settings menu, set the Main document to the primary ``AAATN-NNN.tex`` file.

Your Overleaf document should now be ready to work on and compile.
You may wish to periodically commit your Overleaf edits back to GitHub via ``Menu``; ``GitHub``; ``Push Overleaf changes to GitHub``.
This will allow you to pull those changes into your local clone and re-run ``make``, to update the ``acronyms.tex`` file, and then push back to GitHub and pull back into Overleaf.
