#import "utilities.typ": rubin-teal, nonempty

#let render-abstract(abstract) = {
  if nonempty(abstract) {
    heading(level: 1, outlined: false, numbering: none)[Abstract]
    pad(left: 5%, right: 5%, abstract)
    pagebreak(weak: true)
  }
}

#let render-contents(enabled: true) = {
  if enabled {
    outline(title: [Contents], depth: 3)
    pagebreak(weak: true)
  }
}
