.. _lsst-texmf-beamer:

#####################
Writing Presentations
#####################

You can use `beamer <https://en.wikipedia.org/wiki/Beamer_(LaTeX)>`_ to make LSST-flavoured talks by adding something like:

.. code-block:: latex

   \usepackage[fonts=false]{LSST-beamer}

to your beamer presentation.
You need the ``fonts=false`` if you want to use :command:`pdflatex`; if you're happy with :command:`xelatex` it may be omitted.

The backgrounds for the title and main pages are found in the directory :file:`LSST-themes/`.
Two files are required:

* :file:`LSSTcover.pdf` : background for cover slide
* :file:`LSSTmain.pdf`  : background for all non-cover slides

(``jpg`` files are also allowed, e.g. :file:`LSSTcover.jpg`)

Default may be a symbolic link to choose the proper background, or you may specify a different directory with the ``backgroundTheme`` option to the ``LSST-beamer`` package, e.g.

.. code-block:: latex

   \usepackage[backgroundTheme=LSST2016]{LSST-beamer}

You may use ``footline=XXX`` to put text in the footer, generally with the default "generic" ``backgroundTheme``, as many ``backgroundThemes`` already have something there.
The text may use ``{}`` to quote spaces; see :file:`examples/Example-beamer-LSST2016.tex` for an example.

You may use ``\position`` as an alias for ``\institute`` (e.g. ``\position{DM Boss}``) (but only if you declare it after importing the ``LSST-beamer`` package).

Another common problem is DESC; they use a different layout for their cover slides --- see
:file:`examples/Example-beamer-desc.tex`.

The full set of options that the LSST-beamer package accepts are:

``quiet``
   Suppress some pdf warnings.

``descTheme``
   Fiddle beamer to use DESC templates.

``colorlinks``
   Hyperref's colorlinks, but set colours for beamer (default: ``false``).

``theme``
   Beamer theme to use (default: ``Boadilla``).

``colortheme``
   Beamer colour theme (default: ``seahorse``); takes precedence over ``foreground``.

``foreground``
   Foreground color (RGB triplet e.g. ``{0.1, 0, 0.2}``).

``titleColor``
   Name of colour for title (e.g. ``white``).

``titleVoffset``
   Vertical offset of start of title in units of ``\textheight`` (default: ``0.2``).

``backgroundTheme``
   Location of ``LSST{cover,main}.pdf`` (a directory relative to LSST-themes; default: ``default``).
   No backgrounds are inserted if ``backgroundTheme`` is empty.

``footline``
   Text to put in the footer (generally with ``backgroundTheme=generic``).

``centerFrameTitle``
   Centre frame titles (default: ``true``).

``noOutline``
   Don't include an outline before each section (``BEAMER_FRAME_LEVEL: 2``).

``serif``
   Use serif font theme.

``fonts``
   Allow user to set fonts using using xelatex's font management.

``mainFont``
   The main font (default: ``Tex Gyre Pagella``;  only takes effect if ``fonts=true``).

``mainFontScale``
   Scaling for main font (default: ``1``; only takes effect if ``fonts=true``).

``sansFont``
   The sans font (default: ``Open Sans``; only takes effect if ``fonts=true``).

``sansFontScale``
   Scaling for sans font (default: ``1``; only takes effect if ``fonts=true``).

``monoFont``
   The mono font (default: ``Inconsolata``;    only takes effect if ``fonts=true``).

``monoFontScale``
   Scaling for mono font (default: ``1``; only takes effect if ``fonts=true``).
