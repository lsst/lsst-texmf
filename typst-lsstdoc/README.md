# rubin-technote

**Vera C. Rubin Observatory technical documents in Typst.**

This package renders Rubin technical notes and reports: a branded title page with authors, affiliations, ORCID links, and document state; running headers and footers; draft and obsolete watermarks; a change record; controlled-document notices; and bibliography support for the shared Rubin BibTeX files.
It is the Typst counterpart of the LaTeX `lsstdoc` class, developed as the `typst-lsstdoc/` subtree of [lsst-texmf](https://github.com/lsst/lsst-texmf) until it moves to a standalone repository and Typst Universe.

## Quick start

New technote repositories are normally scaffolded from the `technote_typst` template in the [templates repository](https://github.com/lsst/templates), which provides a Makefile that vendors this package and builds the PDF:

```sh
make pdf
```

To use the package directly, place it under a package path as `preview/rubin-technote/0.1.0` and compile with:

```sh
typst compile --root . \
  --package-path <packages dir> \
  --font-path <packages dir>/preview/rubin-technote/0.1.0/fonts \
  main.typ
```

Once the package is published to Typst Universe, `typst init @preview/rubin-technote` will scaffold the files in `template/` directly.

## Usage

Document metadata normally lives in a Documenteer-style [technote.toml](https://documenteer.lsst.io/technotes/) file, shared with the Markdown and reStructuredText technote tooling, so `documenteer technote add-author` and `sync-authors` manage the author list:

```typst
#import "@preview/rubin-technote:0.1.0": lsstdoc, technote-args

#show: lsstdoc.with(
  ..technote-args(toml("technote.toml")),
  title: "My Technote",
  abstract: [A short description of this document.],
)

= Introduction

Add content here.
```

The mapping covers the handle (`id`), series, status, revision date, DOI, repository URL, the optional title override, and the author list; the change record and abstract stay in the document, and the compiled document exposes its front matter to tooling via `typst eval 'query(<rubin-technote>).first().value' --in <file>`.
The `lsstdoc` show rule also accepts every field directly (`id`, `series`, `status`, `date`, `authors`, `affiliations`, `subtitle`, `doi`, `repository-url`, `changes`, `toc`, `bibliography`, `bibliography-style`, `bibliography-full`) for documents that do not use `technote.toml`.

Shared bibliographies are passed as bytes so paths resolve from the document:

```typst
#let bibliographies = (
  read("local.bib", encoding: none),
  read("lsstbib/lsst.bib", encoding: none),
)
```

The package also exports `note` and `warning` admonitions and the `citeds`/`citedsp` helpers, which cite Rubin documents by their handles.

## Documentation

- [User guide](docs/manual.typ), typeset with the package itself so its pages demonstrate the features it describes, with an API reference generated from the source doc comments by [tidy](https://typst.app/universe/package/tidy); build it with `typst compile --root . --font-path fonts docs/manual.typ manual.pdf` from this directory.
- [Design and audit record](docs/design.md), covering the LaTeX `lsstdoc` feature inventory, the compatibility decisions, and the technote workflow design.
- [Examples](examples/), including the acceptance fixture exercising every feature (`features.typ`) and the `technote.toml`-driven example (`technote.typ`).

## Data and assets

- `data/series.yaml` holds the Rubin document series labels and controlled-document membership, kept in exact agreement with lsst-texmf's `bibtools.py` by a parity test.
- `fonts/` ships the Open Sans, Inconsolata, and XITS families with their licenses so builds are reproducible; pass it to `--font-path`.
- `assets/` contains the Rubin logo, the title-page observatory artwork, the ORCID icon, and the citation-key CSL style; branding redistribution terms must be confirmed before wide publication.

## License

The package code is MIT licensed; see [LICENSE](LICENSE).
The bundled fonts keep their own licenses in `fonts/`.
