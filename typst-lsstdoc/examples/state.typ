#import "../src/lsstdoc.typ": lsstdoc

#let metadata = yaml("metadata.yaml")
#let people = yaml(sys.inputs.at("authors", default: "authors.yaml"))
#let selected-status = sys.inputs.at("status", default: "released")

#show: lsstdoc.with(
  title: "Document State Smoke Test",
  short-title: "State Smoke Test",
  doc-ref: metadata.doc_ref,
  series: metadata.series,
  status: selected-status,
  date: metadata.date,
  authors: people.authors,
  affiliations: people.affiliations,
  toc: false,
)

= State test

This minimal document verifies the `#selected-status` rendering path.
