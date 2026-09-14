#import "../src/lsstdoc.typ": lsstdoc
#import "../src/technote-toml.typ": technote-args

// The document loads technote.toml itself so the path resolves here, then
// spreads the mapped values into the template. Title and abstract remain in
// the document source, matching the Documenteer convention.
#show: lsstdoc.with(
  ..technote-args(toml("technote.toml")),
  title: "Reusing Documenteer Technote Metadata",
  short-title: "Technote Metadata Reuse",
  abstract: [
    This example drives the Rubin Typst template directly from the same
    `technote.toml` metadata file that Documenteer uses for Markdown and
    reStructuredText technotes, so author changes made with
    `documenteer technote add-author` and `sync-authors` are picked up on
    the next compile with no export step.
  ],
  toc: false,
)

= Metadata reuse

The document handle, series, status, revision date, repository link,
authors, and affiliations on the title page all come from
`technote.toml`. A `stable` technote renders as a released document.
