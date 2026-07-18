#import "../src/lsstdoc.typ": lsstdoc

#let people = yaml(sys.inputs.at("authors", default: "authors.yaml"))
#let selected-status = sys.inputs.at("status", default: "released")

#show: lsstdoc.with(
  title: "Document State Smoke Test",
  short-title: "State Smoke Test",
  id: "DMTN-999",
  series: "DMTN",
  status: selected-status,
  date: "2026-07-16",
  authors: people.authors,
  affiliations: people.affiliations,
  toc: false,
)

= State test

This minimal document verifies the `#selected-status` rendering path.
