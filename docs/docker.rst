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

The `lsstsqre/lsst-texmf`_ Docker image is based on the ``python:3.7-slim-buster`` (Debian) official Docker image.
Using a Python base image ensures the correct version of Python is available for ``lsst-texmf``\ ’s Python scripts.

System packages
---------------

The Docker image contains a `TeX Live`_ distribution, as well as several utilities.
See the `docker/install-base-packages.sh`_ script in the ``lsst-texmf`` repository for the current list of installed packages.

Scripts and Python dependencies
-------------------------------

Inside the Docker container, ``lsst-texmf``\ ’s :file:`bin` directory is included in the :envvar:`PATH` environment variable.
You can call scripts such as ``generateAcronyms.py`` and ``db2authors.py`` from your document's :file:`Makefile` directly.

The Docker image also includes Python packages needed for ``lsst-texmf``\ ’s scripts, as well as scripts that might be run as part of your document's :file:`Makefile`.
See the `requirements.txt`_ file in the ``lsst-texmf`` repository for the current list of installed Python packages.

.. _`install Docker`: https://www.docker.com/community-edition#/download
.. _`tags on Docker Hub`: https://hub.docker.com/r/lsstsqre/lsst-texmf/tags/
.. _`lsstsqre/lsst-texmf`: https://hub.docker.com/r/lsstsqre/lsst-texmf/
.. _`TeX Live`: http://tug.org/texlive/
.. _`lsst-texmf GitHub repository`: https://github.com/lsst/lsst-texmf
.. _`docker/install-base-packages.sh`: https://github.com/lsst/lsst-texmf/blob/master/docker/install-base-packages.sh
.. _`requirements.txt`: https://github.com/lsst/lsst-texmf/blob/master/requirements.txt
