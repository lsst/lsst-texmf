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
import posixpath
import re
import sys
import urllib.parse

import requests
from pybtex.database import BibliographyData


def process_bib(bibdata: BibliographyData, token: str) -> BibliographyData:
    """Scan through the bibliography data and update ADS entries whilst
    retaining the bibkey.
    """
    # It is possible that the bibkey is not the ADS bibcode, so we need to
    # map the bib key to bibcode.
    to_update: dict[str, str] = {}
    for bibkey, entry in bibdata.entries.items():
        if adsurl := entry.fields.get("adsurl"):
            parsed = urllib.parse.urlparse(adsurl)
            # Old URLs put bibcode in the query params.
            if parsed.query:
                # Sometimes a bib file latex escapes the &.
                qs = parsed.query.replace("\\&", "&")
                parsed_query = urllib.parse.parse_qs(qs)
                bibcode = parsed_query["bibcode"][0]
            else:
                bibcode = posixpath.basename(parsed.path)
            # Some old bib files try to escape the % or &
            bibcode = bibcode.replace("\\%", "%")
            bibcode = bibcode.replace("\\&", "&")
            bibcode = urllib.parse.unquote(bibcode)

            if not bibcode:
                print("Failed to extract bibcode from ", adsurl, file=sys.stderr)
                continue
            to_update[str(bibkey)] = bibcode

    print(f"Found {len(to_update)} ADS entries.", file=sys.stderr)

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
    for bibkey, bibcode in to_update.items():
        print(f"Replacing bibkey {bibkey} with data from {bibcode} ...", end="", file=sys.stderr)
        if updated := updated_bibdata.entries.get(bibcode):
            updated.key = bibkey  # Consistency.
            bibdata.entries[bibkey] = updated
            print("updated", file=sys.stderr)
            retrieved.remove(bibcode)
        else:
            print("not found", file=sys.stderr)
            missed.add(bibcode)

    if retrieved:
        print("The following bibcodes were retrieved but not associated:", file=sys.stderr)
        for bibcode in sorted(retrieved):
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
    parser.add_argument("-t", "--token", default="", help="""Token for accessing ADS API""")
    args = parser.parse_args()

    with open(args.bibfile) as fd:
        this_bib = BibliographyData.from_string(fd.read(), "bibtex")

    # If no token is given, assume dry-run.
    token = args.token.strip()
    updated = process_bib(this_bib, token)

    output = updated.to_string("bibtex")

    # pybtex is currently broken such that it escapes escapes:
    # https://bitbucket.org/pybtex-devs/pybtex/issues/153/backslashes-accumulate-when-saving-loading
    # Remove all the escaped \ characters (and assume that no titles have
    # them).
    output = output.replace("\\\\", "\\")

    # URL and DOI fields sometimes have % or _ and pybtex escapes
    # them. It probably shouldn't do that.
    lines = output.split("\n")
    for i, line in enumerate(lines):
        if re.match(r"^\s*(url|doi) =", line):
            lines[i] = line.replace("\\", "")

    print("\n".join(lines))
