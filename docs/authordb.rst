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
  in the **lsst/lsst‑texmf** repository.
* ``bin/makeAuthorListsFromGoogle.py`` — helper to pull sign‑ups from a Google Sheet
  and prepare YAMLs for review.
* ``bin/db2authors.py`` — utilities to assemble author lists during builds and
  to help merge curated updates.

Why this matters
================

Technotes and other Rubin documents obtain *consistent* author identity data
from ``authordb.yaml``. Document tooling (Documenteer) resolves author
identifiers in project docs to the canonical entries in this database.

I am not in the AuthorDB
========================
`This convenient sheet <https://docs.google.com/spreadsheets/d/1_zXLp7GaIJnzihKsyEAz298_xdbrgxRgZ1_86kwhGPY/edit?gid=0#gid=0>`_
lets you search easily for your name in the Author DB.
Your author id is in the left column.

If you are not in the list sign up using  the google form
which is bookmarked in Slack `#all-users <https://rubin-obs.slack.com/archives/C02SVMGUC>`_.
It will take at least 24 hours to process via the github nightly action.

I want a paper signup sheet
===========================
If you want an author acknowledgement/signup sheet `copy this google form <https://docs.google.com/forms/d/1bTj04U2Np4w3hF96jvrGzxlJMDfV2gtMj-b2Rnhu17c/edit>`_.
You can collect any information you wish as long as one field is the AuthorID.
We suggest you take the description pointing authors at the signup form if they do not yet have a Rubin AuthorID.

Have the form put results in a google sheet.
Check which column contains the AuthorID and use that in the call to the script.
0 is the first column so column E is 4 for example  which is the default.
The parameter after signup in the call allows you specify a different column.

Then you may use:

  $ bin/makeAuthorListsFromGoogle.py --signup 4 -p --sheet SHEET_ID "FormResponses!A1:Z"

The SHEET_ID is the long string before ? in your google sheet it looks like

   1CGxjpPuyNJ_gXRHTvkEF0qeI0XedQ-GQgbmyzWFLSUE

The string after that gives the sheet(tab) and range to access.

When you run this script you need a client file in your directory client_secret.json.
You can ask wil for one or follow the instructions below to create one.

Google Sheets Access: client_secret.json
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This project reads data directly from a Google Sheet using the
`Google Sheets API <https://developers.google.com/sheets/api>`_.

Because the API requires authentication, **each user must create their own
OAuth client secrets file** called ``client_secret.json``. This file is used
to perform the one-time sign-in that grants the script access to your
Google account.

.. important::

   Do **not** commit ``client_secret.json`` or ``token.pickle`` to Git.
   Both files are personal credentials and should be listed in ``.gitignore``.

Step-by-step setup
^^^^^^^^^^^^^^^^^^

1. Go to the `Google Cloud Console <https://console.cloud.google.com/>`_.

2. If you don’t already have a project:

   * Click the project drop-down → **New Project**.
   * Give it a name (for example, ``Rubin Authors``), and create it.

3. Enable the **Google Sheets API** for your project:

   * From the left menu, go to **APIs & Services → Library**.
   * Search for "Google Sheets API" and click **Enable**.

4. Create OAuth client credentials:

   * From the left menu, go to **APIs & Services → Credentials**.
   * Click **Create credentials → OAuth client ID**.
   * For **Application type**, choose **Desktop app**.
   * Give it a name (for example, ``Rubin Authors Desktop``), then click **Create**.

5. Download the client secrets file:

   * After creation, you will see your new OAuth client in the list.
   * Click the download icon (⭳) to get a JSON file.
   * Rename it to ``client_secret.json``.

6. Place ``client_secret.json`` in the root of this repository
   (next to the scripts that use it).

First run
^^^^^^^^^

When you run a script that accesses the Google Sheet, it will:

* Detect ``client_secret.json`` and launch a browser window for you to sign in.
* Ask you to allow access to your Google account for reading Sheets.
* Save a local token cache in ``token.pickle`` so you won’t need to log in again.

Both ``client_secret.json`` and ``token.pickle`` are ignored by ``.gitignore``.


Overview of components
======================

``authordb.yaml``
-----------------
A single YAML file that stores:

* **Authors**: keyed by a stable *author ID* (usually ``surname`` + initials,
  lowercase). Each entry carries canonical names and identifiers.
  Upper case author IDs are reserved for "collaboration" authors.

* **Affiliations**: keyed by short IDs (e.g., ``RubinObsC``), including the
  public institute name, a postal address, and (optionally) the email domain
  used to shorthand author emails.

Documenteer and downstream tools read this file to render author lists,
affiliations, and metadata consistently across documents.

Typical author entry (illustrative)::

  authors:
    jdoe:
      given_name: John
      family_name: Doe
      orcid: 0000-0000-0000-0000
      email: jdoe@RubinObsC        # “local@AffilID” shorthand - we try to not store full emails
      affil: [RubinObsC]           # primary affiliations (IDs), specify more than one as needed
      altaffil: []                 # Authors often have additional information that needs to be noted
                                   # (e.g. Hubble Fellow, author is deceased, etc.) in addition to their
                                   # affiliation information.
                                   # Do not put actual affiliation here







Typical affiliation entry (illustrative)::

  affiliations:
    RubinObsC:
      institute: Vera C. Rubin Observatory (Chile)
      address:
        example_expanded: Vera C. Rubin Observatory, Cerro Pachón, Chile
        street: Cerro Pachón
        city: Vicu\~na
        postcode: ""
        country_code: CL
      email: rubinobservatory.org   # optional domain for email shorthands

.. tip::

   The “email shorthand” convention lets an author’s email be stored as either
   ``local`` (when the primary affiliation’s domain applies) or
   ``local@AffilID`` when the domain belongs to a *different* affiliation.
   During rendering, the domain is substituted from the affiliation record.
   We discourage the use of full email addressed in this file as it is public.


``makeAuthorListsFromGoogle.py``
--------------------------------
A script that connects to a Google Sheet where contributors submit sign‑ups.
It selects relevant columns (author ID, names, affiliations, ORCID, email),
derives normalized author IDs, and emits small YAML files for review (for
example, a set of *new authors* and *new affiliations* to be merged into
``authordb.yaml``).

Google API access is required (OAuth client, token cache); see Google’s Python
Sheets quickstart for one‑time setup. The ``lsst-texmf`` docs also describe
running helper scripts (including this one) inside the project Docker image.


``db2authors.py``
-----------------
A companion utility used in build pipelines to turn the curated database into
LaTeX author/affiliation blocks and/or to help merge reviewed YAML deltas back
into the database. It is commonly available in the project Docker image used
by document builds.
The main use of this is to read an authors.yaml file containing authorids and
turn that into appropriate latex for a given publication.

You can maintain an authors.yaml file directly but for publications where
authors need to actively sign up you will need a sign up form.

End‑to‑end workflow for sign up form
=====================================

1. **Collect sign‑ups**
   Maintain a Google Form + Sheet with the columns your team uses but
   at least AuthorID

2. **Fetch and stage updates**
   Run ``makeAuthorListsFromGoogle.py`` to read the Sheet ranges you care about
   and produce authors.yaml for your publication.

   * ``authors.yaml`` — is a flat list of normalized author IDs (useful for
     order management and “builders” lists).

3. **Consume in documents**
   Document builds pick up ``authordb.yaml`` (directly or via the Docker image)
   so author lists appear consistent across technotes and other series.
   Usually with:

   	db2authors.py -m aas7 > authors.tex

Supported db2authors output modes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``db2authors.py`` can generate author lists in several formats, depending on
the target document class or publication. Select the mode appropriate for your
build:

- ``aas``
  Generate an author list formatted for *AAS Journals* (ApJ, AJ, ApJS, ApJL).
  Uses the AAS LaTeX macros for authors and affiliations.

- ``aas7``
  Support for the newer *AAS v7* style. Similar to ``aas`` but
  has a few new things.

- ``spie``
  Author list formatted for *SPIE conference proceedings* style.

- ``adass``
  Author list formatted for *ADASS conference proceedings* style.

- ``arxiv``
  A simplified text author block suitable for *arXiv* preprints.

- ``ascom``
  Output formatted for *Astronomy and Computing* (Elsevier).

- ``webofc``
  Output formatted for *Web of Conferences* proceedings style.

- ``lsstdoc``
  Native format used by Rubin’s ``lsstdoc`` LaTeX class, for technotes and
  other Rubin project documents.

- ``csvall``
  Dump all authors into a simple CSV file (one row per author, with metadata).

- ``mnras``
  Author list formatted for *Monthly Notices of the Royal Astronomical Society*
  (MNRAS).

- ``aap``
  Author list formatted for *Astronomy & Astrophysics* (A&A).


Command‑line usage (patterns)
=============================

The exact options vary by revision; consult ``-h``. The following patterns are
commonly used in Rubin pipelines:

Pull sign‑ups from Google and stage YAMLs::

  $ bin/makeAuthorListsFromGoogle.py --signup -p --sheet SHEET_ID "FormResponses!A1:Z"

Pull new authors from AuthorDB new/update Google form and stage YAMLs::

  $ bin/makeAuthorListsFromGoogle.py -skip `cat skip` --adb -p --sheet SHEET_ID "FormResponses!A1:Z"

Merge reviewed authors into the database (this will update authordb.yaml - you need to PR it)::

  $ bin/db2authors.py -m new_authors.yaml

Merge reviewed affiliations (this will update authordb.yaml - you need to PR it)::

  $ bin/db2authors.py -a new_affiliations.yaml

Build‑time author list generation (driven by your doc’s Makefile) typically
invokes ``db2authors.py`` inside the standard Docker image.


Data model details
==================

Author entries (canonical)
--------------------------

* ``given_name``: string with LaTeX‑safe accents/macros.
* ``family_name``: string with LaTeX‑safe accents/macros.
* ``orcid``: 16‑digit ORCID iD, 4 groups of 4 numbers separated  by``-`` chars (optional).
* ``email``: either ``local`` (uses primary affiliation’s domain) **or**
  ``local@AffilID`` (explicit cross‑affiliation domain).
* ``affil``: list of affiliation IDs (primary first).
* ``altaffil``: additional information that needs to be noted (e.g. Hubble Fellow, author is deceased, etc.). NOT actual affiliation. (optional)/


Affiliation entries
-------------------

* ``institute``: public institute name (LaTeX‑safe).
* ``address``: structured address with fields such as ``street``, ``city``,
  ``postcode``, and ``country_code``; may also include an
  ``example_expanded`` string for human‑readable display.
* ``email``: optional domain used for email shorthand resolution.

These conventions align with how technote metadata is resolved from the
database.


Operational tips
================

* **Keep IDs stable.** Renaming an author ID propagates churn across many
  documents; prefer adding aliases only when absolutely necessary.

* **Normalize sign‑up data.** Derive IDs as ``surname`` + initials, lowercase,
  and strip accents/LaTeX from the ID itself. (Store the *display* names with
  proper accents/macros.)

* **Email shorthand.** If an email domain is unique to an affiliation, prefer
  ``local`` for authors whose primary affiliation carries that domain; otherwise
  use ``local@AffilID``.

* **Review new affiliations carefully.** The postal address and public
  institute name are used in rendered front‑matter; get them right before
  merging.


