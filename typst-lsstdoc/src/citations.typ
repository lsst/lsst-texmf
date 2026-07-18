#import "utilities.typ": url-styled

#let citation-key-style = "../assets/citation-key.csl"

#let citation-label(key) = {
  assert(type(key) == str and key != "", message: "Citation keys must be non-empty strings")
  label(key)
}

/// Cite a bibliography entry by displaying its key.
///
/// This is the Typst equivalent of the LaTeX `\citeds` command: the entry
/// is added to the reference list, but the citation shows the bibliography
/// key (typically a Rubin document handle) instead of a CSL-derived
/// author, year, or number, and links to the entry.
///
/// - key (str): The bibliography key, for example "DMTN-001".
/// - display (content, none): Alternate text shown instead of the key.
/// -> content
#let citeds(key, display: none) = {
  let destination = citation-label(key)
  let citation = cite(
    destination,
    supplement: display,
    style: citation-key-style,
  )
  url-styled(citation)
}

/// Cite a bibliography entry by key, wrapped in square brackets.
///
/// The Typst equivalent of the LaTeX `\citedsp` command.
///
/// - key (str): The bibliography key, for example "DMTN-001".
/// - display (content, none): Alternate text shown instead of the key.
/// -> content
#let citedsp(key, display: none) = {
  text("[") + citeds(key, display: display) + text("]")
}
