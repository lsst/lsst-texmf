#!/usr/bin/env python3

"""Migrate local.bib contents to lsst-texmf bib files.

* Reads local.bib file.
* Confirms that all ADS entries use bibcode as bibkey.
* Migrates ADS entries to refs_ads.bib and remaining entries to refs.bib.

Assumes it is being run from the tech note directory containing a local.bib
with a lsst-texmf submodule.
"""

import sys

from bibtools import get_ads_bibcode
from pybtex.database import BibliographyData


def validate_bibkeys(bibdata: BibliographyData) -> tuple[set[str], set[str]]:
    """Validate that all ADS entries use the bibcode as the bibkey.

    Returns set of bibkeys that are ADS bibcodes and set of bibkeys that are
    not.
    """
    ads_bibkeys = set()
    non_ads_bibkeys = set()
    for bibkey, entry in bibdata.entries.items():
        if bibcode := get_ads_bibcode(entry):
            if entry.key != bibcode:
                print(
                    f"Entry {bibkey} has a ADS bibcode {bibcode} but does not use it as bibkey.",
                    file=sys.stderr,
                )
                sys.exit(1)
            ads_bibkeys.add(bibkey)
        else:
            non_ads_bibkeys.add(bibkey)
    return ads_bibkeys, non_ads_bibkeys


if __name__ == "__main__":
    with open("local.bib") as fd:
        bibdata = BibliographyData.from_string(fd.read(), "bibtex")

    ads_bibkeys, non_ads_bibkeys = validate_bibkeys(bibdata)

    ads_entries = BibliographyData(entries={k: bibdata.entries[k] for k in ads_bibkeys})
    non_ads_entries = BibliographyData(entries={k: bibdata.entries[k] for k in non_ads_bibkeys})

    # Add ADS entries to refs_ads.bib
    if ads_bibkeys:
        with open("lsst-texmf/texmf/bibtex/bib/refs_ads.bib", "a") as fd:
            fd.write("\n" + ads_entries.to_string("bibtex") + "\n")

    # Add non-ADS entries to refs.bib
    if non_ads_bibkeys:
        with open("lsst-texmf/texmf/bibtex/bib/refs.bib", "a") as fd:
            fd.write("\n" + non_ads_entries.to_string("bibtex") + "\n")

    # Now zero the local.bib file to remove the entries that were migrated.
    with open("local.bib", "w") as fd:
        fd.write("")
