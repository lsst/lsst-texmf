#import "../src/lsstdoc.typ": lsstdoc

#let selected-status = sys.inputs.at("status", default: "released")

#show: lsstdoc.with(
  title: "Document State Smoke Test",
  short-title: "State Smoke Test",
  id: "DMTN-999",
  series: "DMTN",
  status: selected-status,
  date: "2026-07-16",
  authors: (
    (
      internal_id: "example",
      given_name: "First",
      family_name: "Author",
      display_name: "First Author",
      orcid: none,
      affiliations: ("RubinObs",),
    ),
  ),
  affiliations: (
    RubinObs: (
      name: "NSF-DOE Vera C. Rubin Observatory",
      address: "Tucson, Arizona, USA",
      ror: none,
    ),
  ),
  toc: false,
)

= State test

This minimal document verifies the `#selected-status` rendering path.
