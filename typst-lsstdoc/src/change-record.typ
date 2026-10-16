#import "utilities.typ": light-teal, nonempty, rubin-teal

#let render-change-record(
  changes,
  curator: none,
  repository-url: none,
  source-version: none,
  citation-information: none,
) = {
  if changes.len() > 0 {
    heading(level: 1, outlined: false, numbering: none)[Change Record]
    table(
      columns: (11%, 16%, 1fr, 22%),
      inset: 5pt,
      stroke: 0.5pt + rgb("#666666"),
      fill: (x, y) => if y == 0 { light-teal } else { none },
      table.header(
        repeat: true,
        [#text(weight: "bold", fill: rubin-teal)[Version]],
        [#text(weight: "bold", fill: rubin-teal)[Date]],
        [#text(weight: "bold", fill: rubin-teal)[Description]],
        [#text(weight: "bold", fill: rubin-teal)[Owner]],
      ),
      // Interpolate so that YAML scalars such as an unquoted version 0.1
      // (a float) are accepted as cell content.
      ..changes.map(change => (
        [#change.at("version")],
        [#change.at("date")],
        [#change.at("description")],
        [#change.at("author")],
      )).flatten(),
    )
  }

  // Document provenance follows the change table, as in lsstdoc.cls.
  let lines = ()
  if nonempty(curator) {
    lines.push((emph[Document curator:], [#curator]))
  }
  if nonempty(repository-url) {
    lines.push((emph[Document source location:], link(repository-url)))
  }
  if nonempty(source-version) {
    lines.push((emph[Version from source repository:], [#source-version]))
  }
  if nonempty(citation-information) {
    lines.push((emph[Cite as:], [#citation-information]))
  }
  if lines.len() > 0 {
    if changes.len() > 0 {
      v(8pt)
    }
    for (label, value) in lines {
      [#label #value #linebreak()]
    }
  }

  if changes.len() > 0 or lines.len() > 0 {
    pagebreak(weak: true)
  }
}
