# LSST Presentations using Latex

To get started put the directory containing `LSST-beamer.sty` and `LSST-themes` on your search path (e.g. add
it to ``$TEXINPUTS`). These are in the `texmf` folder so if you have run `mktelsr` (or it is up to date in the repository) they will already be found.


You can use beamer to make LSST-flavoured talks by adding something like:
```latex
\usepackage[fonts=false]{LSST-beamer}
```
to your beamer presentation (see `examples/Example_presentation.tex` for a complete, umhh, example).  You need the
`fonts=false` if you want to use `pdflatex`; if you're happy with `xelatex` it may be omitted.

The backgrounds for the title and main pages are found in the directory LSST-themes/default. Two files are
required:

*	`LSSTcover.pdf` : background for cover slide
* `LSSTmain.pdf`  : background for all non-cover slides

(`jpg` files are also allowed, e.g. `LSSTcover.jpg`)

default may be a symbolic link to choose the proper background, or you may specify a different directory with
the backgroundTheme option to the LSST-beamer package, e.g.
```latex
\usepackage[backgroundTheme=LSST2016]{LSST-beamer}
```
You may use `footline=XXX` to put text in the footer, generally with the default "generic" backgroundTheme, as
many backgroundThemes already have something there.  The text may use `{}` to quote spaces; see
`examples/Example-beamer-LSST2016.tex` for an example.

You may use `\position` as an alias for `\institute` (e.g. `\position{DM Boss}`) (but only if you
declare it after importing the LSST-beamer package).

Another common problem is DESC; they use a different layout for their cover slides --- see
`examples/Example-beamer-desc.tex`.


The full set of options that the LSST-beamer package accepts are:

| | |
| --- | --- |
| `quiet`    	       | Suppress some pdf warnings |
| `descTheme`	       | Fiddle beamer to use DESC templates |
| `colorlinks`	     | Hyperref's colorlinks, but set colours for beamer (default: `false`) |
| `theme`	           | Beamer theme to use (default: `Boadilla`) |
| `colortheme`	     | Beamer colour theme (default: `seahorse`); takes precedence over `foreground` |
| `foreground`	     | Foreground color (RGB triplet e.g. `{0.1, 0, 0.2}`) |
| `titleColor`	     | Name of colour for title (e.g. `white`) |
| `titleVoffset`     | Vertical offset of start of title in units of `\textheight` (default: 0.2) |
| `backgroundTheme`  | Location of `LSST{cover,main}.pdf` (a directory relative to LSST-themes; default: default). No backgrounds are inserted if `backgroundTheme` is empty |
| `footline`	       | Text to put in the footer (generally with `backgroundTheme=generic`) |
| `centerFrameTitle` | Centre frame titles (default: `true`) |
| `noOutline`	       | Don't include an outline before each section (`BEAMER_FRAME_LEVEL: 2`) |
| `serif`	           | Use serif font theme |
| `fonts`	           | Allow user to set fonts using using xelatex's font management |
| `mainFont`	       | The main font (default: `Tex Gyre Pagella`;  only takes effect if `fonts=true`) |
| `mainFontScale`    | Scaling for main font (default: `1`; only takes effect if `fonts=true`) |
| `sansFont`	       | The sans font (default: `Open Sans`; only takes effect if `fonts=true`) |
| `sansFontScale`    | Scaling for sans font (default: `1`; only takes effect if `fonts=true`) |
| `monoFont`	       | The mono font (default: `Inconsolata`;    only takes effect if `fonts=true`) |
| `monoFontScale`    | Scaling for mono font (default: `1`; only takes effect if `fonts=true`) |
