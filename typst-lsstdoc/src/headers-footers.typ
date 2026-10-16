#import "utilities.typ": muted-teal, rubin-logo-path
#import "document-state.typ": controlled-notice, state-label

#let running-header(short-title, id, date) = context {
  place(center + top, dy: 30pt)[
    #block(width: 6.5in)[
      #grid(
        columns: (20%, 1fr),
        column-gutter: 12pt,
        align: (left + horizon, right + horizon),
        box(width: 72pt, height: 45pt, clip: true)[
          #align(center + horizon)[
            #image(rubin-logo-path, width: 112pt, alt: "Vera C. Rubin Observatory logo")
          ]
        ],
        text(
          size: 7pt,
          fill: muted-teal,
          weight: "bold",
          (short-title, id, "Latest Revision " + date)
            .filter(part => part != none)
            .join("  |  "),
        ),
      )
    ]
  ]
}

#let running-footer(series, status) = context {
  let notice = controlled-notice(series, status)
  let label = state-label(status)
  stack(
    dir: ttb,
    spacing: 4pt,
    line(length: 100%, stroke: 0.65pt),
    grid(
      columns: (1fr, 3fr, 1fr),
      align: (left + horizon, center + horizon, right + horizon),
      if label != none {
        text(size: 7pt, fill: red, weight: "bold", label)
      },
      align(center)[
        #if notice != none {
          text(size: 6.5pt, fill: muted-teal, weight: "bold", notice)
          linebreak()
        }
        #counter(page).display()
      ],
      if label != none {
        text(size: 7pt, fill: red, weight: "bold", label)
      },
    ),
  )
}
