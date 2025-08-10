#!/usr/bin/env python3

"""Read a local.bib file and rewrite it to use ADS bibcodes as the bib keys.

This allows those bib keys to be seemlessly used in the lsst-texmf bibtex
archive and shared with all tech notes.

First argument is the bib file to read and remaining arguments are tex files
to rewrite with the new bib keys.
"""

import argparse
import re
import sys

from bibtools import get_ads_bibcode
from pybtex.database import BibliographyData


def process_bib(bibdata: BibliographyData) -> dict[str, str]:
    """Read the bib data and return a mapping of bib key to bibcode."""
    bibcode_map: dict[str, str] = {}
    for bibkey, entry in bibdata.entries.items():
        if bibcode := get_ads_bibcode(entry):
            bibcode_map[bibkey] = bibcode
    return bibcode_map


if __name__ == "__main__":
    description = __doc__
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)

    parser.add_argument("bibfile", help="Name of file bib file to read", nargs="?")
    parser.add_argument("texfiles", help="Name of tex files to rewrite", nargs="*")

    args = parser.parse_args()

    with open(args.bibfile) as fd:
        bibfile_content = fd.read()
        local_bib = BibliographyData.from_string(bibfile_content, "bibtex")

    # Map old bib keys to new bibcodes.
    bibkey_map = process_bib(local_bib)

    # Create a regex that matches any of the keys
    pattern = re.compile(r"\{(" + "|".join(re.escape(k) for k in bibkey_map) + r")\}")
    print(pattern)

    def cite_replacer(match: re.Match) -> str:  # noqa: D103
        return "{" + bibkey_map[match.group(1)] + "}"

    # Process each tex file and replace the bib keys.
    for texfile in args.texfiles:
        with open(texfile) as fd:
            text = fd.read()

        # Replace the bib keys in the text.
        new_text = pattern.sub(cite_replacer, text)

        # Write the modified text back to the file.
        with open(texfile, "w") as fd:
            fd.write(new_text)
        print(f"Updated {texfile} with new bib keys.", file=sys.stderr)

    # Now update the local.bib file with the new bibcodes but do it without
    # using pybtex to avoid confusingly large diffs.
    pattern = re.compile(r"\{(" + "|".join(re.escape(k) for k in bibkey_map) + "),")

    def bibcode_replacer(match: re.Match) -> str:  # noqa: D103
        return "{" + bibkey_map[match.group(1)] + ","

    new_bibdata = pattern.sub(bibcode_replacer, bibfile_content)
    with open(args.bibfile, "w") as fd:
        fd.write(new_bibdata)
