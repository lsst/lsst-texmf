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
from collections import Counter

from bibtools import get_ads_bibcode
from pybtex.database import BibliographyData


def process_bib(bibdata: BibliographyData) -> dict[str, str]:
    """Read the bib data and return a mapping of bib key to bibcode."""
    bibcode_map: dict[str, str] = {}
    for bibkey, entry in bibdata.entries.items():
        if bibcode := get_ads_bibcode(entry):
            bibcode_map[bibkey] = bibcode
    return bibcode_map


# Keep track of what was replaced.
REPLACED: Counter[str] = Counter()

# Match \cite…{<keys>} where <keys> is anything up to the next }
# Also allows `\citep[][]{key}`
cite_cmd = re.compile(r"(\\cite[a-zA-Z]*(?:\[[^\]]*\])*)\{([^}]*)\}")


def _replace_keys(keys_str: str, bibkey_map: dict[str, str]) -> str:
    # Split on commas but KEEP the separators (and their spaces) to preserve
    # formatting.
    global REPLACED

    parts = re.split(r"(\s*,\s*)", keys_str)
    out = []
    for part in parts:
        # If it's a comma (with whatever spaces), keep as-is
        if re.fullmatch(r"\s*,\s*", part):
            out.append(part)
            continue

        # It's a key (with possible leading/trailing spaces) — preserve those
        # spaces.
        leading = part[: len(part) - len(part.lstrip())]
        trailing = part[len(part.rstrip()) :]
        key = part.strip()

        # Replace if we have a mapping; otherwise leave the key untouched.
        new_key = bibkey_map.get(key, key)
        if new_key != key:
            REPLACED[new_key] += 1
        out.append(f"{leading}{new_key}{trailing}")

    return "".join(out)


def replace_citation_keys(latex_text: str, bibkey_map: dict[str, str]) -> str:
    """Replace any bib keys in the text with new values."""

    def repl(m: re.Match) -> str:
        prefix = m.group(1)
        keys = m.group(2)
        modified = _replace_keys(keys, bibkey_map)
        return f"{prefix}{{{modified}}}"

    return cite_cmd.sub(repl, latex_text)


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

    # Process each tex file and replace the bib keys.
    for texfile in args.texfiles:
        REPLACED = Counter()  # Reset the counter.
        with open(texfile) as fd:
            text = fd.read()

        # Replace the bib keys in the text.
        new_text = replace_citation_keys(text, bibkey_map)

        # Write the modified text back to the file.
        with open(texfile, "w") as fd:
            fd.write(new_text)
        print(f"Updated {texfile} with {len(REPLACED)} new bib keys.", file=sys.stderr)

    # Now update the local.bib file with the new bibcodes but do it without
    # using pybtex to avoid confusingly large diffs.
    pattern = re.compile(r"\{(" + "|".join(re.escape(k) for k in bibkey_map) + "),")

    def bibcode_replacer(match: re.Match) -> str:  # noqa: D103
        return "{" + bibkey_map[match.group(1)] + ","

    new_bibdata = pattern.sub(bibcode_replacer, bibfile_content)
    with open(args.bibfile, "w") as fd:
        fd.write(new_bibdata)
