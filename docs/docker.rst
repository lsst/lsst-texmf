.. _docker:

############################
Using lsst-texmf with Docker
############################

Besides installing ``lsst-texmf`` on your computer, you can compile ``lsst-texmf``\ -based documents with Docker.
This setup is useful for continuous integration environments since it avoids having to re-install `TeX Live`_ and ``lsst-texmf`` in each build.
A Docker workflow is also useful for local writing since it turns ``lsst-texmf`` installation and document compilation into a single command.
There's no need to worry about installing LaTeX dependencies and setting a :envvar:`TEXMFHOME` environment variable.

.. _docker-quick-start:

Quick start
===========

To get started, you'll need to `install Docker`_.

Then from your LaTeX document's directory, run:

.. code-block:: bash

   docker run --rm -v `pwd`:/build -w /build lsstsqre/lsst-texmf:latest sh -c 'make'

Here's what's happening:

- ``docker run`` downloads the Docker image (if necessary) and runs a container.
- ``--rm`` removes the container once the run completes.
- ``lsstsqre/lsst-texmf:latest`` is the name of the Docker image.
  This tracks the ``master`` branch of the `lsst-texmf GitHub repository`_.
- ``-v `pwd`:/build`` *binds* the current directory (containing your document) into the ``/build`` directory in the container
- ``-w /build`` makes the bound volume the working directory in the container.
- ``sh -c 'make'`` is the command that's run from the container's working directory to compile your document.
  The example uses a :file:`Makefile`, but this command can be customized for your project.
- The compiled PDF is written into the current directory on your computer since it was bound to the container.

.. _docker-image-refresh:

Deleting or refreshing the Docker image
=======================================

Once downloaded, Docker caches the ``lsstsqre/lsst-texmf:latest`` image on your computer.
If ``lsst-texmf`` is updated, you can refresh your image by deleting the cached copy:

.. code-block:: bash

   docker rmi lsstsqre/lsst-texmf:latest

The next time you :command:`docker run` the new ``lsst-texmf:latest`` image will be downloaded.

.. _docker-details:

About the lsst-texmf Docker image
=================================

The `lsstsqre/lsst-texmf`_ Docker image is based on Ubuntu 14.04 (trusty).
It contains a full `TeX Live`_ distribution, as well as ``make`` and ``git`` via the `lsstsqre/lsst-texlive`_ image.
``lsst-texmf`` is installed in the container's ``/texmf`` directory, with :envvar:`TEXMFHOME` pre-set to that directory.

The ``latest`` tag tracks the ``master`` branch.
Other tags may be available for pinned versions and development branches.
See the list of `tags on Docker Hub`_.

Usually you'll want to use the ``latest`` tag.

.. _`install Docker`: https://www.docker.com/community-edition#/download
.. _`tags on Docker Hub`: https://hub.docker.com/r/lsstsqre/lsst-texmf/tags/
.. _`lsstsqre/lsst-texmf`: https://hub.docker.com/r/lsstsqre/lsst-texmf/
.. _`lsstsqre/lsst-texlive`: https://hub.docker.com/r/lsstsqre/lsst-texlive/
.. _`TeX Live`: http://tug.org/texlive/
.. _`lsst-texmf GitHub repository`: https://github.com/lsst/lsst-texmf
