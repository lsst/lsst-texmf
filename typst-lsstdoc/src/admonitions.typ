#import "utilities.typ": rubin-teal

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

/// Render a note admonition in the Rubin teal callout style.
///
/// The box is kept together across page breaks.
/// For example:
/// ```typ
/// #note(title: "Structured metadata")[
///   Authors do not need to copy metadata into presentation markup.
/// ]
/// ```
/// -> content
#let note(
  /// The note content.
  /// -> content
  body,
  /// The heading shown in the title bar.
  /// -> str | content
  title: "Note",
) = admonition(
  body,
  title,
  rubin-teal,
  rgb("#f2fbfb"),
)

/// Render a warning admonition in an orange callout style.
///
/// A custom title is prefixed with "Warning: " so that the severity is
/// always visible.
/// For example:
/// ```typ
/// #warning[
///   Do not edit the generated bibliography files by hand.
/// ]
/// ```
/// -> content
#let warning(
  /// The warning content.
  /// -> content
  body,
  /// Optional custom heading.
  /// -> str | content | none
  title: none,
) = {
  let displayed-title = if title == none { "Warning" } else { "Warning: " + title }
  admonition(
    body,
    displayed-title,
    rgb("#b85c00"),
    rgb("#fff8f0"),
  )
}
