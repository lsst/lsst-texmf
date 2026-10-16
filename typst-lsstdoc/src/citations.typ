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
/// For example:
/// ```typ
/// The requirements are defined in #citeds("LPM-17"), which can also be
/// cited as #citeds("LPM-17", display: [the science requirements]).
/// ```
/// -> content
#let citeds(
  /// The bibliography key, for example "DMTN-000".
  /// -> str
  key,
  /// Alternate text shown instead of the key.
  /// -> content | none
  display: none,
) = {
  let destination = citation-label(key)
  // The lsstdoc show rule styles all citations like external links.
  cite(
    destination,
    supplement: display,
    style: citation-key-style,
  )
}

/// Cite a bibliography entry by key, wrapped in square brackets.
///
/// The Typst equivalent of the LaTeX `\citedsp` command.
/// For example:
/// ```typ
/// The series is described elsewhere #citedsp("DMTN-000").
/// ```
/// -> content
#let citedsp(
  /// The bibliography key, for example "DMTN-000".
  /// -> str
  key,
  /// Alternate text shown instead of the key.
  /// -> content | none
  display: none,
) = {
  text("[") + citeds(key, display: display) + text("]")
}
