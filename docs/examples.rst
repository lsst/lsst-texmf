.. _examples:

########
Examples
########

These examples show what kinds of documents and presentations can be made with lsst-texmf.
You can tweak and compile these examples yourself by first cloning and installing lsst-texmf, then running :command:`make all` from the :file:`lsst-texmf` directory.

DM document (LDM)
=================

- :download:`LDM-nnn.pdf`
- Source: `LDM-nnn.tex`_

This document demonstrates how to use the ``lsstdoc`` class to make a Data Management document.

DM technical note (DMTN)
========================

- :download:`DMTN-nnn.pdf`
- Source: `DMTN-nnn.tex`_

This document demonstrates how to use the ``lsstdoc`` class to make a Data Management technote in the DMTN or SQR series.

LSST Beamer presentation
========================

- :download:`presentation.pdf`
- Source: `presentation.tex`_

This Beamer presentation uses the ``LSST-beamer`` package to make a standardized LSST presentation.

LSST 2016-style Beamer presentation
===================================

- :download:`beamer-LSST2016.pdf`
- Source: `beamer-LSST2016.tex`_

This Beamer presentation uses an alternate background theme to emulate the LSST 2016 Project and Community Workshop slide templates:

.. code-block:: latex

   \usepackage[
     sansFont=OpenSans, colorlinks,
     backgroundTheme=LSST2016-alt,
     colortheme=bat
   ]{LSST-beamer}

.. _beamer-desc:

DESC-style Beamer presentation
==============================

- :download:`beamer-desc.pdf`
- Source: `beamer-desc.tex`_

This presentation demonstrates the ``descTheme`` Beamer style to emulate standard `LSST DESC`_ presentations:

.. code-block:: latex

   \usepackage[descTheme, sansFont=OpenSans, colorlinks]{LSST-beamer}

.. _test-bibtex:

Bibliography demo
=================

- :download:`test-bibtex.pdf`
- Source: `test-bibtex.tex`_

This document uses the standard ``lsstdoc`` class, but renders all bibliography entries.
Use this demo to test how new bibitems are rendered in ``lsstdoc``.

.. _`LDM-nnn.tex`: https://github.com/lsst/lsst-texmf/blob/master/examples/LDM-nnn.tex
.. _`DMTN-nnn.tex`: https://github.com/lsst/lsst-texmf/blob/master/examples/DMTN-nnn.tex
.. _`presentation.tex`: https://github.com/lsst/lsst-texmf/blob/master/examples/presentation.tex
.. _`beamer-LSST2016.tex`: https://github.com/lsst/lsst-texmf/blob/master/examples/beamer-LSST2016.tex
.. _`beamer-desc.tex`: https://github.com/lsst/lsst-texmf/blob/master/examples/beamer-LSST2016.tex
.. _`test-bibtex.tex`: https://github.com/lsst/lsst-texmf/blob/master/tests/test-bibtex.tex

.. _LSST DESC: http://www.lsst-desc.org
