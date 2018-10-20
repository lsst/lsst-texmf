.. _document-template:

############################################
LSST document (including LDM, DMTN) template
############################################

The ``document`` template lets you create new documents using the :ref:`lsstdoc <lsstdoc>` class.
These can be project controlled documents (LPM, LSE, LDM, for example) or technical notes (DMTN, SQR, SMTN).
This page describes how to use the ``document`` template.

.. seealso::

   For background, see :ref:`templates`.

   For help with using the ``lsstdoc`` class, see :ref:`lsstdoc`.

.. note::

   We intend to provide a chatbot for creating new documents that handles creating a GitHub repository, filling in the template, and deploying the document as a website.
   In the meantime, you can still manually create new documents with this template.

.. _document-template-invocation:

Invoking the template
=====================

After you have :ref:`set up <template-set-up>` cookiecutter and cloned the ``lsst-texmf`` repository, you can create a document by pointing :command:`cookiecutter` at ``lsst-texmf``\ ’s :file:`templates/document` directory.
For example, from a directory containing a ``lsst-texmf`` clone:

.. code-block:: bash

   cookiecutter lsst-texmf/templates/document

Cookiecutter will prompt you to configure your document.
See the next section for details.

.. _document-template-configs:

Template configurations
=======================

This section describes configurations requested by :command:`cookiecutter`.

``series``
   Handle of the documentation series.
   Technical notes can be ``DMTN``, ``SQR``, ``PSTN'' or ``SMTN`` (see the `DM Developer Guide <https://developer.lsst.io/docs/technotes.html>`__ for more information).

``serial_number``
   Serial number of the document.
   For project documents, this number is pre-assigned by DocuShare.
   For technical notes, you can claim the next available number yourself.
   These links show existing technical notes in each series:

   - `DMTN <https://github.com/lsst-dm?utf8=✓&q=DMTN-&type=&language=>`__
   - `SQR <https://github.com/lsst-sqre?utf8=✓&q=SQR-&type=&language=>`__
   - `SMTN <https://github.com/lsst-sims?utf8=✓&q=SMTN-&type=&language=>`__
   - `PSTN <https://github.com/lsst-pst?utf8=✓&q=PSTN-&type=&language=>`__

``github_org``
    Documents belong in specific GitHub organizations:

    - LDM: `lsst <https://github.com/lsst>`__
    - DMTN: `lsst-dm <https://github.com/lsst-dm>`__
    - SQR: `lsst-sqr <https://github.com/lsst-sqre>`__
    - SMTN: `lsst-sims <https://github.com/lsst-sims>`__
    - PSTN: `lsst-pst <https://github.com/lsst-sims>`__

``docushare_url``
   Provide a URL to the document in DocuShare, if available.
   Technotes might not have DocuShare handles.
   Using the https://ls.st short link to the document's version page in DocuShare is effective.
   For example: ``'https://ls.st/ldm-151*'``.

``title``
   Title of the document, without a handle prefix.

``first_author``
   The first and last name of the document's primary author.
   You can add additional authors later to the ``\author`` command in the generated document.

``abstract``
   Abstract or summary of the document.
   This abstract appears both in the document's ``\setDocAbstract`` command an in the :file:`README`.

``copyright_year``
   Year when copyright is first claimed.

``copyright_hold``
   Institution that holds the document's copyright.

``license_cc_by``
   If ``true``, a Creative Commons Attribution license is added to the :file:`README`.

.. _document-template-deploy:

Deploying the document
======================

.. note::

   These instructions will help you deploy your documentation project to GitHub and LSST the Docs.
   In the future, a chatbot service will automate these steps.

After creating a document directory with `cookiecutter`_\ , the next step is to initialize it as a Git repository and push that repository to GitHub.
Keep in mind the organization you host the repository in must match the organization name provided to `cookiecutter`_.
Also, the repository name should be the document's handle in lowercase (for example, `lsst-sqre/sqr-019 <https://github.com/lsst-sqre/sqr-019>`__ for the `SQR-019 <https://sqr-019.lsst.io>`__ technical note).

Once the document is on GitHub, notify the `#dm-docs`_ channel on Slack that a new document is ready to be deployed to LSST the Docs.

.. _cookiecutter: https://cookiecutter.readthedocs.io/en/latest/index.html
.. _`#dm-docs`: https://lsstc.slack.com/messages/C2B6DQBAL
