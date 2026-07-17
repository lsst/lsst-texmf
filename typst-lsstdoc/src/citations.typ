#import "utilities.typ": url-blue

#let citation-key-style = "../assets/citation-key.csl"

#let citation-label(key) = {
  assert(type(key) == str and key != "", message: "Citation keys must be non-empty strings")
  label(key)
}

// Include a bibliography entry while displaying its key rather than a
// CSL-derived author, year, or number.
#let citeds(key, display: none) = {
  let destination = citation-label(key)
  let citation = cite(
    destination,
    supplement: display,
    style: citation-key-style,
  )
  underline(
    stroke: 0.45pt + url-blue,
    text(fill: url-blue, citation),
  )
}

#let citedsp(key, display: none) = {
  text("[") + citeds(key, display: display) + text("]")
}
