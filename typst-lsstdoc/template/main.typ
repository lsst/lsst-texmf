#import "@preview/rubin-technote:0.1.0": citeds, citedsp, lsstdoc, note, technote-args, warning

// Metadata, authors, and the document status come from technote.toml.
#show: lsstdoc.with(
  ..technote-args(toml("technote.toml")),
  title: "Document Title",
  abstract: [A short description of this document.],
  toc: false,
)

= Introduction

Add content here.
