#import "../src/lsstdoc.typ": citeds, citedsp, lsstdoc, note, technote-args, warning
#import "@preview/tidy:0.4.3"

#let package = toml("../typst.toml").at("package")

// The guide is typeset with the package it documents, so its own pages
// demonstrate the features it describes. TESTN is the series reserved for
// template test documents.
#show: lsstdoc.with(
  title: "The rubin-technote Package",
  short-title: "rubin-technote User Guide",
  subtitle: "User guide for version " + package.version,
  id: "TESTN-001",
  series: "TESTN",
  status: "released",
  date: "2026-07-18",
  repository-url: package.repository,
  authors: (
    (
      internal_id: "rubinobs",
      display_name: "Vera C. Rubin Observatory",
      affiliations: (),
    ),
  ),
  affiliations: (:),
  abstract: "This guide documents the rubin-technote package for writing Vera C. Rubin Observatory technical documents in Typst. It is typeset with the package it documents: the title page, front matter, page furniture, tables, admonitions, and citations in these pages are live demonstrations of the features described alongside them.",
  changes: (
    (
      version: "0.1.0",
      date: "2026-07-18",
      description: "Initial user guide for the prototype package.",
      author: "Rubin Observatory",
    ),
  ),
  toc: true,
  // Two sources demonstrate that any number of bibliography files can be
  // combined; manual.bib provides handle-keyed entries for citeds.
  bibliography: (
    read("../examples/references.bib", encoding: none),
    read("manual.bib", encoding: none),
  ),
)

#show raw.where(block: true): block.with(
  fill: rgb("#f4f4f6"),
  inset: 8pt,
  radius: 3pt,
  width: 100%,
)

= Introduction <sec-intro>

The `rubin-technote` package renders Rubin Observatory technical documents:
a branded title page with authors and document state, running headers and
footers, front matter with an abstract and change record, and bibliography
support for the shared Rubin BibTeX files.
Document metadata normally comes from the same Documenteer `technote.toml`
file used by Markdown and reStructuredText technotes, so author and metadata
tooling applies unchanged.

This guide is itself a Rubin document produced by the package: its title
page, contents, change record, and the tables and callouts below are the
features it describes.
The `TESTN` series shown on the title page is the series reserved for
template test documents.
Build the guide from the package root with:

```sh
typst compile --root . --font-path fonts docs/manual.typ manual.pdf
```

= Quick start <sec-quickstart>

New technote repositories are scaffolded from the `technote_typst` template
in the templates repository, which provides a Makefile:
`make pdf` vendors this package, downloads the shared bibliographies, and
compiles the document, while `make add-author` and `make sync-authors`
manage the author list in `technote.toml` from the central author database.

A document selects the template with a show rule, spreading the mapped
`technote.toml` metadata and keeping the title and abstract in the source,
as @lst-quickstart shows.

#figure(
  ```typ
  #import "@preview/rubin-technote:0.1.0": lsstdoc, technote-args

  #show: lsstdoc.with(
    ..technote-args(toml("technote.toml")),
    title: "My Technote",
    abstract: [A short description of this document.],
  )

  = Introduction

  Add content here.
  ```,
  caption: [A minimal `index.typ` driving the template from `technote.toml`.],
) <lst-quickstart>

Documents outside the technote workflow pass every field directly instead;
@tab-arguments lists the full argument set.

= Document metadata <sec-metadata>

#figure(
  table(
    columns: (auto, auto, 1fr),
    inset: 5pt,
    stroke: 0.4pt + rgb("#777777"),
    table.header([*Argument*], [*Default*], [*Purpose*]),
    [`title`], [required], [Document title, also used as PDF metadata.],
    [`id`], [required], [Document handle, for example `DMTN-999`; the name matches the `technote.toml` field.],
    [`series`], [required], [Series key, validated against the shared Rubin series data in `data/series.yaml`.],
    [`date`], [required], [Latest revision date for the title page and running header.],
    [`authors`], [required], [Ordered author dictionaries; see @sec-authors.],
    [`affiliations`], [required], [Affiliation records keyed by identifier; see @sec-authors.],
    [`status`], [`"released"`], [`"draft"`, `"released"`, or `"obsolete"`; see @sec-state.],
    [`short-title`], [`none`], [Running-header title; defaults to the title.],
    [`subtitle`], [`none`], [Subtitle below the title, as on this guide's title page.],
    [`doi`], [`none`], [Bare DOI rendered as a link on the title page; URL-prefixed values are rejected.],
    [`repository-url`], [`none`], [Document source link printed after the body.],
    [`abstract`], [`none`], [Front-matter abstract; a plain string also becomes the PDF description.],
    [`changes`], [`()`], [Change-record entries with `version`, `date`, `description`, and `author`.],
    [`toc`], [`true`], [Whether to render a table of contents.],
    [`bibliography`], [`none`], [Bibliography sources as bytes; see @sec-citations.],
    [`bibliography-style`], [`auto`], [The Rubin AAS style, or a bundled style name or CSL file path.],
    [`bibliography-full`], [`false`], [List all bibliography entries, not only the cited ones.],
  ),
  caption: [The `lsstdoc` arguments. This multi-page table is itself a demonstration: table figures break across pages and repeat their headers.],
) <tab-arguments>

Validation is immediate and specific: a missing required argument, an
unknown series, an unsupported status, or a URL-prefixed DOI each stop the
compile with a message naming the problem.

== Document state <sec-state>

`status: "draft"` adds a pale diagonal watermark to every page, red state
marks in the footer, and a red state label on the title page.
`status: "obsolete"` does the same with obsolete wording and replaces
controlled-document approval text with a historical-information notice.
This guide is `released`, so its pages carry no state furniture.
Controlled document series such as `LDM` and `LSE`, recorded in
`data/series.yaml`, additionally get a configuration-control notice in the
footer.

== Documenteer technote.toml <sec-toml>

`technote.toml` is the metadata file shared with Markdown and
reStructuredText technotes; the full schema is documented in the
#link("https://technote.lsst.io/user-guide/technote-toml.html")[technote.toml
user guide].
@lst-technote-toml shows a representative file (this package's technote
example fixture), and @lst-quickstart in @sec-quickstart shows how the
mapped values are passed to the template.

#figure(
  raw(read("../examples/technote.toml"), lang: "toml", block: true),
  caption: [A representative `technote.toml` metadata file.],
) <lst-technote-toml>

`technote-args` maps the parsed file onto the arguments of
@tab-arguments: `id`, `series_id`, `status.state` (`draft`, `stable`, and
`deprecated` become `draft`, `released`, and `obsolete`), `date_updated`
falling back to `date_created`, `doi`, `github_url`, the optional `title`
override, and the author list with deduplicated affiliations.
URL-prefixed DOI, ORCID, and ROR identifiers are normalized to the bare
form, and an unknown status state stops the compile with the accepted
values.
`date` and `status` can be passed to `technote-args` explicitly to override
the mapping.

== Machine-readable front matter <sec-query>

The compiled document embeds its front matter as a labeled metadata
element, the Typst counterpart of the annotated abstract structures in
Markdown and reStructuredText technotes.
Tooling can read the handle, series, status, date, title, and abstract
without parsing the source:

```sh
typst eval 'query(<rubin-technote>).first().value' --in index.typ
```

= Authors and affiliations <sec-authors>

Authors are ordered dictionaries; affiliations are records keyed by the
identifiers the authors reference:

```typ
authors: (
  (
    internal_id: "lovelacea",
    given_name: "Ada",
    family_name: "Lovelace",
    display_name: "Ada Lovelace",
    orcid: "0000-0001-5982-167X",
    affiliations: ("RubinObs",),
    corresponding: true,
  ),
),
affiliations: (
  RubinObs: (
    name: "NSF-DOE Vera C. Rubin Observatory",
    address: "Tucson, Arizona, USA",
    ror: "048g3cy84",
  ),
),
```

The title page assigns numeric affiliation markers in first-use order,
renders ORCID identifiers as linked icons following AASTeX practice, and
marks a corresponding author with an asterisk.
Wrapping is only allowed between authors, and a two-author list joins with
a plain "and".
An institutional author is a dictionary with an empty affiliation list, as
on this guide's title page.
In the technote workflow the author list lives in `technote.toml` and is
managed by `documenteer technote add-author` and `sync-authors` against the
central author database.

= Body content <sec-body>

Headings, cross-references, equations, figures, tables, footnotes, and raw
blocks are all native Typst; the template only restyles them.
Section references such as @sec-intro and table references such as
@tab-arguments use ordinary labels.
Equations are numbered:

$ L = 4 pi R^2 sigma T^4 $

External links are rendered dark blue and underlined, while internal
references keep the ordinary text styling.
Table figures may span pages with repeated headers, as @tab-arguments
demonstrates.

== Admonitions <sec-admonitions>

#note(title: "Structured metadata")[
  Notes use the Rubin teal callout and accept an optional custom title.
]

#warning[
  Warnings use an orange callout, and a custom title is always prefixed
  with "Warning".
]

Both admonitions are kept together across page breaks.

= Citations and bibliographies <sec-citations>

Bibliography sources are passed as bytes so that paths resolve from the
document rather than from inside the package:

```typ
#let bibliographies = (
  read("local.bib", encoding: none),
  read("lsstbib/lsst.bib", encoding: none),
)
```

In the technote workflow `make sync-bibs` downloads the five shared Rubin
bibliography files into `lsstbib/` using the same per-file mechanism as the
Sphinx technotes.
Ordinary citations use Typst's `@` syntax against any loaded source, for
example the FITS standard paper @fits-standard.
Rubin documents are conventionally cited by their handles, which are the
bibliography keys in the shared `lsst.bib`: `citeds` shows the key, as in
#citeds("DMTN-000"), and `citedsp` adds brackets, as in #citedsp("SQR-000").
Alternate display text is supported: #citeds("DMTN-000", display: [the
technical note series description]).
References follow the AAS journal (aastex) conventions by default,
implemented by the bundled `rubin-aas.csl` style: author-year citations,
comma-separated reference entries, and technote entries rendered as type,
handle, and institution, with the handle taken from the bibliography key.
The bibliography below lists only the cited entries unless
`bibliography-full: true` is set, and `bibliography-style` selects another
bundled style or a CSL file.

= Building documents <sec-building>

Technote repositories run `make pdf`.
Under the hood that is a single Typst compile against the vendored package:

```sh
typst compile --root . \
  --package-path .typst-packages \
  --font-path .typst-packages/preview/rubin-technote/0.1.0/fonts \
  index.typ TESTN-000.pdf
```

The package ships the Open Sans, Inconsolata, and XITS families in
`fonts/`, so builds are reproducible wherever the package is vendored.
Documents also compile under `--pdf-standard ua-1` for tagged, accessible
output when alt text is supplied for figures and equations.

// The generated reference nests function and parameter headings deeply;
// cap the displayed numbering at three levels.
#set heading(numbering: (..nums) => if nums.pos().len() <= 3 {
  numbering("1.1", ..nums)
})

#heading(level: 1, numbering: none)[API reference] <sec-api>

The reference below is generated from the doc comments in the package
source by the tidy package.

#let show-api(path, name) = tidy.show-module(
  tidy.parse-module(read(path), name: name),
  style: tidy.styles.default,
)

#show-api("../src/lsstdoc.typ", "rubin-technote")
#show-api("../src/technote-toml.typ", "technote-toml")
#show-api("../src/admonitions.typ", "admonitions")
#show-api("../src/citations.typ", "citations")
