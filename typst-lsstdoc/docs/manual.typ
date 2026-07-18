#import "@preview/tidy:0.4.3"

#let package = toml("../typst.toml").at("package")

#set document(title: "rubin-technote manual", author: "Rubin Observatory")
#set page(paper: "us-letter", numbering: "1", margin: 1in)
#set text(size: 11pt)
#set heading(numbering: "1.1")
#show link: set text(fill: rgb("#005ea8"))
#show raw.where(block: true): block.with(
  fill: rgb("#f4f4f4"),
  inset: 8pt,
  radius: 3pt,
  width: 100%,
)

#align(center)[
  #text(size: 24pt, weight: "bold")[rubin-technote]
  #v(4pt)
  #text(size: 12pt)[#package.description]
  #v(2pt)
  Version #package.version --- #package.license license
]
#v(16pt)

= Overview

The `rubin-technote` package renders Vera C. Rubin Observatory technical
documents: a branded title page with authors and affiliations, running
headers and footers, draft and obsolete state rendering, a change record,
and bibliography support for the shared Rubin BibTeX files.

Document metadata normally lives in a Documenteer-style `technote.toml`
file, so the same author and metadata tooling used by Markdown and
reStructuredText technotes applies unchanged.

= Quick start

```typ
#import "@preview/rubin-technote:0.1.0": lsstdoc, technote-args

#show: lsstdoc.with(
  ..technote-args(toml("technote.toml")),
  title: "My Technote",
  abstract: [A short description of this document.],
)

= Introduction

Add content here.
```

Shared bibliographies are passed as bytes so that paths resolve from the
document rather than from inside the package:

```typ
#let bibliographies = (
  read("local.bib", encoding: none),
  read("lsstbib/lsst.bib", encoding: none),
)
#show: lsstdoc.with(
  // ...
  bibliography: bibliographies,
)
```

= Document API

#let lsstdoc-module = tidy.parse-module(
  read("../src/lsstdoc.typ"),
  name: "rubin-technote",
)
#tidy.show-module(lsstdoc-module, style: tidy.styles.default)

= Documenteer metadata

#let technote-module = tidy.parse-module(
  read("../src/technote-toml.typ"),
  name: "technote-toml",
)
#tidy.show-module(technote-module, style: tidy.styles.default)

= Admonitions

#let admonitions-module = tidy.parse-module(
  read("../src/admonitions.typ"),
  name: "admonitions",
)
#tidy.show-module(admonitions-module, style: tidy.styles.default)

= Citations

#let citations-module = tidy.parse-module(
  read("../src/citations.typ"),
  name: "citations",
)
#tidy.show-module(citations-module, style: tidy.styles.default)
