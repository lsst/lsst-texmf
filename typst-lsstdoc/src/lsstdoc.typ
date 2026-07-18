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
/// Use as a show rule:
/// ```typ
/// #show: lsstdoc.with(
///   title: "My Technote",
///   id: "DMTN-999",
///   series: "DMTN",
///   date: "2026-07-16",
///   authors: people.authors,
///   affiliations: people.affiliations,
/// )
/// ```
///
/// - title (str, content): The document title.
/// - id (str): The document handle, for example "DMTN-999".
/// - series (str): The series key, validated against the shared Rubin
///   series data that also determines the displayed type label.
/// - status (str): One of "draft", "released", or "obsolete"; draft and
///   obsolete documents get watermarks and footer state marks.
/// - date (str): The latest revision date shown on the title page and in
///   the running header.
/// - authors (array): Ordered author dictionaries with `display_name`,
///   optional `orcid` and `corresponding`, and `affiliations` identifiers.
/// - affiliations (dictionary): Affiliation records keyed by identifier,
///   each with a `name` and optional `address` and `ror`.
/// - short-title (str, none): Running-header title; defaults to the title.
/// - subtitle (str, none): Optional subtitle shown below the title.
/// - doi (str, none): Bare DOI rendered as a link on the title page.
/// - repository-url (str, none): Document source link shown after the body.
/// - abstract (content, none): Abstract rendered in the front matter.
/// - changes (array): Change-record entries with `version`, `date`,
///   `description`, and `author` fields.
/// - toc (bool): Whether to render a table of contents.
/// - bibliography (bytes, array, none): Bibliography sources loaded with
///   `read(path, encoding: none)` from the document.
/// - bibliography-style (auto, str): A bundled citation style name or a CSL
///   file path; `auto` selects the bundled Rubin AAS style, which follows
///   aasjournal.bst and renders Rubin document handles from bibliography
///   keys.
/// - bibliography-full (bool): List all entries, not only the cited ones.
/// - body (content): The document body.
/// -> content
#let lsstdoc(
  title: none,
  id: none,
  series: none,
  status: "released",
  date: none,
  authors: none,
  affiliations: none,
  short-title: none,
  subtitle: none,
  doi: none,
  repository-url: none,
  abstract: none,
  changes: (),
  toc: true,
  bibliography: none,
  // auto selects the bundled Rubin AAS style; pass a bundled style name or
  // a CSL file path to override it.
  bibliography-style: auto,
  bibliography-full: false,
  body,
) = {
  assert(nonempty(title), message: "The title field is required")
  assert(nonempty(id), message: "The id field is required")
  assert(nonempty(series), message: "The series field is required")
  assert(nonempty(date), message: "The date field is required")
  assert(authors != none, message: "The authors field is required")
  assert(affiliations != none, message: "The affiliations field is required")
  validate-status(status)
  validate-series(series)
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
