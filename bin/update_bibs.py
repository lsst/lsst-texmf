#!python

"""
Update bibtex entries from ADS.

ADS entries evolve over time, such as arXiv entries being published
or DOIs being added later.

This command reads an existing bib file, determines all the ADS bib
entries, and re-requests them from ADS.
"""

import argparse
import json
import re
import sys

import requests
from bibtools import get_ads_bibcode
from pybtex.database import BibliographyData


def process_bib(bibdata: BibliographyData, token: str) -> BibliographyData:
    """Scan through the bibliography data and update ADS entries whilst
    retaining the bibkey.
    """
    # It is possible that the bibkey is not the ADS bibcode, so we need to
    # map the bib key to bibcode.
    to_update: dict[str, str] = {}
    non_ads = set()
    for bibkey, entry in bibdata.entries.items():
        if bibcode := get_ads_bibcode(entry):
            to_update[str(bibkey)] = bibcode
        elif adsurl := entry.fields.get("adsurl"):
            print("Failed to extract bibcode from ", adsurl, file=sys.stderr)
        else:
            non_ads.add(bibkey)

    print(f"Found {len(to_update)} ADS entries out of {len(bibdata.entries)}.", file=sys.stderr)

    if non_ads:
        print("The following bibkeys are not ADS entries:", file=sys.stderr)
        for bibkey in sorted(non_ads):
            print(f"- {bibkey}", file=sys.stderr)

    if not token:
        if to_update:
            print("Would have searched for the following bibcodes:", file=sys.stderr)
            for bibcode in to_update.values():
                print(f"- {bibcode}", file=sys.stderr)

        print("No token provided. Not querying ADS.", file=sys.stderr)
        return bibdata

    baseurl = "https://api.adsabs.harvard.edu/v1/export/bibtex"
    payload = {"bibcode": list(to_update.values())}

    results = requests.post(
        baseurl,
        headers={"Authorization": "Bearer " + token},
        data=json.dumps(payload),
    )
    results.raise_for_status()

    data = results.json()
    print(data["msg"], file=sys.stderr)

    # ADS return all the bib entries as a single string.
    updated_bibdata = BibliographyData.from_string(data["export"], "bibtex")
    retrieved = set(updated_bibdata.entries.keys())

    # Now re-attach these to the original.
    missed: set[str] = set()
    handled: set[str] = set()
    for bibkey, bibcode in to_update.items():
        print(f"Replacing bibkey {bibkey} with data from {bibcode} ...", end="", file=sys.stderr)
        if updated := updated_bibdata.entries.get(bibcode):
            updated.key = bibkey  # Consistency.
            bibdata.entries[bibkey] = updated
            print("updated", file=sys.stderr)
            # A single bibcode may be used multiple times with different
            # bibkeys, so we need to track that.
            handled.add(bibcode)
        else:
            print("not found", file=sys.stderr)
            missed.add(bibcode)

    if unhandled := (retrieved - handled):
        print("The following bibcodes were retrieved but not associated:", file=sys.stderr)
        for bibcode in sorted(unhandled):
            print(f"- {bibcode}", file=sys.stderr)
    if missed:
        print("The following bibcodes were requested but not found in results:", file=sys.stderr)
        for bibcode in sorted(missed):
            print(f"- {bibcode}", file=sys.stderr)

    return bibdata


if __name__ == "__main__":
    description = __doc__
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)

    parser.add_argument("bibfile", help="Name of file bib file to read", nargs="?")
    parser.add_argument(
        "-t",
        "--token",
        default="",
        help="""Token for accessing ADS API. Without a token the bib content is
        output without querying ADS but is sorted. You can get your token from
        ADS at https://ui.adsabs.harvard.edu/user/settings/token""",
    )
    args = parser.parse_args()

    with open(args.bibfile) as fd:
        # Read any prologue comments. Pybtex will ignore them but we want
        # to include them in the output.
        prologue = []
        for line in fd:
            if line.startswith("@"):
                # This is the start of the first real entry, so stop reading
                # comments.
                break
            prologue.append(line.strip())
        # Rewind the file to the start of the first non-comment line.
        fd.seek(0)
        this_bib = BibliographyData.from_string(fd.read(), "bibtex")

    # If no token is given, assume dry-run.
    token = args.token.strip()
    updated = process_bib(this_bib, token)

    # Sort the entries by bibkey.
    updated = BibliographyData(entries=sorted(updated.entries.items()))

    output = "\n".join(prologue) + "\n\n" + updated.to_string("bibtex")

    # pybtex is currently broken such that it escapes escapes:
    # https://bitbucket.org/pybtex-devs/pybtex/issues/153/backslashes-accumulate-when-saving-loading
    # Remove all the escaped \ characters (and assume that no titles have
    # them).
    output = output.replace("\\\\", "\\")

    # URL and DOI fields sometimes have % or _ and pybtex escapes
    # them. It probably shouldn't do that.
    lines = output.split("\n")
    for i, line in enumerate(lines):
        if re.match(r"^\s*(adsurl|url|doi) =", line):
            lines[i] = line.replace("\\", "")

    print("\n".join(lines))
