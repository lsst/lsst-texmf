#import "utilities.typ": rubin-teal

#let supported-statuses = ("draft", "released", "obsolete")

#let validate-status(status) = assert(
  supported-statuses.contains(status),
  message: "Unsupported document status: " + status,
)

#let state-label(status) = {
  validate-status(status)
  if status == "draft" {
    "D R A F T"
  } else if status == "obsolete" {
    "O B S O L E T E"
  } else {
    none
  }
}

#let state-color(status) = if status == "released" { rubin-teal } else { red }

#let controlled-series = ("LDM", "LSE", "LCA", "LTS", "LPM", "LEP", "RDO")

#let is-controlled(series) = controlled-series.contains(series)

#let controlled-notice(series, status) = {
  if status == "obsolete" {
    "This document is preserved for historical information only."
  } else if is-controlled(series) {
    "The contents of this document are subject to configuration control."
  } else {
    none
  }
}

#let state-background(status) = {
  validate-status(status)
  if status != "released" {
    place(
      center + horizon,
      rotate(
        -45deg,
        text(
          72pt,
          fill: rgb("#ededed"),
          weight: "bold",
          if status == "draft" { "Draft" } else { "Obsolete" },
        ),
      ),
    )
  }
}
