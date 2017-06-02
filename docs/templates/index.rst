.. _templates:

#####################################
Creating new documents with templates
#####################################

``lsst-texmf`` includes cookiecutter_ templates that help you start new projects more quickly.

.. _template-set-up:

Set up
======

To use the templates, you'll need to install cookiecutter_ and have a local clone of the ``lsst-texmf`` repository.

Cookiecutter
------------

You can install cookiecutter_ with :command:`pip`:

.. code-block:: bash

   pip install cookiecutter

Or with Anaconda_:

.. code-block:: bash

   conda install cookiecutter

lsst-texmf
----------

You need a local copy of ``lsst-texmf`` to use the templates.
If you have :ref:`installed <install>` ``lsst-texmf``, you'll have a ``lsst-texmf`` clone at ``$TEXMFHOME/..``.
Otherwise, you can clone the repository now:

.. code-block:: bash

   git clone https://github.com/lsst/lsst-texmf

Quick start
===========

Templates are located in the :file:`lsst-texmf/templates` directory.
You can create a new document by passing the template's directory path to :command:`cookiecutter`.
For example:

.. code-block:: bash

   cookiecutter lsst-texmf/templates/document

Then answer the prompts to initialize the document.
See the :ref:`template-list` section for information about specific templates.

.. _template-list:

Templates
=========

These templates are included with ``lsst-texmf``:

.. toctree::

   document
   presentation

.. _cookiecutter: https://cookiecutter.readthedocs.io/en/latest/index.html
.. _Anaconda: https://www.continuum.io/downloads
