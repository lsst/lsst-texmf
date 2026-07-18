#import "utilities.typ": nonempty

// Documenteer technote.toml status states mapped to lsstdoc statuses.
#let technote-status-map = (
  draft: "draft",
  stable: "released",
  deprecated: "obsolete",
)

#let strip-prefix(value, prefix) = {
  if value != none and value.starts-with(prefix) {
    value.slice(prefix.len())
  } else {
    value
  }
}

#let format-technote-date(value) = {
  if type(value) == datetime {
    value.display("[year]-[month]-[day]")
  } else {
    value
  }
}

/// Map a parsed Documenteer technote.toml dictionary onto lsstdoc arguments.
///
/// The caller loads the file, because paths resolve relative to the calling
/// module:
/// ```typ
/// #show: lsstdoc.with(
///   ..technote-args(toml("technote.toml")),
///   title: "My Technote",
/// )
/// ```
/// The mapping covers the handle, series, status, revision date, repository
/// URL, and the author list with deduplicated affiliations. URL-prefixed
/// ORCID and ROR identifiers are normalized to the bare form. The title and
/// abstract stay in the document, matching Documenteer.
///
/// - data (dictionary): The parsed technote.toml contents.
/// - date (auto, str): Override for the revision date; `auto` uses
///   `date_updated`, falling back to `date_created`.
/// - status (auto, str): Override for the document status; `auto` maps the
///   technote states draft, stable, and deprecated onto draft, released,
///   and obsolete.
/// -> dictionary
#let technote-args(data, date: auto, status: auto) = {
  let technote = data.at("technote")

  let resolved-status = status
  if resolved-status == auto {
    let state = technote.at("status", default: (:)).at("state", default: "draft")
    assert(
      state in technote-status-map,
      message: "Unsupported technote status state: "
        + state
        + ". Expected one of "
        + technote-status-map.keys().join(", ")
        + "; pass status: explicitly to override.",
    )
    resolved-status = technote-status-map.at(state)
  }

  let resolved-date = date
  if resolved-date == auto {
    let value = technote.at("date_updated", default: technote.at("date_created", default: none))
    assert(
      value != none,
      message: "technote.toml has no date_updated or date_created; pass date: explicitly.",
    )
    resolved-date = format-technote-date(value)
  }

  let authors = ()
  let affiliations = (:)
  for author in technote.at("authors", default: ()) {
    let name = author.at("name")
    let given = name.at("given", default: "")
    let family = name.at("family")
    let display = (given, family).filter(part => nonempty(part)).join(" ")

    let affiliation-ids = ()
    for affiliation in author.at("affiliations", default: ()) {
      let affiliation-id = affiliation.at("internal_id", default: affiliation.at("name"))
      affiliation-ids.push(affiliation-id)
      if affiliation-id not in affiliations {
        affiliations.insert(affiliation-id, (
          name: affiliation.at("name"),
          address: affiliation.at("address", default: none),
          ror: strip-prefix(affiliation.at("ror", default: none), "https://ror.org/"),
        ))
      }
    }

    authors.push((
      internal_id: author.at("internal_id", default: display),
      given_name: given,
      family_name: family,
      display_name: display,
      orcid: strip-prefix(author.at("orcid", default: none), "https://orcid.org/"),
      affiliations: affiliation-ids,
    ))
  }

  (
    doc-ref: technote.at("id"),
    series: technote.at("series_id"),
    status: resolved-status,
    date: resolved-date,
    repository-url: technote.at("github_url", default: none),
    authors: authors,
    affiliations: affiliations,
  )
}
