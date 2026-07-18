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

#let author-item(author, markers-by-id, comma-before-marker: false) = {
  let author-affiliations = value-or(author, "affiliations", default: ())
  let markers = author-affiliations.map(id => markers-by-id.at(id))
  let corresponding = value-or(author, "corresponding", default: false)
  let marker-text = markers.join(",") + if corresponding { "*" } else { "" }
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
  let marker-content = if nonempty(marker-text) { super(marker-text) } else { [] }

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

#let render-authors(authors, affiliations) = {
  assert(authors.len() > 0, message: "At least one author is required")
  let affiliation-ids = affiliation-order(authors)

  for id in affiliation-ids {
    assert(
      id in affiliations,
      message: "Unknown affiliation referenced by author data: " + id,
    )
  }

  let markers-by-id = (:)
  for (index, id) in affiliation-ids.enumerate() {
    markers-by-id.insert(id, str(index + 1))
  }

  let author-content = authors.enumerate().map(((index, author)) => author-item(
    author,
    markers-by-id,
    // AAS style: each non-final comma precedes the affiliation markers,
    // but a two-author list has no comma before the "and".
    comma-before-marker: authors.len() > 2 and index < authors.len() - 1,
  ))
  let affiliation-content = affiliation-ids.enumerate().map(((index, id)) => {
    let affiliation = affiliations.at(id)
    let address = value-or(affiliation, "address", default: none)
    [
      #super(str(index + 1)) #affiliation.at("name")#if nonempty(address) { [; #format-address(address)] }
    ]
  })

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
