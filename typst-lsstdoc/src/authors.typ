#import "utilities.typ": nonempty, value-or

#let orcid-icon-path = "../assets/orcid-id.png"

#let affiliation-order(authors) = {
  let ids = ()
  for author in authors {
    for id in value-or(author, "affiliations", default: ()) {
      if id not in ids {
        ids.push(id)
      }
    }
  }
  ids
}

#let author-item(author, markers-by-id, comma-before-marker: false, link-markers: false) = {
  let author-affiliations = value-or(author, "affiliations", default: ())
  let corresponding = value-or(author, "corresponding", default: false)
  // markers-by-id is none when affiliation display is disabled; the
  // corresponding-author star is independent of it.
  let marker-body = if markers-by-id == none { none } else {
    author-affiliations.map(id => if link-markers {
      link(label("affil-" + id), markers-by-id.at(id))
    } else {
      markers-by-id.at(id)
    }).join(",")
  }
  let marker-text = marker-body + if corresponding { "*" } else { "" }
  let orcid = value-or(author, "orcid", default: none)
  let orcid-content = if nonempty(orcid) {
    h(2pt) + link("https://orcid.org/" + orcid)[
      #box(width: 9pt, height: 9pt, baseline: 1.5pt)[
        #image(
          orcid-icon-path,
          width: 9pt,
          alt: "ORCID profile for " + author.at("display_name"),
        )
      ]
    ]
  } else { [] }
  let comma-content = if comma-before-marker { [,] } else { [] }
  let marker-content = if marker-text == none or marker-text == "" { [] } else { super(marker-text) }

  box(
    strong(author.at("display_name"))
      + orcid-content
      + comma-content
      + marker-content,
  )
}

#let join-authors(items) = items.join([ ], last: [ and ])

#let format-address(address) = {
  if type(address) == dictionary {
    address.values().filter(value => nonempty(value)).join(", ")
  } else {
    address
  }
}

#let affiliation-line(index, id, affiliations) = {
  let affiliation = affiliations.at(id)
  let address = value-or(affiliation, "address", default: none)
  [
    #super(str(index + 1)) #affiliation.at("name")#if nonempty(address) { [; #format-address(address)] }
  ]
}

#let render-authors(authors, affiliations, affiliation-style: "inline") = {
  assert(authors.len() > 0, message: "At least one author is required")
  let affiliation-ids = affiliation-order(authors)

  for id in affiliation-ids {
    assert(
      id in affiliations,
      message: "Unknown affiliation referenced by author data: " + id,
    )
  }

  let markers-by-id = if affiliation-style == "none" { none } else {
    let markers = (:)
    for (index, id) in affiliation-ids.enumerate() {
      markers.insert(id, str(index + 1))
    }
    markers
  }

  let author-content = authors.enumerate().map(((index, author)) => author-item(
    author,
    markers-by-id,
    // AAS style: each non-final comma precedes the affiliation markers,
    // but a two-author list has no comma before the "and".
    comma-before-marker: authors.len() > 2 and index < authors.len() - 1,
    // Deferred affiliations live on their own page; the markers link
    // to the entries there.
    link-markers: affiliation-style == "deferred",
  ))
  let affiliation-content = if affiliation-style == "inline" {
    affiliation-ids.enumerate().map(((index, id)) => affiliation-line(index, id, affiliations))
  } else {
    ()
  }

  align(center)[
    #set text(size: 10.5pt)
    #join-authors(author-content)
    #v(0.55em)
    #set text(size: 8pt)
    #for affiliation in affiliation-content {
      affiliation
      linebreak()
    }
    #if authors.any(author => value-or(author, "corresponding", default: false)) {
      [#super("*") Corresponding author]
    }
  ]
}

#let render-affiliation-page(authors, affiliations) = {
  heading(level: 1, outlined: false, numbering: none)[Affiliations]
  for (index, id) in affiliation-order(authors).enumerate() {
    // The label is the target of the title-page marker links.
    [#box(affiliation-line(index, id, affiliations))#label("affil-" + id)]
    linebreak()
  }
  pagebreak(weak: true)
}
