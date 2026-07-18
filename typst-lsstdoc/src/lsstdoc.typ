#import "utilities.typ": nonempty, rubin-teal, url-styled, validate-series
#import "admonitions.typ" as admonitions
#import "document-state.typ": state-background, validate-status
#import "headers-footers.typ": running-footer, running-header
#import "title-page.typ": render-title-artwork, render-title-page
#import "front-matter.typ": render-abstract, render-contents
#import "change-record.typ": render-change-record
#import "citations.typ" as citations

#let render-bibliography = bibliography
#let note = admonitions.note
#let warning = admonitions.warning
#let citeds = citations.citeds
#let citedsp = citations.citedsp

#let lsstdoc(
  title: none,
  doc-ref: none,
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
  // Typst does not bundle the AAS CSL style. APA is a close bundled
  // author-year baseline; pass another bundled style name or a CSL file
  // path to override it.
  bibliography-style: "apa",
  bibliography-full: false,
  body,
) = {
  assert(nonempty(title), message: "The title field is required")
  assert(nonempty(doc-ref), message: "The doc-ref field is required")
  assert(nonempty(series), message: "The series field is required")
  assert(nonempty(date), message: "The date field is required")
  assert(authors != none, message: "The authors field is required")
  assert(affiliations != none, message: "The affiliations field is required")
  validate-status(status)
  validate-series(series)
  let displayed-short-title = if nonempty(short-title) { short-title } else { title }
  let author-names = authors.map(author => author.at("display_name"))

  set document(title: title, author: author-names)
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

  render-title-page(
    title: title,
    subtitle: subtitle,
    doc-ref: doc-ref,
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
    foreground: running-header(displayed-short-title, doc-ref, date),
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
      style: bibliography-style,
      title: [References],
      full: bibliography-full,
    )
  }
}
