#import "utilities.typ": nonempty, rubin-logo-path, rubin-teal, series-label
#import "authors.typ": render-authors
#import "document-state.typ": state-color, state-label

#let observatory-image-path = "../assets/rubinobs.png"

#let render-title-artwork() = align(center + bottom)[
  #image(
    observatory-image-path,
    width: 8.5in,
    alt: "Illustration of Vera C. Rubin Observatory on Cerro Pachón",
  )
]

#let render-title-page(
  title: none,
  id: none,
  series: none,
  status: none,
  date: none,
  authors: none,
  affiliations: none,
  subtitle: none,
  doi: none,
) = {
  let label = state-label(status)

  // The content flows, so a long author list continues onto a second
  // page instead of colliding with the page furniture, matching the
  // lsstdoc.cls behavior. The observatory artwork is a first-page
  // background rather than a reserved region.
  align(center)[
    #pad(top: 18pt)[
      #grid(
        columns: (1fr,),
        rows: (auto, 18pt, auto, 4pt, auto),
        align: center,
        box(width: 170pt, height: 108pt, clip: true)[
          #align(center + horizon)[
            #image(
              rubin-logo-path,
              width: 265pt,
              alt: "Vera C. Rubin Observatory logo",
            )
          ]
        ],
        [],
        text(size: 17pt, weight: "bold", fill: rubin-teal)[Vera C. Rubin Observatory],
        [],
        text(size: 16pt, weight: "bold", fill: rubin-teal, if series == none { "" } else {
          series-label(series)
        }),
      )
    ]
    #v(60pt)
    #set text(hyphenate: false)
    #set par(justify: false)
    #text(size: 27pt, weight: "bold", fill: rubin-teal, title)
    #if nonempty(subtitle) {
      v(8pt)
      text(size: 13pt, fill: rubin-teal, subtitle)
    }
    #v(20pt)
    #render-authors(authors, affiliations)
    #v(16pt)
    #if nonempty(id) {
      text(size: 14pt, weight: "bold", id)
      v(7pt)
    }
    #if nonempty(doi) {
      // Pass the display text as a string: in markup a literal
      // https:// URL would swallow an interpolation as a fragment.
      let doi-url = "https://doi.org/" + doi
      text(
        size: 10pt,
        weight: "bold",
        link(doi-url, doi-url),
      )
      v(7pt)
    }
    #text(size: 11pt, weight: "bold")[Latest Revision: #date]
    #if label != none {
      v(14pt)
      text(size: 12pt, weight: "bold", fill: state-color(status), label)
    }
  ]
}
