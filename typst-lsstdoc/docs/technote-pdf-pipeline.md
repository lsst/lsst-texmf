# Design: PDF output for Markdown and reStructuredText technotes

This document specifies the pipeline that renders existing Documenteer technotes as Rubin-styled PDFs using the `rubin-technote` Typst package.
It supersedes the "Proposal: PDF output for Markdown and reStructuredText technotes" section of [`design.md`](design.md), which proposed a single pandoc-plus-Lua path for both source formats.
The evidence gathered here shows that Markdown and reStructuredText need different converters, so the design splits into two front ends over one shared Typst back end.

The target is a best-effort companion PDF published alongside the HTML edition.
Markdown and reStructuredText technotes have no PDF at all today, so degrading gracefully on an exotic Sphinx construct is acceptable; silently dropping content is not.

## Decision

Two converters, one Typst template.

reStructuredText technotes convert with pandoc plus a small Lua filter, as originally proposed.
Markdown technotes convert with [mystmd](https://mystmd.org), whose Typst exporter understands MyST directives and roles as first-class syntax.

The earlier proposal assumed one converter could serve both.
That assumption fails for Markdown: pandoc has no MyST directive support, so every construct in a Markdown technote would have to be reconstructed from raw text in Lua.
The same constructs in reStructuredText are parsed natively by pandoc, because they are ordinary reStructuredText directives and roles.

## Evidence

Both routes were run against DMTN-349, a Markdown technote with an abstract directive, five SVG figures, twenty-four citations, five footnotes, and an `include` directive pulling in a 1,150-line appendix.
The mystmd route produced a 48-page PDF that compiled with no Typst errors.
Software versions were mystmd 1.10.1, pandoc 3.10, and Typst 0.15.0.

### Markdown source

| Construct | mystmd | pandoc 3.10 |
| --- | --- | --- |
| `{figure}` with an SVG | `#figure(image(...))` with caption, numbering, and the asset copied into the build directory | emitted unchanged as a fenced code block |
| `{cite:p}` and `{cite:t}` | `#cite(<key>)`, switching to `#cite(label("key"))` for keys containing dots | left as literal text |
| `{include}` | resolved, appendix present in the output | dropped with no diagnostic |
| footnotes | `#footnote[...]` | `#footnote[...]` |
| `{abstract}` | needs preprocessing (see below) | escaped into literal backticks |
| headings | emitted with slug labels, so cross-references resolve | emitted without labels |

The `{include}` result is the decisive one.
pandoc discarded roughly a third of the document and reported nothing.

### reStructuredText source

pandoc parses the relevant constructs natively:

- `.. figure::` becomes `#figure(image(...), caption: [...])`;
- `:cite:` becomes `#cite(label("..."))` for keys containing dots and `@key` otherwise;
- `:cite:t:` becomes `#cite(<key>, form: "prose")`;
- `.. abstract::` becomes a div the filter can identify and strip;
- footnotes become `#footnote[...]`.

pandoc 3.10 already emits every citation form correctly, including the `label()` escape for ADS-style keys.
The `Cite` handler in the `design.md` filter listing was written against an older pandoc and is now redundant.
Confirm this against a corpus before deleting it, in particular that a bare `@key` immediately followed by sentence punctuation still parses as a Typst label.

## Architecture

Three layers, of which only the middle one differs by source format.

1. **Typst back end.** The `rubin-technote` package, unchanged.
   It owns the title page, front matter, running furniture, document state, reference list, and bibliography style.
2. **Converter.** mystmd for Markdown, pandoc plus a Lua filter for reStructuredText.
   Each produces a Typst body and copies referenced assets.
3. **Metadata bridge.** `technote-args(toml("technote.toml"))`, unchanged.
   Both paths read the same untouched `technote.toml` the HTML build uses.

No technote metadata is duplicated on either path.
In the DMTN-349 run the title page handle, author name, ORCID marker, affiliation, revision date, and draft watermark all came from `technote.toml` with no edits to the repository.

## Markdown path

### The mystmd template

mystmd renders Typst through a template directory containing `template.yml` and a `template.typ` written in jtex syntax.
The template ships in this subtree at `myst-template/`, next to the Typst package it adapts, and travels with the existing subtree fetch that technotes already perform.

`template.typ` imports `rubin-technote` and spreads the mapped metadata:

```typst
#import "@preview/rubin-technote:0.1.0": lsstdoc, technote-args

#show: lsstdoc.with(
  ..technote-args(toml("[-options.technote_toml-]")),
  title: "[-doc.title-]",
  abstract: [
[-parts.abstract-]
  ],
  bibliography: read("[-doc.bibtex-]", encoding: none),
  toc: [# if options.show_toc #]true[# else #]false[# endif #],
)

[-IMPORTS-]

// mystmd hard-codes breakableDefault to true, which lets a figure split
// from its caption across a page break. Typst's own default is false;
// shadow the imported binding to restore it.
#let breakableDefault = false

[-CONTENT-]
```

`technote.toml` reaches the build directory by being declared in `template.yml` as an option of `type: file`.
mystmd copies such files in and rewrites the path, so the template reads the real metadata file rather than a transcription of it:

```yaml
options:
  - id: technote_toml
    type: file
    description: The Documenteer technote.toml metadata file.
```

Two constraints found while building this:

- `toc` is a reserved export property name in mystmd.
  The option must be called something else; `show_toc` is used above.
- A local template is selected with a path that resolves from the project root, such as `./myst-template`.
  A path mystmd cannot resolve on disk is treated as the name of a remote template and fails with a 404 against `api.mystmd.org`.
- mystmd emits `#let breakableDefault = true` into its macro file and precedes every figure with `#show figure: set block(breakable: breakableDefault)`.
  The value is hard-coded in the renderer with no configuration hook, and it inverts Typst's own default.
  A figure near a page boundary therefore splits, leaving the caption stranded at the top of the next page.
  The template shadows the imported binding between `[-IMPORTS-]` and `[-CONTENT-]`, which takes effect for every `#show` rule in the body.

### The dialect adapter

mystmd implements MyST, not Documenteer's Sphinx-flavored MyST.
The differences are small but every one of them loses or corrupts content, so a preprocessing step is required.
It reads the technote sources and writes a git-ignored build directory; the repository sources are never modified.

| Difference | Handling |
| --- | --- |
| Title is the leading `#` heading | Lift into frontmatter `title`, remove the heading so it is not repeated as a section. |
| `{abstract}` directive is unknown to mystmd | Lift the body into the frontmatter `abstract` part, which the template renders through `lsstdoc`. |
| `{bibliography}` directive has no Typst renderer in mystmd | Drop the directive *and* an immediately preceding `References` or `Bibliography` heading. The template owns the reference list, and a heading left behind renders as an empty section with the real reference list still appearing at the end. |
| Bare `@handle` is citation syntax in mystmd | Escape as `\@handle`. |
| Shared bibliographies are implicit in the Sphinx build | Emit a generated `myst.yml` listing `local.bib` and the shared files explicitly. |

The `@handle` case deserves emphasis because it is the only one that changes the meaning of valid source.
GitHub handles are common in Rubin prose, and mystmd reads each one as a citation.
DMTN-349 contains twenty such handles; every one became a broken citation, reported only as a warning while the build continued.
The escape must be applied outside code spans, code blocks, and email addresses.

### Build steps

mystmd invokes `typst compile` itself and offers no way to pass compiler flags, so it cannot locate the vendored `rubin-technote` package or its bundled fonts.
The Markdown path therefore exports Typst rather than PDF and compiles separately:

```make
pdf: $(PACKAGE_DIR) bibs
	python -m documenteer.technote.pdf prepare --output _build/pdf
	myst build _build/pdf/index.md --typst
	typst compile --root _build/pdf \
	  --package-path .typst-packages \
	  --font-path $(PACKAGE_DIR)/fonts \
	  --input source-version=$(GITVERSION)$(GITDIRTY) \
	  _build/pdf/_build/$(DOCNAME).typ $(DOCNAME).pdf
```

This mirrors the two-step shape already used by the `technote_typst` Makefile.
The `prepare` step is the dialect adapter; see [Where the code lives](#where-the-code-lives) for its interim home.

## reStructuredText path

Unchanged from the `design.md` proposal, with the filter reduced to what pandoc 3.10 still needs:

- strip the `abstract` div and the `refs` div, which the template owns;
- strip a `References` heading;
- map `{ref}` cross-references, which arrive as `#raw(lang: "interpreted-text", ...)` rather than as references;
- carry `:name:` labels from figures onto Typst labels, which pandoc currently drops.

The wrapper document is generated rather than hand-written, from the title and abstract lifted into pandoc metadata by the filter.

## Bibliographies

Both paths need `local.bib` plus the five shared files from `lsst-texmf`: `lsst.bib`, `lsst-dm.bib`, `refs.bib`, `refs_ads.bib`, and `books.bib`.

Documenteer's `githubbibcache` extension already downloads these for the HTML build and stores them under `.technote/bibfiles/lsst/lsst-texmf/main/texmf/bibtex/bib/`.
The PDF target reads that cache, downloading only when it is absent.
This is simpler than the `sync-bibs` target proposed in `design.md`, which would have maintained a second copy.

All five shared files parse cleanly under mystmd's bibtex parser.

One compatibility hazard: mystmd's parser is stricter than pybtex and rejects an entry whose key is not followed by a comma, such as `@MISC{ZPXWCS` on its own line.
pybtex accepts this, so such entries pass the HTML build unnoticed and exist in the wild.
DMTN-349's `local.bib` contains three.
A malformed entry causes mystmd to reject the entire file, which silently breaks every citation resolved from it.
The preprocessor should validate `local.bib` and fail with a message naming the offending entries rather than let the build proceed with an empty bibliography.

## Where the code lives

The mystmd template, the Lua filter, and their fixtures live in this subtree, so they are versioned with the Typst package whose interface they depend on.

The preprocessor and the build orchestration belong in Documenteer as `documenteer technote pdf`, as `design.md` proposes for the conversion step generally.
Until that lands, an equivalent script ships in this subtree so the pipeline is testable and usable from a technote Makefile.

Publishing remains outside this package: uploading the PDF alongside the HTML edition and linking it from the technote theme.

## Testing

Extend `tests/` with fixtures exercising both paths end to end.

The Markdown fixture covers an `{abstract}` directive, a `{figure}` with an SVG, an `{include}`, a citation with a dotted ADS key, a footnote, and a bare `@handle`.
Assertions run at three levels: on the generated `.typ`, so a regression names the construct that broke; on a successful `typst compile`, so template-level breakage is caught; and on the compiled document's structure with `typst eval 'query(...)'`, which is how both layout defects below were confirmed.

Two regressions found while building the DMTN-349 proof of concept have explicit checks, because both produce a valid document that is quietly wrong:

- every figure sits on the same page as its caption, asserted with `query(figure).map(it => it.location().page())` against the caption's page;
- the document contains exactly one `References` heading, on the page the template's reference list occupies.

Add a malformed `local.bib` fixture asserting that the preprocessor fails with a diagnostic naming the entry, since the failure mode it guards against is silent.

The reStructuredText fixture covers the same constructs in their reStructuredText spellings.

## Known limitations

- mystmd is a Node package. Technote repositories currently need only Python and Sphinx, so the Markdown path adds a toolchain. The `mystmd` PyPI distribution installs the Node CLI through pip, which keeps it inside the existing tox environment; whether to depend on it that way or require a separate install is open.
- mystmd resolves DOIs over the network during the build. Offline and CI behavior needs checking.
- Sphinx extensions with no MyST equivalent, and MyST directives mystmd does not implement, degrade to warnings. The preprocessor should promote an unknown-directive warning to an error so content loss is not silent.
- The two front ends will drift. The shared fixture set is what keeps the two paths producing comparable documents.
- Coverage beyond DMTN-349 is untested. Tables, math, and admonitions need spot-checking across a larger corpus on both paths.
