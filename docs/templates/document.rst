.. _document-template:

############################################
LSST document (including LDM, DMTN) template
############################################

The easiest way to create a new document with the :doc:`lsstdoc <../lsstdoc>` class is through our Cookiecutter_ templates in the `lsst/templates <https://github.com/lsst/templates>`__ GitHub repository:

- `latex_lsstdoc <https://github.com/lsst/templates/tree/main/project_templates/latex_lsstdoc>`__ for general-purpose lsstdoc-class documents
- `technote_latex <https://github.com/lsst/templates/tree/main/project_templates/technote_latex>`__ for technical notes
- `test_report <https://github.com/lsst/templates/tree/main/project_templates/test_report>`__ for test reports that integrate with docsteady.

The recommended way to use these templates is through our Slack bot, which automatically creates and configures the GitHub repository for you.
These pages describe how to create documents through Slack:

- `Creating a new LaTeX (lsstdoc) change-controlled document <https://developer.lsst.io/project-docs/change-controlled-docs.html#creating-a-new-latex-lsstdoc-change-controlled-document>`__
- `Create a technote <https://developer.lsst.io/project-docs/technotes.html#create-a-technote>`__

.. _cookiecutter: https://cookiecutter.readthedocs.io/en/latest/index.html
