#import "../src/lsstdoc.typ": citeds, citedsp, lsstdoc, note, warning

#let metadata = yaml("metadata.yaml")
#let people = yaml("authors.yaml")
#let bibliography-sources = (
  // Loading bytes here resolves paths from this document rather than from the
  // imported template module. No shared entries are copied into the example.
  read("references.bib", encoding: none),
  read("../../texmf/bibtex/bib/refs.bib", encoding: none),
  read("../../texmf/bibtex/bib/lsst.bib", encoding: none),
  read("../../texmf/bibtex/bib/lsst-dm.bib", encoding: none),
  read("../../texmf/bibtex/bib/books.bib", encoding: none),
  read("../../texmf/bibtex/bib/refs_ads.bib", encoding: none),
)

#show: lsstdoc.with(
  title: metadata.title,
  short-title: metadata.short_title,
  subtitle: metadata.subtitle,
  doc-ref: metadata.doc_ref,
  series: metadata.series,
  status: metadata.status,
  date: metadata.date,
  doi: metadata.doi,
  repository-url: metadata.repository_url,
  authors: people.authors,
  affiliations: people.affiliations,
  abstract: metadata.abstract,
  changes: metadata.changes,
  toc: metadata.toc,
  bibliography: bibliography-sources,
)

= Introduction <sec-introduction>

Rubin Observatory technical documents need a recognizable hierarchy and
consistent metadata without requiring authors to write presentation markup.
This prototype loads the title, state, change record, people, and affiliations
directly from YAML. It also cites ordinary BibTeX entries using Typst's native
bibliography support @jenness-example.

The implementation is intentionally not a line-by-line translation of
`lsstdoc.cls`. It follows the same design language while using native Typst
layout, counters, links, and references. The data flow is summarized in
@fig-data-flow.

#figure(
  image(
    "figure.svg",
    width: 90%,
    alt: "YAML metadata and author data flow through the Typst template to a tagged PDF.",
  ),
  caption: [Structured inputs are rendered by the Typst template.],
) <fig-data-flow>

== Document state and metadata <sec-state>

The example is compiled in *draft* state. The same template accepts `released`
and `obsolete`; unsupported values produce a direct error. The document series
is validated against the complete Rubin series mapping, and the series supplies
the human-readable type label.

Metadata remains structured until presentation time:

```yaml
series: DMTN
status: draft
doc_ref: DMTN-999
```

#note(title: "Structured metadata")[
  YAML remains the authoritative input to the template; authors do not need to
  copy metadata into presentation markup.
]

#warning(title: "Prototype scope")[
  This proof of concept does not yet reproduce every historical `lsstdoc.cls`
  workflow. Requirements and action extraction remain deferred.
]

== Equations and cross-references

The standard luminosity relation is

#math.equation(
  block: true,
  alt: "Luminosity equals four pi times radius squared times the Stefan-Boltzmann constant times temperature to the fourth power.",
  $ L = 4 pi R^2 sigma T^4 $,
) <eq-luminosity>

@eq-luminosity, @sec-state, and @fig-data-flow use native labels and
references. Footnotes also remain native to Typst.#footnote[
  This footnote is included to exercise page layout and text sizing.
]

#pagebreak()
= Tables and structured records <sec-tables>

The change record in the front matter is generated from YAML. Longer technical
tables use the same native table model. The representative @tab-series
deliberately contains enough rows to exercise page breaking.

#figure(
  [],
  kind: table,
  alt: "A representative technical table with 25 component records.",
  caption: [Representative multi-page technical table.],
) <tab-series>

#let component-table(start, end) = table(
  columns: (14%, 31%, 1fr),
  inset: 5pt,
  stroke: 0.4pt + rgb("#777777"),
  table.header(
    [*Index*],
    [*Component*],
    [*Purpose*],
  ),
  ..range(start, end).map(number => (
    str(number),
    "Prototype component " + str(number),
    "Representative technical content used to verify wrapping, repeated headers, and page breaks.",
  )).flatten(),
)

#component-table(1, 16)
#pagebreak()
#component-table(16, 26)

= Code and lists

Inline code such as `typst compile` uses a monospace font. Blocks use native
raw content:

```python
metadata = load_yaml("metadata.yaml")
document = render_template(metadata)
```

The first prototype demonstrates:

- YAML metadata and author input;
- Rubin title and page furniture;
- citations, equations, figures, and tables;
- draft, released, and obsolete states.

= Bibliography compatibility

The local fixture includes articles, books, proceedings, reports, software,
and web entries. The same bibliography loads all five repository bibliography
pools directly. Examples include FITS @fits-standard, Python @python-paper,
software @typst-software, and the shared Tidy Data entry @JSSv059i10. A Rubin
technical report can display its bibliography key without depending on a
custom `handle` field: #citeds("DMTN-001"). The bracketed form is
#citedsp("DMTN-000", display: [technical-note series]). Typst itself is
available at #link("https://typst.app/")[https://typst.app/].

= Conclusion

The prototype favors explicit data, native Typst document structures, and
readable diagnostics. The output should look and feel like a Rubin document
without matching LaTeX pagination or glyph choices exactly.

#heading(level: 1, numbering: none)[Appendix A: Prototype scope] <app-scope>

Requirements extraction and meeting action items are deferred. They can be
revisited if real document migrations show that they remain valuable.
