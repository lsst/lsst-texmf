#import "utilities.typ": nonempty, value-or

#let orcid-icon-path = "../assets/orcid-id.png"

#let affiliation-order(authors) = {
  let ids = ()
  for author in authors {
    for id in value-or(author, "affiliations", default: ()) {
      if not ids.contains(id) {
        ids.push(id)
      }
    }
  }
  ids
}

#let author-item(author, affiliation-ids, comma-before-marker: false) = {
  let author-affiliations = value-or(author, "affiliations", default: ())
  let markers = author-affiliations.map(id => str(affiliation-ids.position(value => value == id) + 1))
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

#let join-authors(items) = {
  if items.len() == 1 {
    items.first()
  } else {
    items.slice(0, items.len() - 1).join([ ]) + [ and ] + items.last()
  }
}

#let format-address(address) = {
  if type(address) == dictionary {
    address.values().filter(value => nonempty(value)).join(", ")
  } else {
    address
  }
}

#let render-authors(authors, affiliations, compact: false) = {
  assert(authors.len() > 0, message: "At least one author is required")
  let affiliation-ids = affiliation-order(authors)

  for id in affiliation-ids {
    assert(
      affiliations.keys().contains(id),
      message: "Unknown affiliation referenced by author data: " + id,
    )
  }

  let author-content = authors.enumerate().map(((index, author)) => author-item(
    author,
    affiliation-ids,
    comma-before-marker: index < authors.len() - 1,
  ))
  let affiliation-content = affiliation-ids.enumerate().map(((index, id)) => {
    let affiliation = affiliations.at(id)
    let address = value-or(affiliation, "address", default: none)
    [
      #super(str(index + 1)) #affiliation.at("name")#if nonempty(address) { [; #format-address(address)] }
    ]
  })

  align(center)[
    #set text(size: if compact { 9pt } else { 10.5pt })
    #join-authors(author-content)
    #v(0.55em)
    #set text(size: if compact { 7pt } else { 8pt })
    #for affiliation in affiliation-content {
      affiliation
      linebreak()
    }
    #if authors.any(author => value-or(author, "corresponding", default: false)) {
      [#super("*") Corresponding author]
    }
  ]
}
