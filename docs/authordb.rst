.. _authordb:

#################################
Rubin Author Database and scripts
#################################

All Rubin authors should be in the Author Database.
From this source we can generate author tex for various publications.

This page explains how Rubin’s author database is curated and how the
Google‑Form → YAML workflow is used to create and maintain author lists in
``lsst-texmf``. It is based on:

* ``etc/authordb.yaml`` — the canonical author + affiliation registry
  in the **lsst/lsst‑texmf** repository. :contentReference[oaicite:0]{index=0}
* ``bin/makeAuthorListsFromGoogle.py`` — helper to pull sign‑ups from a Google Sheet
  and prepare YAMLs for review. :contentReference[oaicite:1]{index=1}
* ``bin/db2authors.py`` — utilities to assemble author lists during builds and
  to help merge curated updates. :contentReference[oaicite:2]{index=2}

Why this matters
================

Technotes and other Rubin documents obtain *consistent* author identity data
from ``authordb.yaml``. Document tooling (Documenteer) resolves author
identifiers in project docs to the canonical entries in this database. :contentReference[oaicite:3]{index=3}

I am not in the AuthorDB
========================
`This convenient sheet <https://docs.google.com/spreadsheets/d/1_zXLp7GaIJnzihKsyEAz298_xdbrgxRgZ1_86kwhGPY/edit?gid=0#gid=0>`_
lets you search easiy for your name in the Author DB.
Your author id is int he left column.

If you are not in the list sign up using `this google form <https://forms.gle/KerayScYggLf2od3A>`_.
It will take 24 hours to process.


Overview of components
======================

``authordb.yaml``
-----------------
A single YAML file that stores:

* **Authors**: keyed by a stable *author ID* (usually ``surname`` + initials,
  lowercase). Each entry carries canonical names and identifiers.
* **Affiliations**: keyed by short IDs (e.g., ``RubinObsC``), including the
  public institute name, a postal address, and (optionally) the email domain
  used to shorthand author emails.

Documenteer and downstream tools read this file to render author lists,
affiliations, and metadata consistently across documents. :contentReference[oaicite:4]{index=4}

Typical author entry (illustrative)::

  authors:
    jdoe:
      given_name: John
      family_name: Doe
      orcid: 0000-0000-0000-0000
      email: jdoe@RubinObsC        # “local@affilid” shorthand
      affil: [RubinObsC]           # primary affiliations (IDs)
      altaffil: []                 # optional additional affiliations

Typical affiliation entry (illustrative)::

  affiliations:
    RubinObsC:
      institute: Vera C. Rubin Observatory (Chile)
      address:
        example_expanded: Vera C. Rubin Observatory, Cerro Pachón, Chile
        street: Cerro Pachón
        city: Vicuña
        postcode: ""
        country_code: CL
      email: rubinobservatory.org   # optional domain for email shorthands

.. tip::

   The “email shorthand” convention lets an author’s email be stored as either
   ``local`` (when the primary affiliation’s domain applies) or
   ``local@affilid`` when the domain belongs to a *different* affiliation.
   During rendering, the domain is substituted from the affiliation record.


``makeAuthorListsFromGoogle.py``
--------------------------------
A script that connects to a Google Sheet where contributors submit sign‑ups.
It selects relevant columns (author ID, names, affiliations, ORCID, email),
derives normalized author IDs, and emits small YAML files for review (for
example, a set of *new authors* and *new affiliations* to be merged into
``authordb.yaml``). :contentReference[oaicite:5]{index=5}

Google API access is required (OAuth client, token cache); see Google’s Python
Sheets quickstart for one‑time setup. The ``lsst-texmf`` docs also describe
running helper scripts (including this one) inside the project Docker image. :contentReference[oaicite:6]{index=6}


``db2authors.py``
-----------------
A companion utility used in build pipelines to turn the curated database into
LaTeX author/affiliation blocks and/or to help merge reviewed YAML deltas back
into the database. It is commonly available in the project Docker image used
by document builds. :contentReference[oaicite:7]{index=7}


End‑to‑end workflow
===================

1. **Collect sign‑ups**
   Maintain a Google Form + Sheet with the columns your team uses (author ID,
   surname, given names, primary affiliation ID(s), ORCID, email, etc.).

2. **Fetch and stage updates**
   Run ``makeAuthorListsFromGoogle.py`` to read the Sheet ranges you care about
   and produce small YAMLs for review, such as:

   * ``authors.yaml`` — a flat list of normalized author IDs (useful for
     order management and “builders” lists).
   * ``new_authors.yaml`` — mapping of *only* new or changed authors.
   * ``new_affiliations.yaml`` — mapping of *only* new or changed affiliations.

   You then review/edit these YAMLs, commit them to a PR, or hand them to the
   database maintainer for merging. :contentReference[oaicite:8]{index=8}

3. **Curate and merge**
   Use helper scripts (for example, functions in ``db2authors.py``) to validate
   the staged YAMLs and merge them into ``etc/authordb.yaml`` when approved.
   Keep IDs stable; fix typos or ORCID changes at the source (the database)
   rather than in individual documents. :contentReference[oaicite:9]{index=9}

4. **Consume in documents**
   Document builds pick up ``authordb.yaml`` (directly or via the Docker image)
   so author lists appear consistent across technotes and other series. :contentReference[oaicite:10]{index=10}


Command‑line usage (patterns)
=============================

The exact options vary by revision; consult ``-h``. The following patterns are
commonly used in Rubin pipelines: :contentReference[oaicite:11]{index=11}

Pull sign‑ups from Google and stage YAMLs::

  $ bin/makeAuthorListsFromGoogle.py -p --sheet SHEET_ID "FormResponses!A1:Z"

Merge reviewed authors into the database::

  $ bin/db2authors.py --merge-authors new_authors.yaml

Merge reviewed affiliations::

  $ bin/db2authors.py --merge-affiliations new_affiliations.yaml

Build‑time author list generation (driven by your doc’s Makefile) typically
invokes ``db2authors.py`` inside the standard Docker image. :contentReference[oaicite:12]{index=12}


Data model details
==================

Author entries (canonical)
--------------------------

* ``given_name``: string with LaTeX‑safe accents/macros.
* ``family_name``: string with LaTeX‑safe accents/macros.
* ``orcid``: 16‑digit ORCID iD (optional).
* ``email``: either ``local`` (uses primary affiliation’s domain) **or**
  ``local@affilid`` (explicit cross‑affiliation domain).
* ``affil``: list of affiliation IDs (primary first).
* ``altaffil``: list of additional affiliation IDs (optional).

Affiliation entries
-------------------

* ``institute``: public institute name (LaTeX‑safe).
* ``address``: structured address with fields such as ``street``, ``city``,
  ``postcode``, and ``country_code``; may also include an
  ``example_expanded`` string for human‑readable display.
* ``email``: optional domain used for email shorthand resolution.

These conventions align with how technote metadata is resolved from the
database. :contentReference[oaicite:13]{index=13}


Operational tips
================

* **Keep IDs stable.** Renaming an author ID propagates churn across many
  documents; prefer adding aliases only when absolutely necessary.

* **Normalize sign‑up data.** Derive IDs as ``surname`` + initials, lowercase,
  and strip accents/LaTeX from the ID itself. (Store the *display* names with
  proper accents/macros.)

* **Email shorthand.** If an email domain is unique to an affiliation, prefer
  ``local`` for authors whose primary affiliation carries that domain; otherwise
  use ``local@affilid``.

* **Review new affiliations carefully.** The postal address and public
  institute name are used in rendered front‑matter; get them right before
  merging.


Troubleshooting
===============

* **Document build can’t find authors.** Ensure the document build environment
  (often a Docker image) is using a version of ``lsst-texmf`` that includes
  your updated ``authordb.yaml``. :contentReference[oaicite:14]{index=14}

* **Inconsistent names across docs.** Update the canonical entry in
  ``authordb.yaml`` rather than patching per‑document metadata; Documenteer
  pulls the canonical record at render time. :contentReference[oaicite:15]{index=15}

* **Google API authentication.** For first‑time runs of the Google importer,
  complete the OAuth flow and preserve the token cache as instructed by the
  Google Sheets API quickstart; subsequent runs are non‑interactive.


References
==========

* lsst‑texmf documentation home. :contentReference[oaicite:16]{index=16}
* How technotes resolve authors from ``authordb.yaml`` (Documenteer docs). :contentReference[oaicite:17]{index=17}
* Docker usage notes (scripts available in the image). :contentReference[oaicite:18]{index=18}
* Background discussions and usage in Rubin community posts. :contentReference[oaicite:19]{index=19}


