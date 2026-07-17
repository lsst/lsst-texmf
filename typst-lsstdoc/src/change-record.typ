#import "utilities.typ": light-teal, rubin-teal

#let render-change-record(changes) = {
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
      ..changes.map(change => (
        change.at("version"),
        change.at("date"),
        change.at("description"),
        change.at("author"),
      )).flatten(),
    )
  }
}
