.. _install:

#####################
Installing lsst-texmf
#####################

You can get the LSST LaTeX classes and style files from GitHub:

.. code-block:: bash

   git clone https://github.com/lsst/lsst-texmf

To enable LaTeX to find the style files the :envvar:`TEXMFHOME` environment variable can be set to the :file:`texmf` subdirectory.
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
