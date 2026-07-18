# Prototype assets

- `rubin-logo.svg` is the supplied “Colorized RGB — use over white” Vera C. Rubin Observatory logo.
  The square source canvas is cropped by the Typst layout rather than altering the artwork.
- `orcid-id.png` is the small ORCID icon already used by the neighboring `pstn-019` document.
  The template links the icon to the author's ORCID page and does not print the identifier.
- `rubinobs.png` is the pale observatory illustration used along the bottom of the title page, copied from the LaTeX class assets in `texmf/tex/latex/lsst/` so the template subtree is self-contained.
- `rubin-aas.csl` is the default bibliography style, following the aastex `aasjournal.bst` author-year conventions.
  It renders Rubin technote handles from the bibliography keys (the convention of the shared `lsst.bib`) because hyphenated report numbers do not survive the bibliography processor.
  It is adapted from the Astrophysical Journal style in the CSL project (CC-BY-SA 3.0), whose authors are credited in the file.
- `citation-key.csl` is a minimal CSL style used only for `citeds` and `citedsp`.
  It renders the standard CSL `citation-key` variable, or a supplied locator as alternate text, while retaining Typst's native bibliography-entry hyperlink.

These files are suitable for evaluating the prototype.
Branding, trademark, and redistribution terms must be confirmed before publishing a package.
