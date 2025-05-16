#!/usr/bin/env python3

"""
Utility that can be executed in a latex document directory and will
produce a bib entry suitable to be put in lsst.bib in texmf.

"""

import argparse
import re
from datetime import datetime

from bibtools import BibEntry


def find_meta(filename: str) -> BibEntry:
    """Search for the bibentry items

    Parameters
    ----------
    filename : `str`
        Path to file.

    Returns
    -------
    bibentry : `bibtools.BibEntry'
        Ready to use bib entry
    """
    auth = re.compile(r"\\author\s*{([\w'`,\- ]+)}")
    title = re.compile(r"\\title\s*[\[\]a-z A-Z\\]+{([\w\\#,:\-\+ ]+)}")  # a real pity .+ consumes closing }
    title2 = re.compile(r"\\title\{(.+)} \\setD")  # a real pity .+ consumes closing }
    yearm = re.compile(r"\\date\s*{([0-9]+)-([0-9]+)-.+}")  # only if its an actual date not a macro
    yearm2 = re.compile(r"\\vcs[dD]ate}{(.+)-(.+)-.+}")  # only chance from meta.tex if it was a macro
    handle = re.compile(r"\\setDocRef\s*{([A-Z]+-[0-9]+)}")
    comment = re.compile(r"%.*")
    doctype = re.compile(r"lsstDocType}{(.+)} .+\\")
    docnum = re.compile(r"lsstDocNum}{([0-9]+)} .+\\")

    # Read the content of the file into a single string
    lines = []
    be = BibEntry()
    be.year = datetime.now().year
    be.month = datetime.now().strftime("%h")
    doctypes = ""
    docnums = ""
    meta = filename == "meta.tex"
    with open(filename) as fd:
        for line in fd:
            line = line.strip()
            # Latex specific ignore
            if not meta and (
                line.startswith(r"\def")
                or line.startswith(r"\newcommand")
                or line.startswith(r"\renewcommand")
                or line.startswith("%")
            ):
                continue
            line = comment.sub("", line)
            lines.append(line)
        text = " ".join(lines)

    if meta:
        rset = doctype.findall(text)
        if rset:
            doctypes = rset[0]
            end = doctypes.find("}")
            doctypes = doctypes[0:end]
        rset = docnum.findall(text)
        if rset:
            docnums = rset[0]
        if not be.handle:
            be.handle = f"{doctypes}-{docnums}"
        yearmm = yearm2.findall(text)
        if yearmm:
            be.year = yearmm[0][0]
            be.month = yearmm[0][1]
    else:
        rset = auth.findall(text)
        if rset:
            be.author = rset[0]
        rset = title.findall(text)
        if rset:
            be.title = rset[0]
        else:
            rset = title2.findall(text)
            if rset:
                be.title = rset[0]
        rset = handle.findall(text)
        if rset:
            be.handle = rset[0]
        else:
            be.handle = f"{doctypes}-{docnums}"
        yearmm = yearm.findall(text)
        if yearmm:
            be.year = yearmm[0][0]
            be.month = yearmm[0][1]

    return be


def main(texfiles: tuple[str, ...]) -> None:
    """Run program and generate bibentry ."""
    if not texfiles:
        raise RuntimeError("No files supplied.")
    be = BibEntry()
    for f in texfiles:
        rbe = find_meta(f)
        if rbe.author and not be.author:
            be.author = rbe.author
        if rbe.title and not be.title:
            be.title = rbe.title
        if rbe.month and not be.month:
            be.month = rbe.month
        if rbe.year and not be.year:
            be.year = rbe.year
        if rbe.handle and not be.handle:
            be.handle = rbe.handle
    be.write_latex_bibentry()


if __name__ == "__main__":
    description = __doc__
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)

    parser.add_argument(
        "files",
        metavar="FN",
        nargs="+",
        help="FILE to process - usually the main LDM,DMTN tex file",
    )

    args = parser.parse_args()
    texfiles = args.files
    main(texfiles)
