# Design and audit record for the rubin-technote package

This document records the Phase 1 source/rendering audit of Rubin Observatory's LaTeX `lsstdoc` class and the design decisions behind the working Typst proof of concept in this package.
The design target is the same Rubin look and feel, information hierarchy, branding, and page furniture.
Exact layout, font, pagination, or pixel equivalence with LaTeX is not required.

## Phase 1 scope and evidence

The inventory below is based on:

- [`lsstdoc.cls`](../../texmf/tex/latex/lsst/lsstdoc.cls), including its public class options, document commands, layout rules, and file/log writes;
- [`docs/lsstdoc.rst`](../../docs/lsstdoc.rst) and the checked-in LaTeX examples;
- [`db2authors.py`](../../bin/db2authors.py), [`authordb.py`](../../bin/authordb.py), and [`authordb.yaml`](../../etc/authordb.yaml);
- [`bibtools.py`](../../bin/bibtools.py), which contains the repository's actual document-series mapping;
- a local XeLaTeX build of `examples/DMTN-nnn.tex`, visually inspected as a seven-page PDF.

The source was inspected at repository revision `HEAD`; the most recent commit touching `lsstdoc.cls` was `8c4740042907bb7cd55b6ba16e1a8accdff7c131` (2025-10-03).
The rendering check used TeX Live 2025.
It is a behavioral baseline, not a claim that every historical document renders identically.

## Executive findings

1. The class is primarily a presentation layer, but requirements and meeting actions also create machine-readable build output.
   Those workflows should be redesigned around structured source data rather than emulated with Typst diagnostics.
2. The class displays a group/document-type option such as `DM` and accepts an arbitrary document handle, but it does not model Rubin document series coherently or check that a selected label agrees with the handle.
   The complete `TN_SERIES` key set in `bin/bibtools.py` is the prototype's source of truth for supported handle prefixes.
   Its labels are the baseline; the historically incorrect RDO label in `bibtools.py` has been corrected to match `lsstdoc.cls`.
   The separate inherited Gaia document-type catalog will not be ported.
3. The title page accepts one opaque LaTeX author block.
   The current `lsstdoc` mode of `db2authors.py` emits names only: it does not emit affiliations, ORCIDs, or email addresses.
   The prototype's structured author rendering is therefore an intentional extension, not a direct port.
4. The class infers controlled-document notices from handle prefixes (`LDM-`, `LSE-`, `LPM-`, and `RDO-`).
   An explicit metadata field is preferable, with prefix-based defaults retained only for compatibility.
5. Front-matter numbering has a notable edge case: `\maketitle` switches to Roman numbering unconditionally, but only the `toc` path resets to Arabic.
   Typst may use a cleaner native transition; small differences in the reset point or visible page sequence are acceptable.
6. The checked PDF is US Letter and untagged.
   Producing useful tagged or more accessible PDFs is a desirable Typst bonus and one motivation for the experiment, not a requirement to reproduce LaTeX behavior.
7. Directly loading structured YAML into the document is another motivating Typst advantage.
   The prototype should demonstrate it while avoiding a new, duplicated hand-maintained metadata source.

## Feature compatibility inventory

Status meanings:

- **Required**: needed in the representative prototype and acceptance test.
- **Representative**: implement a small native subset that proves feasibility.
- **Deferred**: document the workflow or compatibility issue, but do not block the first prototype on a full implementation.
- **Bonus**: a desirable Typst advantage rather than a LaTeX-parity gate.
- **Do not port**: obsolete, unused, or better replaced by structured data.

### Public LaTeX interface summary

The class options fall into overlapping groups:

- document state and behavior: `lsstdraft`, `obsolete`, `authoryear`, `toc`, and `notoc` (`onecolumn` and `twocolumn` are explicitly ignored);
- inherited content-type labels: `CP`, `MN`, `PR`, `SP`, `TN`, `TR`, `DP`, `DDP`, `SRS`, `SDD`, `ICD`, `SUM`, `SRN`, `STP`, `STS`, `STR`, `VTR`, `SOW`, `SPAR`, `PL`, `UG`, and `SSS`;
- organizational labels: `PST`, `DP`, `PF`, `DM`, `CTN`, `TS`, `SE`, `RDO`, `PMO`, and `OPS`.

`DP` occurs in both of the last two groups, and the later Data Production definition wins.
Both content types and organizations overwrite the same displayed `\docType` value, so selecting more than one label option creates a processing-order-dependent result.
This catalog is recorded as audit evidence only; the Typst prototype will not expose it.

There will be no Typst `doc-type`, group, or organization argument.
The `TN_SERIES` entry alone supplies the document's public type label.

The active title/front-matter interface is `\title`, `\author`, `\date` or `\setDocDate`, `\setDocSubtitle`, `\setDocRef`, `\setDocDOI`, `\setDocCurator`, `\setDocCitationInformation`, `\setDocUpstreamLocation`, `\setDocUpstreamVersion`, `\setDocAbstract`, `\setDocChangeRecord` with `\addtohist`, and one of `\maketitle`, `\mkshorttitle`, or `\mkmemotitle`.
`\setDocCompact` alters the full-title flow.
The legacy metadata setters listed later in this inventory do not provide active metadata behavior.

The other substantial public interfaces are `issueList`/`\addissue`, the requirement commands, the action-item commands, `note`, `warning`, `draftnote`, glossary commands supplied by the loaded package, standard bibliography commands, and convenience cross-reference/domain macros.
The prototype should expose native document concepts, not aliases for this entire TeX macro surface.

The prototype's public series set is the complete `TN_SERIES` mapping from `bin/bibtools.py`:

| Series/handle prefix | Display label |
| --- | --- |
| `DMTN` | Data Management Technical Note |
| `RTN` | Technical Note |
| `PSTN` | Project Science Technical Note |
| `SCTR` | Commissioning Technical Report |
| `SITCOMTN` | Commissioning Technical Note |
| `SMTN` | Simulations Team Technical Note |
| `SOTN` | Summit Operation Technical Note |
| `SQR` | SQuaRE Technical Note |
| `ITTN` | Information Technology Technical Note |
| `TSTN` | Telescope and Site Technical Note |
| `DMTR` | Data Management Test Report |
| `LDM` | Data Management Controlled Document |
| `LSE` | Systems Engineering Controlled Document |
| `LCA` | Camera Controlled Document |
| `LTS` | Telescope & Site Controlled Document |
| `LPM` | Project Controlled Document |
| `LEP` | Education and Public Outreach Controlled Document |
| `CTN` | Camera Technical Note |
| `RDO` | Rubin Directors Office |
| `Agreement` | Formal Construction Agreement |
| `Document` | Informal Construction Document |
| `Publication` | LSST Construction Publication |
| `Report` | Construction Report |

`bin/bibtools.py` previously labeled RDO as “Data Management Operations Controlled Document”; that value was a bug and has been corrected to the `lsstdoc.cls` label “Rubin Directors Office”.

The implementation should not maintain an unchecked second copy of this mapping in Typst.
`data/series.yaml` is the Typst-readable copy, and a parity test asserts exact key/label agreement with `bibtools.py`.
The same data file records which series are subject to configuration control.
The mixed-case keys `Agreement`, `Document`, `Publication`, and `Report` are part of the mapping and must be preserved.

### Layout and visual design

| Feature | LaTeX behavior and interface | Priority | Proposed Typst approach | Compatibility notes |
| --- | --- | --- | --- | --- |
| Page size | `article` at 11 pt on US Letter. | Required | `#set page(paper: "us-letter", ...)`. | Rendered PDF is 612 x 792 pt. Reject or explicitly support other sizes rather than silently accepting them. |
| Margins and page frame | `geometry` uses 6.5 in text width, 8.5 in text height, 1 in left margin, 55 pt header height, 2 em header separation, 60 pt margin-note width, and 40 pt footer skip. | Required | Encode named layout constants in one module and use page margins/header/footer regions. | `includeall` makes the effective vertical geometry more subtle than four independent margins. Match the visible baseline, not the package arithmetic. |
| Body typography | Open Sans, 11 pt, with `\baselinestretch` 1.25. Paragraphs have no first-line indent and one baseline of paragraph separation. | Required | Use a convenient, widely available humanist sans-serif with similar weight and proportions; preserve the overall density, hierarchy, no-indent paragraphs, and block spacing. | Open Sans is a baseline reference, not a compatibility requirement. Prefer a reproducible default that is easy to use locally and in CI. |
| Monospace font | Inconsolata. | Representative | Use a convenient, readable monospace for raw/code content; use Inconsolata when it is readily available. | Exact font matching is unnecessary. Do not copy font files into the prototype merely to match LaTeX. |
| Mathematics font | XITS Math with XeLaTeX; `newtxmath` is the pdfLaTeX fallback. | Representative | Use Typst's convenient default math font or another reproducible compatible choice. | Preserve mathematical clarity and hierarchy, not glyph identity or TeX spacing. |
| Small caps | XeLaTeX config names Carrois Gothic SC, although the main title design mostly uses bold Open Sans. | Deferred | Use real small caps only where available; otherwise document the fallback. | Carrois Gothic SC was not found in the repository font assets inspected. Caption labels currently rely on small caps. |
| Rubin color | Title, headings, header, and controlled footer use RGB (5, 139, 140), hex `#058B8C`. | Required | Define one Rubin teal constant with optional component aliases. | The class exposes five color names but initializes all five to the same value. |
| Section headings | Teal, bold headings: section `Large`, subsection `large`, subsubsection normal size, with compact before/after spacing. Numbering extends through level 5 and the TOC through level 3. | Required | Show rules for heading levels 1-3; retain native numbering and references. | Deeper levels inherit the base article style and need only representative coverage. |
| Captions | Small, centered captions; the label is small caps followed by a colon. Long captions use a centered block at 90% width. There is 10 pt above and no configured space below. | Required | Customize `figure.caption` and table captions with a 90% maximum width. | Typst's line breaking will differ; preserve hierarchy and alignment. |
| Footnotes | No class-specific redesign; behavior is inherited from `article` with the selected fonts and spacing. | Representative | Use native Typst footnotes and check size/spacing visually. | There is no special LaTeX contract to port. |
| Figures and tables | Native LaTeX floats; figures default to `!htbp`. Float pages may be 50% full, with generous top/bottom fractions and up to five floats per page. `longtable`, `tabularx`, and `multirow` are loaded. | Required | Use native figures/tables; exercise a figure, a multi-page table, captions, and references. | Placement is a semantic equivalence target, not a pagination target. Complex spanning tables may need explicit component helpers. |
| Code listings | The `listings` package is loaded, but the class defines no Rubin-specific listing style. Inline `\code` uses monospace. | Required | Use Typst raw blocks and inline raw text with a small local style. | Syntax highlighting and line-breaking will differ unless a policy is defined. |
| Lists | Ordinary lists plus compact `enumerate_single` and `itemize_single` variants. | Representative | Provide normal native lists and one compact list helper if the example needs it. | No need to reproduce TeX length manipulation exactly. |
| Admonitions | `note` and `warning` render 75%-width colored boxes. `draftnote` is visible only in draft mode. | Representative | Local box component with state-aware draft-note inclusion. | Useful class behavior, but secondary to the acceptance criteria. |

### Title page and document metadata

| Feature | LaTeX behavior and interface | Priority | Proposed Typst approach | Compatibility notes |
| --- | --- | --- | --- | --- |
| Full title page | `\maketitle` places the Rubin logo near the top, Rubin/type text and title centrally, author/handle/date below, and a pale observatory image along the bottom. It suppresses normal page furniture. | Required | A dedicated title-page function using the `TN_SERIES` display label, a stable vertical grid, and page background/foreground layers. | The prototype uses a supplied official color SVG logo and retains the class's pale `rubinobs.png` observatory image. Confirm redistribution terms before packaging. |
| Document title and short title | `\title[short]{long}`; the long title appears on the title page and the short title in running headers. | Required | Required `title`; optional `short-title` defaults to `title`. | Typst metadata should also receive the long title for the PDF information dictionary. |
| Subtitle | `\setDocSubtitle`; shown below the title and appended to the PDF title. | Representative | Optional `subtitle`. | It is absent from the proposed minimum example but cheap to support. |
| Document handle | `\setDocRef`; displayed on title page/header and stored as a PDF keyword. Its prefix also triggers controlled-document state. | Required | Required `doc-ref`, validated as a non-empty string; derive series when possible but keep it explicit. | Prefix inference is coupled to governance policy and must not be the sole source of truth. |
| Document series/handle prefix | The handle is opaque to the title layout, and the class options do not represent the full Rubin series set. `bin/bibtools.py` contains the authoritative `TN_SERIES` key set. | Required | Support every `TN_SERIES` key and derive the display label from a corrected shared mapping. | The previously erroneous `bibtools.py` label for RDO has been corrected at the source. Series/handle agreement should produce a clear error. Do not carry the separate Gaia-derived class-option catalog into the public Typst API. |
| Revision date | `\date` aliases `\setDocDate`. The title/header label it `Latest Revision`. `\setDocRevision` is only a warning and stores nothing. | Required | Use the ISO `date` as the sole displayed latest-revision value. | Git branch names and other build labels are deliberately excluded from page furniture. |
| DOI | `\setDocDOI`; title page prints a linked `https://doi.org/...`. | Required | Optional bare DOI rendered as a link. | The template rejects URL-prefixed or malformed values; only the bare identifier is accepted. |
| Repository/source URL | `\setDocUpstreamLocation` is printed after the change table, not on the title page. `\setDocUpstreamVersion` and curator/citation fields appear there too. | Representative | Optional `repository-url`, `source-version`, `curator`, and `citation-information`, placed in front matter. | The prototype plan proposes repository URL on the title page; that is a deliberate design change and should be called out in PDF comparisons. |
| Local logo | `\setDocLocalLogo` stores a value but the class never reads it. | Do not port | Add a documented secondary-logo slot only if a real target document requires it. | Treating the dormant macro as a requirement would create false compatibility work. |
| PDF metadata | `\maketitle` sets title, author, and handle keyword through `hyperref`. | Required | Set Typst document title/author metadata and inspect the generated PDF. | The rendered baseline had no custom metadata stream and was untagged. |
| Compact title mode | `\setDocCompact` suppresses some vertical space and a title-page break. | Deferred | Prefer an explicit `compact-title: false` option only after testing a concrete use case. | Current setter semantics are truthiness-by-emptiness rather than a real Boolean. |
| Short title and memo variants | `\mkshorttitle` prints a small title/author/date block. `\mkmemotitle` changes geometry and prints logo, address, To/From/Subject. | Deferred | Separate template entry points after the main technical-note prototype is stable. | They are distinct document forms, not variants that should complicate the first `lsstdoc` API. |
| Legacy metadata setters | `\setDocIssue`, `\setDocStatus`, `\setDocRevision`, `\setDocAffil`, `\setDocApprove`, and `\setDocAuthorize` emit warnings or are unsupported. `\setDocAuthor` is not used by title rendering. | Do not port | Omit them; document migration to structured metadata. | Compatibility aliases would hide errors and preserve unused concepts. |

### Authors and affiliations

| Feature | LaTeX/tool behavior | Priority | Proposed Typst approach | Compatibility notes |
| --- | --- | --- | --- | --- |
| Multiple authors | `\author` is an opaque formatted string. `db2authors.py -m lsstdoc` preserves the requested order and generates a comma/`and` name list. | Required | Ordered author dictionaries from YAML, rendered by the template. | Keep presentation out of generated data. |
| Author names | AuthorDB stores `given_name` and `family_name`; `db2authors` derives plain and LaTeX display forms. Empty given names can represent collaborations. | Required | Export `internal_id`, component names, and a normalized `display_name`. | Some database strings contain LaTeX escapes; conversion/normalization must be tested rather than passed directly to Typst. |
| Affiliations | AuthorDB stores affiliation IDs and structured institute/department/address/ROR data. The current `lsstdoc` generator discards all of it. Other generators number deduplicated affiliations in first-use order. | Required | Export referenced affiliation records keyed by stable ID; the template assigns stable first-use numeric markers. | The new title page is intentionally richer than current `lsstdoc` output. Preserve document author order and per-author affiliation order. |
| ORCID | AuthorDB stores bare identifiers. `authordb.py` validates dashed or 16-character forms; the current `lsstdoc` generator discards ORCID. | Required | Export the bare normalized identifier and render the standard small ORCID icon linked to `https://orcid.org/...`, following AASTeX practice. | The identifier is not printed on the title page. Validation is shared by AuthorDB and the exporter; checksum validation is not currently implemented. Confirm icon redistribution terms before packaging. |
| Corresponding author | Not represented in the current AuthorDB model. | Representative | Optional per-document overlay in the authors input, defaulting to false. | It cannot be truthfully generated from AuthorDB without a schema or document-local source. |
| Email | AuthorDB can resolve a username through an affiliation's email domain. Current `lsstdoc` output does not show email. | Representative | Export only when requested; hide by default. | Avoid putting personal email into output merely because it exists in the database. |
| Institutional authors | `authordb.py` recognizes a collaboration as an empty given name with affiliation `"_"`. | Required | Preserve a `kind` or equivalent derived flag and allow an author with no ordinary affiliation markers. | The Typst schema must not require every author to be a person. |
| Long author lists | No dedicated title-page layout; the opaque author string simply wraps. | Required | Add regular and compact rendering modes, selected explicitly or by a documented threshold. | Each display name, ORCID icon, comma, and affiliation marker is an unbreakable inline box, equivalent to TeX's `Tim~Jenness`. Following AASTeX style, each non-final comma precedes that author's affiliation marker, with “and” before the final name; wrapping is allowed only between authors. |

### Page furniture, state, and front matter

| Feature | LaTeX behavior and interface | Priority | Proposed Typst approach | Compatibility notes |
| --- | --- | --- | --- | --- |
| Running header | Left: Rubin logo at 18% of text width. Right: tiny teal bold short title, handle, and latest-revision date separated by vertical bars. Title page is empty style. | Required | Contextual page header suppressed on the title page. | The current LaTeX build warns that 55 pt is too small for the actual header (about 62 pt). Match the visible result without reproducing the warning/overfull geometry. |
| Running footer | A 1 pt top rule, centered page number, controlled-document text when applicable, and red draft/obsolete marks at the sides for uncontrolled documents. | Required | One state-aware footer function driven by explicit metadata. | Long controlled text needs wrapping tests. |
| Draft state | `lsstdraft` adds a pale 45-degree `Draft` watermark to every page, red title-page state, and red footer notices. `\XXX` and `draftnote` content are visible only in draft mode. | Required | `status: "draft"` and centralized state rendering. | The rendered example confirms the watermark and footer on front and main matter. |
| Released state | Default: no watermark/state label. Controlled notices still appear when inferred from the handle. | Required | `status: "released"`. | Make released explicit in metadata even though it is implicit in LaTeX. |
| Obsolete state | `obsolete` adds a watermark and prominent state text. It replaces approval wording with historical-information wording. | Required | `status: "obsolete"`, overriding controlled approval wording. | Documentation says draft and obsolete must not be combined, but the class does not enforce that. An enum should make the invalid combination impossible. |
| Controlled-document notices | Handle prefixes select one of general CCB, DM CCB, or RDO CCB wording blocks; obsolete overrides them. | Required | Explicit controlled-document policy with defaults derived from the authoritative series mapping. | A Boolean alone cannot reproduce the distinct notice texts. `TN_SERIES` also identifies LCA, LTS, and LEP as controlled documents although the class does not infer control for those prefixes; governance wording therefore needs review rather than blind class parity. |
| Front matter | Full title page, abstract, change record, and optional TOC. `\maketitle` switches to Roman numbering after the title page. | Required | Compose explicit front-matter components inside `lsstdoc`, using Typst-native page numbering. | The rendered example's title page consumes Roman page i but prints no number and the abstract begins at ii. Reproducing that exact sequence is not required. |
| Main matter | With `toc`, the class clears the page, resets to Arabic 1, and repeats the document title before the first section. Without `toc`, authors must reset numbering themselves. | Required | Use a simple automatic transition or a small public `lsst-main-matter()` helper, whichever is more idiomatic in Typst. | Arabic main-matter numbering is desirable, but small differences in reset timing or page sequence are acceptable. Do not preserve the `toc` coupling merely for parity. |
| Table of contents | `toc` option; depth 3, 1.5 spacing, followed by clear page and Arabic reset. | Required | Native outline with configurable depth and an explicit Boolean. | `notoc` is redundant and also resets citation mode in the class; do not copy that coupling. |
| Lists of figures/tables | No class-specific automatic support; standard LaTeX commands are available to document authors. | Representative | Optional native outlines for figure/table kinds. | Treat their appearance as new prototype design, not class parity. |
| Change record | `\setDocChangeRecord` inserts a `longtable` with Version, Date, Description, Owner name; headers repeat and continuation text is added. Curator/source/citation fields follow it. | Required | Structured change list rendered by a table component with repeating headers if Typst supports it. | Preserve source order; test long descriptions and page breaks. |
| Issue list | `issueList`/`\addissue` render a two-column ID/Summary long table. | Representative | Structured issue data and a reusable two-column table. | It has no extraction side effect. |

### Bibliography, cross-references, glossaries, and technical content

| Feature | LaTeX behavior and interface | Priority | Proposed Typst approach | Compatibility notes |
| --- | --- | --- | --- | --- |
| Bibliography engine/style | Class forces BibTeX `lsst_aa.bst`; `natbib` is numeric by default and author-year with the `authoryear` option. | Required | Use Typst's native bibliography support. The prototype uses bundled APA author-year output because Typst 0.15 does not bundle AAS CSL. | Exact `lsst_aa.bst` rendering is unnecessary. A Rubin/AAS CSL file is optional follow-up work. |
| Existing `.bib` files | Repository provides `lsst`, `lsst-dm`, `refs`, `books`, and `refs_ads`; the baseline example built all five. The style recognizes Rubin-specific fields including `handle`, plus ADS/e-print fields. | Required | Compile a curated cross-section of real entries with Typst and record parse/render failures. | LaTeX commands, brace-protected acronyms, collaboration authors, and custom `@DocuShare` behavior are likely normalization points. Do not rewrite the canonical files during the experiment. |
| Citation-key display | `\citeds` uses the bibliography key in place of a derived year; alternate text still cites the same entry. `\citedsp` adds brackets. | Implemented | Generic `citeds` and `citedsp` helpers use a small CSL style whose citation layout selects `citation-key`; caller-supplied text is passed as the citation locator. | The helpers depend only on the bibliography key, not a custom `handle` field or a particular BibTeX layout. They retain Typst's native link to the exact bibliography entry and render as blue underlined links. |
| Cross-references | Standard labels/hyperref plus convenience names for sections, figures, tables, equations, requirements, actions, and appendices. | Required | Native labels and references, with small semantic helpers only where output wording matters. | Avoid translating the large library of domain-specific TeX convenience macros. |
| Equations | AMS math/unicode math and bold-vector helpers. | Required | Native Typst equations, labels, and references. | Visual math differs; verify semantic content and numbering. |
| Appendices | Standard LaTeX `\appendix`; no special class layout. | Required | Native appendix heading/numbering configuration. | Exercise at least one appendix in the representative document. |
| Glossary/acronyms | `glossaries` is loaded, but document definitions are generated externally by `generateAcronyms.py`; glossary compilation requires additional passes/tools. | Representative | Structured YAML plus a small local acronym API for the example. | First-use tracking and full glossary generation require a focused experiment. This is both template and build-system work. |

The bibliography compatibility fixture must include at least `@article`, `@book`, `@inproceedings`, `@techreport`, `@software`, and `@misc`, plus DOI, URL, e-print/arXiv, institutional author, collaboration author, and brace/LaTeX-markup cases.
Missing entry types in the repository corpus should be supplied by synthetic fixtures rather than by editing canonical `.bib` files.

### Build-time behavior and workflow redesign

| Feature | Current behavior | Priority | Proposed Typst/workflow approach | Compatibility notes |
| --- | --- | --- | --- | --- |
| Requirements | `reqblock`, `reqinsert`, `req`, `reqapp`, `reqsimp`, and `reqdel` assign sparse IDs, render requirement boxes, and write `REQ:` records to the TeX log for downstream CSV tooling. Deleted requirements may exist only in log output. | Deferred | If later demand justifies it, make requirements YAML authoritative; validate IDs/parents/status, render from that data, and export any required CSV from the same source. | Requirements are rarely used and are explicitly outside the initial implementation. Parsing Typst diagnostics would recreate a fragile implementation accident. |
| Meeting actions | `\action`, `\nolabelaction`, and `\oldaction` write `actions`/`oldactions` files, emit `AI:` log records, place margin labels, and later input the files into `\listofactions`. | Deferred | If later demand justifies it, use structured action YAML plus a renderer/exporter. | Action items are rarely used and are explicitly outside the initial implementation. Direct page-time file writes do not map naturally to Typst. |
| Acronym generation | `generateAcronyms.py` scans source, writes TeX definitions/tables, and may require `makeglossaries` and repeated LaTeX passes. | Deferred | Separate preprocessing/validation around a neutral glossary data file. | Source rewriting (`-gu`) is explicitly described as potentially surprising and should not be replicated. |
| Bibliography pipeline | BibTeX plus LaTeX reruns; standard bibliography files are found through TEXMF. | Required | One Typst compile using explicit `.bib` paths, with all required resources declared in the build command. | Pin Typst and CSL inputs for reproducibility. |
| Author generation | `db2authors.py` reads a flat `authors.yaml` from the working directory, resolves `etc/authordb.yaml`, filters IDs through `dni.yaml`, and prints format-specific markup to stdout. | Required | Add a neutral YAML output mode that reuses the validated database model and accepts explicit input/output paths consistent with current CLI conventions. | The current CLI's `-m/--mode` means output mode, so `-m typst-yaml` is more consistent than introducing `--format` unless the CLI is deliberately modernized. Preserve requested order and DNI behavior only if it is part of the target document workflow. |
| Native YAML metadata | Repository documents already carry `metadata.yaml` for Documenteer/indexing; the class separately receives title/author/handle/date in TeX. | Required | Load authoritative YAML directly with Typst's data functions and pass structured values into the template. Generate or derive any secondary form. | Direct YAML loading is a strategic Typst benefit rather than visual parity. Reconcile names such as `doc_title`/`doc_id` with `title`/`doc_ref` so the prototype does not create a third divergent source. |
| PDF accessibility/tagging | The rendered XeLaTeX baseline reports `Tagged: no`. | Bonus | Inspect Typst's produced structure, links, outlines, copy/paste order, alt text support, and tagging. | Useful tagged output would strengthen the migration case, but lack of tagging does not block the first visual and functional prototype. |

## Proposed prototype metadata boundary

The template should receive presentation-neutral data.
The following fields are supported by observed class behavior or are justified prototype extensions:

| Field | Source/meaning | Validation recommendation |
| --- | --- | --- |
| `title`, `short_title`, `subtitle` | LaTeX title metadata. | Non-empty title; short title defaults to title. |
| `doc_ref` | Document handle. | Non-empty; validate its prefix against `series` when known. |
| `series` | Explicit replacement for implicit/external series mapping. | Accept every key in `bin/bibtools.py`'s `TN_SERIES`; the shared labels agree exactly. |
| `status` | Replaces independent draft/obsolete flags. | Enum: `draft`, `released`, `obsolete`. |
| `date` | Revision date shown on the title page and in running headers. | ISO `YYYY-MM-DD`; this is the sole latest-revision value. |
| `doi`, `repository_url` | Optional external identifiers. | Bare DOI; absolute HTTPS repository URL. |
| `toc`, `list_of_figures`, `list_of_tables` | Front-matter controls. | Booleans with documented defaults. |
| `controlled_document_policy` | Governance text and behavior. | Enum such as `none`, `ccb`, `dm-ccb`, `observatory-ccb`; allow a compatibility default from handle prefix. |
| `changes` | Ordered structured change records. | Require version, date, description, and author/owner. |
| `authors`, `affiliations` | Separate generated author data. | Validate all referenced IDs and preserve list order. |

Before implementation, decide whether the existing Documenteer `metadata.yaml` is extended or whether the prototype file is explicitly generated from it.
A second hand-maintained copy of title, handle, authors, DOI, and repository URL would be a migration regression.

## Author exporter assessment

The most maintainable exporter is a new `typst-yaml` generator in the existing author tooling, backed by the Pydantic models in `bin/authordb.py`:

- `authordb.py` already validates ORCID shape, ROR shape, model fields, author IDs, and email/affiliation consistency.
- `db2authors.py` currently has a separate raw-YAML-to-dataclass path.
  Extending that path alone would miss some of the stronger database validation.
- The exporter must retain each requested database key as `internal_id`; the current resolved `Author` dataclass loses that key.
- It should emit only the referenced, deduplicated affiliations, in stable first-use order, while retaining an ID-keyed mapping in YAML.
- It should preserve collaboration/institutional authors and must not invent a corresponding-author flag.
  Correspondence is document-specific data unless AuthorDB is deliberately extended.
- It should normalize LaTeX-bearing name/address strings carefully.
  Existing `latex2text` is useful, but structured address components should be preferred over the presentation-oriented `example_expanded` field.

Suggested CLI shape, consistent with the current tool, is:

```sh
db2authors.py --mode typst-yaml --authors authors.yaml --output people.yaml
```

The CLI accepts `--authors` and `--output` with backward-compatible defaults, avoiding shell redirection and a fixed current-working-directory input.

## Known direct-mapping gaps

- TeX package and macro compatibility is explicitly out of scope.
  Native Typst constructs should replace document structure, math, figures, tables, lists, and references.
- `lsst_aa.bst` has no direct Typst equivalent.
  The prototype's bundled APA author-year baseline is acceptable for feasibility testing; a custom Rubin/AAS CSL and handle rendering are optional and deferred.
- Requirements and actions are rarely used and are deferred.
  If implemented later, they cross the template/build-tool boundary and should use neutral structured data.
- The title page's absolute TeX placement should be reproduced with robust grids and page regions, not copied coordinate-for-coordinate.
- Exact line breaks, float positions, page count, and pagination are comparison diagnostics, not acceptance requirements.
- The class contains dormant and legacy interfaces.
  Preserving every command would enlarge the prototype while reducing clarity.

## Phase 1 answers to prototype questions

Evidence from the compiled prototype supports these answers:

1. **Title page feasibility:** yes.
   A centered grid plus page layers reproduces the hierarchy without shipout coordinates.
2. **Headers and footers:** yes for the representative draft, released, and obsolete builds.
   Long controlled notices remain a production test case.
3. **Page-number transitions:** Typst should use a clear native front/main transition.
   It does not need to reproduce the LaTeX page sequence or exact reset point as long as the result is understandable.
4. **Existing `.bib` compatibility:** the ten-entry representative fixture compiles without normalization.
   A larger real Rubin corpus is still needed to characterize embedded LaTeX and custom-field failures.
5. **Bibliography style:** Typst 0.15 does not bundle AAS CSL. Bundled APA author-year output is a usable baseline; exact `lsst_aa.bst` output and prominent handle rendering are not required.
6. **Formatting versus build system:** title/page layout, typography, document state, change tables, and captions are formatting.
   Author export, requirements/actions extraction, glossary generation, bibliography normalization, metadata indexing, and reproducible font/resource discovery are build-system concerns.
7. **Largest early risks:** bibliography normalization, metadata ownership, long-author layout, and stable page furniture need evidence.
   Requirements and action extraction are too rarely used to shape the initial prototype.
8. **Fonts:** Open Sans, Inconsolata, and XITS Math establish the current visual baseline, but the prototype may use more convenient similar-looking fonts.
   Reproducibility and Rubin look-and-feel matter more than exact family names.
9. **Accessibility:** the inspected LaTeX PDF is untagged.
   Tagged or otherwise improved Typst output is a desirable bonus and should be measured as a potential migration benefit.
10. **YAML metadata:** direct YAML loading should be demonstrated as a Typst benefit, with one authoritative metadata source rather than copied fields.

## Working prototype

The prototype now demonstrates:

- a YAML-driven title page, metadata model, change record, and author model;
- all series keys declared by `TN_SERIES`, with controlled-series membership recorded in the shared `data/series.yaml`;
- ordered unbreakable author names, shared/multiple affiliations, linked AAS-style ORCID icons, and a corresponding-author marker;
- draft, released, and obsolete state rendering;
- Roman-numbered front matter and Arabic-numbered main matter;
- running headers and footers, a draft watermark, and controlled-series notices;
- native headings, cross-references, equations, figures, multi-page tables, raw/code blocks, footnotes, URL-styled external links, Note and Warning admonitions, appendices, citations, and bibliography;
- ten representative local BibTeX records plus direct loading of all five shared bibliography pools;
- tagged output by default and a successful PDF/UA-1 build when requested; and
- smoke tests for compilation, state validation, metadata mapping, and series parity.

Requirements extraction, meeting actions, glossary generation, compact long author lists, issue tables, and a custom Rubin/AAS CSL style remain deferred.

### Requirements and build

The tested version is Typst 0.15.0.
The template ships its own copies of the Open Sans, Inconsolata, and XITS families in `fonts/`, with their licenses, so local and CI builds use the same families and the subtree is self-contained.
From the repository root, build the example with:

```sh
mkdir -p typst-lsstdoc/output
typst compile \
  --root . \
  --font-path typst-lsstdoc/fonts \
  typst-lsstdoc/examples/prototype.typ \
  typst-lsstdoc/output/prototype.pdf
```

Typst's default PDF is tagged.
The representative example also passes Typst's PDF/UA-1 validation:

```sh
typst compile \
  --root . \
  --font-path typst-lsstdoc/fonts \
  --pdf-standard ua-1 \
  typst-lsstdoc/examples/prototype.typ \
  typst-lsstdoc/output/prototype-pdfua.pdf
```

The alt text in the example is part of that successful PDF/UA-1 build.
This is encouraging evidence, not yet a full accessibility audit.

### Template API

The primary show-rule function is `lsstdoc`.
Required arguments are `title`, `id`, `series`, `date`, `authors`, and `affiliations`; `id` deliberately matches the technote.toml field name for the document handle.
Optional arguments are `short-title`, `subtitle`, `status`, `doi`, `repository-url`, `abstract`, `changes`, `toc`, `bibliography`, `bibliography-style`, and `bibliography-full`.
The template also emits the front matter as a labeled metadata element, so tooling can extract the handle, title, and abstract from the compiled document with `typst eval 'query(<rubin-technote>).first().value' --in <file>`, the Typst counterpart of the annotated abstract structures in Markdown and reStructuredText technotes.
`status` accepts only `draft`, `released`, or `obsolete`.
Bibliographies list only cited entries by default; set `bibliography-full: true` only for the equivalent of `\nocite{*}`.
`bibliography-style` defaults to the bundled APA style and accepts another bundled style name or a CSL file path.

The same module exports `note`, `warning`, `citeds`, and `citedsp` functions.
Notes use a cyan Rubin callout; warnings use an orange callout and automatically prefix custom titles with “Warning.” Both are kept together across page breaks.
The citation helpers display a bibliography key (or alternate text) while adding the entry to the reference list without requiring a custom `handle` field.
Their blue underlined text uses Typst's native citation link to the exact bibliography entry.

External HTTP and HTTPS links are dark blue and underlined in body text and bibliographies.
Internal cross-references and citations retain the ordinary document text styling.

```typst
#import "../src/lsstdoc.typ": citeds, citedsp, lsstdoc, technote-args
#let bibs = (
  read("../../texmf/bibtex/bib/refs.bib", encoding: none),
  read("../../texmf/bibtex/bib/lsst.bib", encoding: none),
)

#show: lsstdoc.with(
  ..technote-args(toml("technote.toml")),
  title: "A Typst Prototype for Rubin Technical Documents",
  abstract: [A short description of this document.],
  bibliography: bibs,
)

= Introduction

Prototype text with a citation @JSSv059i10 and a Rubin document
#citeds("DMTN-001"). A bracketed alternate display is
#citedsp("DMTN-000", display: [technical-note series]).
```

Typst resolves a path string from the module that calls `bibliography`, not from the importing document.
Calling `read(path, encoding: none)` in the document loads bibliography bytes at the caller's location and avoids that boundary.
An array of those byte values lets a document use the repository's shared `refs.bib`, `lsst.bib`, `lsst-dm.bib`, `books.bib`, and `refs_ads.bib` files directly without copying entries locally.

Typst still restricts file reads to the compilation root.
An external document build must choose a `--root` containing the shared bibliography directory or expose that directory through its build environment.
This is a build-system integration requirement, not a requirement to copy individual entries into a document-local `.bib` file.

### Documenteer technote metadata

Typst reads TOML natively, so a document can be driven by the same `technote.toml` file that Documenteer uses for Markdown and reStructuredText technotes.
The `technote-args` function in `src/technote-toml.typ` maps the parsed file onto template arguments:

```typst
#import "../src/lsstdoc.typ": lsstdoc
#import "../src/technote-toml.typ": technote-args

#show: lsstdoc.with(
  ..technote-args(toml("technote.toml")),
  title: "Reusing Documenteer Technote Metadata",
)
```

The document loads the file itself because Typst resolves paths relative to the calling module.
The mapping covers the handle (`id`), series (`series_id`), status (`draft`, `stable`, and `deprecated` map to `draft`, `released`, and `obsolete`), revision date (`date_updated`, falling back to `date_created`), DOI (`doi`), repository URL (`github_url`), the optional `title` override, and the author list with deduplicated affiliations.
URL-prefixed ORCID and ROR identifiers are normalized to the bare form the template expects.
Unknown status states produce a clear error, and `date` and `status` can be passed explicitly to override the mapping.
The title and abstract stay in the document source, matching the Documenteer convention, so `documenteer technote add-author` and `sync-authors` work unchanged: they edit `technote.toml` and the next compile picks the changes up.
`examples/technote.typ` demonstrates the flow against `examples/technote.toml`.

### Author input

Author data comes from `technote.toml`, kept synchronized with the central author database by `documenteer technote add-author` and `sync-authors`, or is passed as explicit `authors` and `affiliations` arguments for documents outside the technote workflow.
An earlier `db2authors.py --mode typst-yaml` exporter that generated a separate authors YAML file was retired once it became clear that the Documenteer/ook route covers author management wholesale; the Author exporter assessment above is retained as the audit record of that dead end.

### Tests

Run the smoke suite from the repository root:

```sh
python3 -m unittest discover -s typst-lsstdoc/tests -v
```

The test compiles the full example as PDF/UA-1, compiles draft/released/obsolete state fixtures, verifies the invalid-state diagnostic, checks the technote.toml mapping and controlled-series data, and compares `data/series.yaml` exactly with `bibtools.py`.

## Current findings

1. The title page and page furniture can be reproduced with ordinary grids and page regions; fragile absolute placement is not needed.
2. Native YAML works well for document and author metadata, and the Documenteer `technote.toml` adapter resolves the metadata-ownership question without introducing another hand-maintained source.
3. The tested local fixture and all five shared bibliography pools parse without normalization; the example cites entries directly from `refs.bib` and `lsst.bib`.
   Typst 0.15 does not bundle an AAS CSL style, so the prototype uses its bundled APA author-year style.
   A Rubin/AAS CSL file is optional follow-up work rather than a blocker.
4. Typst's ordinary tagged PDF and PDF/UA-1 mode are both viable for this representative document.
   A production assessment still needs screen-reader, reading-order, table semantics, and link-purpose review.
5. Front/main numbering transitions cleanly.
   Exact LaTeX page-sequence parity is neither necessary nor desirable.
6. The template makes table figures breakable with repeated headers, so a single captioned figure can span pages and cross-references target the real table.
7. The next useful evidence is a real Rubin `.bib` compatibility corpus, a long AuthorDB-generated author list, CI integration, and a side-by-side visual comparison against a representative LaTeX technical note.

## Technote workflow design

This is the agreed plan for making Typst technotes first-class citizens of the Markdown/reStructuredText technote workflow.
Every mechanism named here was verified against the Documenteer source, the `templates` package, and a representative deployed technote.

The published product is a PDF uploaded to lsst.io, following the LaTeX technote model, with the metadata boundary kept clean enough that Typst HTML export can be added later without changing the repository contract.

The template is developed in this directory and consumed by documents as the Typst package `rubin-technote`.
This subtree is self-contained: sources, series data, artwork, and fonts (with their licenses) all live inside it, and the test suite compiles the technote example with the project root and font path confined to the subtree, both directly and through a vendored `@preview/rubin-technote` package layout.
While the template incubates here, a technote's Makefile fetches this subtree (about 5 MB, not a full repository clone) into a vendored package directory and compiles with `--package-path`, so documents use the permanent `#import "@preview/rubin-technote:..."` line from the start.
When the template graduates to its own repository and is published to Typst Universe, only the fetch step is deleted; no technote source changes.
Fonts ride inside the fetched package during incubation, which sidesteps the limitation that Typst Universe packages cannot register fonts; after Universe publication a small font-provisioning step remains in the Makefile.

A Typst technote repository is as thin as a Markdown one: `technote.toml`, `index.typ`, `local.bib`, a Makefile, and CI configuration.
`index.typ` spreads `technote-args(toml("technote.toml"))` into `lsstdoc` and keeps the title and abstract in the document source.

The Makefile mirrors the Markdown technote targets.
`make add-author` and `make sync-authors` are unchanged: they run `documenteer technote add-author`/`sync-authors`, which resolve authors through the ook API at `roundtable.lsst.cloud` and write `technote.toml`, and the next compile picks the changes up.
A new `make sync-bibs` target materializes the five shared bibliography files into a git-ignored directory for the document to `read()`, using the same per-file GitHub raw download that Documenteer's `githubbibcache` extension performs for Sphinx builds.
The natural home for that logic is a new `documenteer technote sync-bibs` subcommand, since the download and cache code already exists in Documenteer; a plain download loop in the Makefile is the interim fallback.
`make pdf` runs `typst compile`.

Scaffolding is a new `technote_typst` project template in the `templates` repository alongside `technote_md`; templatekit metadata means the Slack bot needs no changes.
Continuous integration follows the shared-workflow pattern of `rubin-sphinx-technote-workflows`: fetch the template (cacheable), sync the bibliographies, compile, and upload the PDF with a landing page to LSST the Docs.

While the template lives in this repository, the existing tests guard series-label parity with `bibtools.py`.
After the split, the template repository's CI fetches `bibtools.py` from GitHub raw, the same pattern used for the bibliographies, to keep that guard.
