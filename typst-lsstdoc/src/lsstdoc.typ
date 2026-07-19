#import "utilities.typ": nonempty, rubin-teal, url-styled, validate-doi, validate-series
#import "admonitions.typ" as admonitions
#import "document-state.typ": state-background, validate-status
#import "headers-footers.typ": running-footer, running-header
#import "title-page.typ": render-title-artwork, render-title-page
#import "front-matter.typ": render-abstract, render-contents
#import "change-record.typ": render-change-record
#import "citations.typ" as citations
#import "technote-toml.typ" as technote-toml

#let render-bibliography = bibliography
#let note = admonitions.note
#let warning = admonitions.warning
#let citeds = citations.citeds
#let citedsp = citations.citedsp
#let technote-args = technote-toml.technote-args

/// Render a Rubin Observatory technical document.
///
/// Use as a show rule, with metadata mapped from `technote.toml` or passed
/// directly:
/// ```typ
/// #import "@preview/rubin-technote:0.1.0": lsstdoc, technote-args
///
/// #show: lsstdoc.with(
///   ..technote-args(toml("technote.toml")),
///   title: "My Technote",
///   abstract: [A short description of this document.],
/// )
///
/// = Introduction
///
/// Add content here.
/// ```
/// -> content
#let lsstdoc(
  /// The document title, also used as PDF metadata.
  /// -> str | content
  title: none,
  /// The document handle, for example "DMTN-999"; the argument name
  /// matches the technote.toml field. Omit it for standalone documents
  /// such as manuals, which have no handle.
  /// -> str | none
  id: none,
  /// The series key, validated against the shared Rubin series data that
  /// also determines the displayed type label. Omit it together with the
  /// handle for standalone documents.
  /// -> str | none
  series: none,
  /// One of "draft", "released", or "obsolete"; draft and obsolete
  /// documents get watermarks and footer state marks.
  /// -> str
  status: "released",
  /// The latest revision date shown on the title page and in the running
  /// header.
  /// -> str
  date: none,
  /// Ordered author dictionaries with `display_name`, optional `orcid`
  /// and `corresponding`, and `affiliations` identifiers.
  /// -> array
  authors: none,
  /// Affiliation records keyed by identifier, each with a `name` and
  /// optional `address` and `ror`.
  /// -> dictionary
  affiliations: none,
  /// Running-header title; defaults to the title.
  /// -> str | none
  short-title: none,
  /// Optional subtitle shown below the title.
  /// -> str | none
  subtitle: none,
  /// Bare DOI rendered as a link on the title page.
  /// -> str | none
  doi: none,
  /// Document source link shown after the body.
  /// -> str | none
  repository-url: none,
  /// Abstract rendered in the front matter; a plain string also becomes
  /// the PDF description.
  /// -> content | str | none
  abstract: none,
  /// Change-record entries with `version`, `date`, `description`, and
  /// `author` fields.
  /// -> array
  changes: (),
  /// Whether to render a table of contents.
  /// -> bool
  toc: true,
  /// Bibliography sources loaded with `read(path, encoding: none)` from
  /// the document.
  /// -> bytes | array | none
  bibliography: none,
  /// A bundled citation style name or a CSL file path; `auto` selects the
  /// bundled Rubin AAS style, which follows aasjournal.bst and renders
  /// Rubin document handles from bibliography keys.
  /// -> auto | str
  bibliography-style: auto,
  /// List all bibliography entries, not only the cited ones.
  /// -> bool
  bibliography-full: false,
  /// The document body.
  /// -> content
  body,
) = {
  assert(nonempty(title), message: "The title field is required")
  assert(nonempty(date), message: "The date field is required")
  assert(authors != none, message: "The authors field is required")
  assert(affiliations != none, message: "The affiliations field is required")
  validate-status(status)
  if series != none {
    validate-series(series)
  }
  validate-doi(doi)
  let displayed-short-title = if nonempty(short-title) { short-title } else { title }
  let author-names = authors.map(author => author.at("display_name"))

  set document(
    title: title,
    author: author-names,
    description: if type(abstract) == str { abstract } else { none },
  )
  set text(font: ("Open Sans", "Arial", "Helvetica"), size: 11pt, lang: "en")
  set par(justify: true, leading: 0.8em, spacing: 1em)
  set heading(numbering: "1.1")
  set math.equation(numbering: "(1)")
  show heading.where(level: 1): set text(size: 17pt, weight: "bold", fill: rubin-teal)
  show heading.where(level: 2): set text(size: 13pt, weight: "bold", fill: rubin-teal)
  show heading.where(level: 3): set text(size: 11pt, weight: "bold", fill: rubin-teal)
  // Give sections air comparable to the LaTeX class rather than Typst's
  // tighter defaults. The em units scale with each level's text size. A
  // level-filtered show-set (heading.where(level: ..)) must not be used
  // here: it breaks the tagged list structure under PDF/UA-1.
  show heading: set block(above: 1.8em, below: 1em)
  show figure.caption: it => align(center, text(size: 9pt, it))
  // Table figures may span pages, with the caption before the table and
  // repeated headers supplied by table.header.
  show figure.where(kind: table): set block(breakable: true)
  show figure.where(kind: table): set figure.caption(position: top)
  show link: it => {
    let destination = it.dest
    // ORCID links are shown as the icon alone; internal links keep the
    // ordinary text styling.
    let is-external = type(destination) == str and (
      destination.starts-with("https://") or destination.starts-with("http://")
    )
    if is-external and not destination.starts-with("https://orcid.org/") {
      url-styled(it)
    } else {
      it
    }
  }
  // Citations link into the reference list; style them like external
  // links so they are easy to spot, matching the hyperref link treatment
  // in the LaTeX class. Adjacent citations still merge into one group.
  show cite: url-styled

  set page(
    paper: "us-letter",
    margin: (left: 1in, right: 1in, top: 0.6in, bottom: 0.55in),
    header: none,
    footer: none,
    background: state-background(status),
    foreground: render-title-artwork(),
  )

  // Machine-readable front matter, the Typst counterpart of the annotated
  // abstract structures in Markdown and reStructuredText technotes. Tooling
  // extracts it from the compiled document with
  // `typst eval 'query(<rubin-technote>).first().value' --in <file>`.
  [#metadata((
    id: id,
    series: series,
    status: status,
    date: date,
    title: title,
    abstract: abstract,
  )) <rubin-technote>]

  render-title-page(
    title: title,
    subtitle: subtitle,
    id: id,
    series: series,
    status: status,
    date: date,
    doi: doi,
    authors: authors,
    affiliations: affiliations,
  )

  pagebreak()
  set page(
    margin: (left: 1in, right: 1in, top: 1.4in, bottom: 0.75in),
    header: none,
    footer: running-footer(series, status),
    foreground: running-header(displayed-short-title, id, date),
    numbering: "i",
  )
  counter(page).update(1)

  render-abstract(abstract)
  render-change-record(changes)
  render-contents(enabled: toc)

  set page(numbering: "1")
  counter(page).update(1)
  align(center, text(size: 17pt, weight: "bold", fill: rubin-teal, title))
  v(12pt)

  body

  if nonempty(repository-url) {
    v(12pt)
    text(size: 8pt, fill: rgb("#555555"))[
      Document source: #link(repository-url)[#repository-url]
    ]
  }

  if bibliography != none {
    pagebreak()
    render-bibliography(
      bibliography,
      style: if bibliography-style == auto { "../assets/rubin-aas.csl" } else { bibliography-style },
      title: [References],
      full: bibliography-full,
    )
  }
}
