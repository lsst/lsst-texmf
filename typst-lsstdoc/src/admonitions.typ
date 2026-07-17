#let admonition(body, title, accent, background) = block(
  width: 75%,
  fill: background,
  stroke: 0.8pt + accent,
  radius: 2pt,
  inset: 0pt,
  clip: true,
  breakable: false,
)[
  #grid(
    columns: (1fr,),
    rows: (auto, auto),
    block(width: 100%, fill: accent, inset: (x: 8pt, y: 5pt))[
      #text(fill: white, weight: "bold", title)
    ],
    pad(left: 8pt, right: 8pt, top: 7pt, bottom: 8pt, body),
  )
]

#let note(body, title: "Note") = admonition(
  body,
  title,
  rgb("#058b8c"),
  rgb("#f2fbfb"),
)

#let warning(body, title: none) = {
  let displayed-title = if title == none { "Warning" } else { "Warning: " + title }
  admonition(
    body,
    displayed-title,
    rgb("#b85c00"),
    rgb("#fff8f0"),
  )
}
