#!/usr/bin/env python3

"""
Utility that ican be executed in a latex document directory and will
produce a bib entry suitable to be put in lsst.bib in texmf.

"""

import sys
import re
import argparse
from datetime import datetime


def find_meta(filename):
    """search for the bibentry items

    Parameters
    ----------
    filename : `str`
        Path to file.

    Returns
    -------
    bibentry : `str'
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
    year = datetime.now().year
    month = datetime.now().strftime('%h')
    auths = ""
    titles = ""
    handles = ""
    doctypes = ""
    docnums = ""
    meta = filename == "meta.tex"
    with open(filename, "r") as fd:
        for line in fd:
            line = line.strip()
            # Latex specific ignore
            if (not meta and (line.startswith(r"\def") or
                              line.startswith(r"\newcommand") or
                              line.startswith(r"\renewcommand") or
                              line.startswith("%"))):
                continue
            line = comment.sub("", line)
            lines.append(line)
        text = " ".join(lines)

    if (meta):
        rset = doctype.findall(text)
        if (rset):
            doctypes = rset[0]
            end = doctypes.find('}')
            doctypes = doctypes[0:end]
        rset = docnum.findall(text)
        if (rset):
            docnums = rset[0]
        if not handles:
            handles = f"{doctypes}-{docnums}"
        yearmm = yearm2.findall(text)
        if (yearmm):
            year = yearmm[0][0]
            month = yearmm[0][1]
    else:
        rset = auth.findall(text)
        if (rset):
            auths = rset[0]
        rset = title.findall(text)
        if (rset):
            titles = rset[0]
        else:
            rset = title2.findall(text)
            if (rset):
                titles = rset[0]
        rset = handle.findall(text)
        if (rset):
            handles = rset[0]
        else:
            handles = f"{doctypes}-{docnums}"
        yearmm = yearm.findall(text)
        if (yearmm):
            year = yearmm[0][0]
            month = yearmm[0][1]

    return auths, titles, year, month, handles


def write_latex_bibentry(auth, title, year, month, handle, fd=sys.stdout):
    """ Write a bibentry based inthe current document
    Parameters
    ----------
    auth : `str``
        Author
    title : `str`
    year  : `str`
    month  : `str`
    handle  : `str`

    """

    print("@DocuShare{{{},".format(handle), file=fd)
    print("   author = {{{}}},".format(auth), file=fd)
    print("    title = {{{}}},".format(title), file=fd)
    print("     year = {},".format(year), file=fd)
    print("    month = {},".format(month), file=fd)
    print("   handle = {{{}}},".format(handle), file=fd)
    print("      url = {{http://{}.lsst.io }} }}".format(handle), file=fd)


def main(texfiles):
    """Run program and generate bibentry ."""

    if not texfiles:
        raise RuntimeError("No files supplied.")
    auth = ""
    title = ""
    year = ""
    month = ""
    handle = ""
    for f in texfiles:
        rauth, rtitle, ryear, rmonth, rhandle = find_meta(f)
        if (rauth and not auth):
            auth = rauth
        if (rtitle and not title):
            title = rtitle
        if (rmonth and not month):
            month = rmonth
        if (ryear and not year):
            year = ryear
        if (rhandle and not handle):
            handle = rhandle
    write_latex_bibentry(auth, title, year, month, handle)


if __name__ == "__main__":
    description = __doc__
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=formatter)

    parser.add_argument('files', metavar='FN', nargs='+',
                        help='FILE to process - usullly the main LDM,DMTN tex file')

    args = parser.parse_args()
    texfiles = args.files
    main(texfiles)
