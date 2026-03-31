#!/usr/bin/env python3

r"""Extract citations from LaTeX documents and build a local bibliography.

* Reads a LaTeX document(s).
* Finds all citation commands (\cite, \citet, \citep, etc.).
* Extracts cited bibkeys.
* Pulls matching entries from central bibfiles to a local bib file.
* It does not modify the bibliograpy in the original file(s)
* Modify the original file yourslef with SED or such

"""

import argparse
import os
import re
import sys
from pathlib import Path

from pybtex.database import BibliographyData


def extract_citations_from_latex(latex_file: str | Path) -> set[str]:
    r"""Extract all citation bibkeys from a LaTeX file.

    Searches for citation commands: \cite, \citet, \citep, \citealp, etc.

    Parameters
    ----------
    latex_file : str or Path
        Path to the LaTeX file to search.

    Returns
    -------
    citations : set[str]
        Set of unique bibkeys found in citation commands.
    """
    citations = set()
    citation_pattern = r"\\cite[a-z]*\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}"

    try:
        with open(latex_file, encoding="utf-8") as fd:
            content = fd.read()
    except FileNotFoundError:
        print(f"Error: LaTeX file '{latex_file}' not found.", file=sys.stderr)
        sys.exit(1)

    matches = re.findall(citation_pattern, content)
    for match in matches:
        # Handle multiple citations separated by commas
        bibkeys = [key.strip() for key in match.split(",")]
        citations.update(bibkeys)

    return citations


def load_bibfiles(bibfile_paths: list[str | Path]) -> BibliographyData:
    """Load bibliography data from central bibfiles.

    Parameters
    ----------
    bibfile_paths : list[str or Path]
        Paths to bibfiles to load.

    Returns
    -------
    bibdata : BibliographyData
        Combined bibliography data from all files.
    """
    combined_bibdata = BibliographyData()

    for bibfile in bibfile_paths:
        try:
            with open(bibfile, encoding="utf-8") as fd:
                bibdata = BibliographyData.from_string(fd.read(), "bibtex")
                combined_bibdata.entries.update(bibdata.entries)
                print(f"Loaded {len(bibdata.entries)} entries from {bibfile}")
        except FileNotFoundError:
            print(f"Warning: Bibfile '{bibfile}' not found.", file=sys.stderr)
        except Exception as e:
            print(
                f"Warning: Failed to parse '{bibfile}': {e}",
                file=sys.stderr,
            )

    return combined_bibdata


def extract_cited_entries(
    citations: set[str], bibdata: BibliographyData
) -> tuple[BibliographyData, set[str]]:
    """Extract bibliography entries for cited bibkeys.

    Parameters
    ----------
    citations : set[str]
        Set of bibkeys to extract.
    bibdata : BibliographyData
        Complete bibliography data to extract from.

    Returns
    -------
    cited_entries : BibliographyData
        Bibliography data containing only cited entries.
    missing : set[str]
        Set of bibkeys not found in the bibliography.
    """
    cited_entries = BibliographyData()
    missing = set()

    for bibkey in citations:
        if bibkey in bibdata.entries:
            cited_entries.entries[bibkey] = bibdata.entries[bibkey]
        else:
            missing.add(bibkey)

    return cited_entries, missing


def unescape_bibtex_output(bibtex_str: str) -> str:
    r"""Unescape double backslashes in BibTeX output.

    Fixes the issue where pybtex escapes backslashes, turning \\_ into \\_.

    Parameters
    ----------
    bibtex_str : str
        The BibTeX string output from pybtex.

    Returns
    -------
    unescaped : str
        The unescaped BibTeX string.
    """
    # Replace double backslashes followed by special characters with single
    # This handles cases like \\_ -> \_
    bibtex_str = re.sub(r"\\\\([_{}~^])", r"\\\1", bibtex_str)
    return bibtex_str


if __name__ == "__main__":
    # Get default bibfile paths from $TEXMFHOME
    texmfhome = os.environ.get("TEXMFHOME", os.path.expanduser("~/.texmf"))
    default_bibfiles = [
        os.path.join(texmfhome, "bibtex/bib/lsst.bib"),
        os.path.join(texmfhome, "bibtex/bib/lsst-dm.bib"),
        os.path.join(texmfhome, "bibtex/bib/refs_ads.bib"),
        os.path.join(texmfhome, "bibtex/bib/refs.bib"),
        os.path.join(texmfhome, "bibtex/bib/ivoa.bib"),
        os.path.join(texmfhome, "bibtex/bib/books.bib"),
    ]

    parser = argparse.ArgumentParser(
        description="Extract citations from LaTeX documents and build a local bibliography."
    )
    parser.add_argument(
        "latex_files",
        nargs="+",
        help="LaTeX file(s) to search for citations",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="allcitations.bib",
        metavar="FILE",
        help="Output bibfile name (default: allcitations.bib)",
    )
    parser.add_argument(
        "-b",
        "--bibfiles",
        nargs="+",
        default=default_bibfiles,
        metavar="FILE",
        help=" bibfile(s) to search (default: most of $TEXMFHOME/bibtex/bib/)",
    )

    args = parser.parse_args()

    # Extract citations from all LaTeX files
    all_citations = set()
    for latex_file in args.latex_files:
        citations = extract_citations_from_latex(latex_file)
        all_citations.update(citations)
        print(f"Found {len(citations)} citations in {latex_file}")

    print(f"\nTotal unique citations: {len(all_citations)}")

    # Load central bibfiles
    print(f"\nLoading bibfiles: {', '.join(args.bibfiles)}")
    bibdata = load_bibfiles(args.bibfiles)
    print(f"Total entries in central bibfiles: {len(bibdata.entries)}")

    # Extract cited entries
    cited_entries, missing = extract_cited_entries(all_citations, bibdata)

    # Report results
    print(f"\nExtracted {len(cited_entries.entries)} entries to {args.output}")
    if missing:
        print(f"Warning: {len(missing)} citations not found in bibfiles:")
        for bibkey in sorted(missing):
            print(f"  - {bibkey}")

    # Write to output file
    with open(args.output, "w") as fd:
        bibtex_output = cited_entries.to_string("bibtex")
        bibtex_output = unescape_bibtex_output(bibtex_output)
        fd.write(bibtex_output)

    sys.exit(0 if not missing else 1)
