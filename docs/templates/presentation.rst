.. _presentation-template:

#################################
LSST beamer presentation template
#################################

The ``presentation`` template lets you create new beamer_ presentations using the :ref:`LSST-beamer <lsst-texmf-beamer>` class.

.. seealso::

   For background, see :ref:`templates`.

   For help with using the ``LSST-beamer`` class, see :ref:`lsst-texmf-beamer`.

.. _presentation-template-invocation:

Invoking the template
=====================

After you have :ref:`set up <template-set-up>` cookiecutter and cloned the ``lsst-texmf`` repository, you can create a document by pointing :command:`cookiecutter` at ``lsst-texmf``\ ’s :file:`templates/presentation` directory.
For example, from a directory containing a ``lsst-texmf`` clone:

.. code-block:: bash

   cookiecutter lsst-texmf/templates/presentation

Cookiecutter will prompt you to configure your document.

.. _presentation-template-configs:

Template configurations
=======================

This section describes configurations requested by :command:`cookiecutter`.

``title``
   The presentation's title (used in the :file:`README` and the ``\title`` command).

``short_title``
   A shortened title that appears in the footer of slides.

``slug``
   A string that determines the presentation's directory and file name.
   Being a file name, the ``slug`` should contain no white space, ``/``, or other characters not valid in file names.

``presenter``
   Name of the presenter (formatted "First Last").

``presenter_role``
   Position of the presenter in the organization (such as "Manager" or "Software Developer").

``presenter_institution``
   Presenter's home institution (such as "AURA/LSST" or "University of Washington").

``date``
   Date of the presentation, following ISO 8601 formatting: ``YYYY-MM-DD``.

``venue``
   Institution or event where the presentation is being given.

``copyright_year``
   Year when copyright is first claimed.

``copyright_hold``
   Institution that holds the presentation's copyright.

``license_cc_by``
   If ``true``, a Creative Commons Attribution license is added to the :file:`README`.

.. _beamer: https://en.wikipedia.org/wiki/Beamer_(LaTeX)
