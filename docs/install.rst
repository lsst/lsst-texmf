.. _install:

#####################
Installing lsst-texmf
#####################

There are three ways to install and use lsst-texmf: as a single centralized installation on your computer, as a submodule of individual document Git repositories, and as a Docker container.
This page describes how to install lsst-texmf centrally.
See :doc:`submodule` and :doc:`docker` for the other approaches.

To install lsst-texmf, clone the lsst-texmf repository:

.. code-block:: bash

   git clone https://github.com/lsst/lsst-texmf

To enable LaTeX to find the style files the :envvar:`TEXMFHOME` environment variable can be set to the :file:`texmf` subdirectory.
For example, the following can be used if you are in the directory from which you cloned the repository:

.. code-block:: bash

   export TEXMFHOME=`pwd`/lsst-texmf/texmf

If you do not want to override this environment setting but wish to have the files always available you can move the entire :file:`texmf` tree to the default home location which can be found using:

.. code-block:: bash

   kpsewhich -var-value TEXMFHOME

On a Mac this is :file:`~/Library/texmf`.

Once this environment variable is set, :command:`xelatex` and :command:`pdflatex` will find the relevant files automatically.

.. note::

   :command:`xelatex` is the modern version of :command:`pdflatex` that has support for more modern native fonts and Unicode.
   The :file:`lsstdoc.cls` class and the :file:`LSST-beamer.sty` adjust correctly when :command:`xelatex` is being used.
   More information on :command:`xelatex` can be found at https://en.wikipedia.org/wiki/XeTeX.
   Consider using :command:`xelatex` for all documents.
   Use the ``-xelatex`` option for the :command:`latexmk` command, rather than ``-pdf``.
