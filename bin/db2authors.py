#!/usr/bin/env python3

"""
Load the author list and database from the support directory and
convert it to an author tex file using AASTeX6.1 syntax.

  python3 db2authors.py > authors.tex

The list of authors for the paper should be defined in a authors.yaml
file in the current working directory.  This YAML file contains a
sequence of author IDs matching the keys in the author database
file in the etc/authordb.yaml file in this package.

This program requires the "yaml" package to be installed.

"""

import argparse
import os
import os.path
import re
import sys

import yaml

# Set to True to write a comma separated list of authors
WRITE_CSV = False

# There is a file listing all the authors and a file mapping
# those authors to full names and affiliations

# This is the author list. It's a yaml file with authorID that
# maps to the database file below.  For now we assume this file is in
# the current working directory.
authorfile = os.path.join("authors.yaml")

# this should probably be a dict with the value of affil_cmd
# the keys could then be passed to the arg parser.
OUTPUT_MODES = ["aas", "spie", "adass", "arxiv", "ascom", "webofc", "lsstdoc"]

description = __doc__
formatter = argparse.RawDescriptionHelpFormatter
parser = argparse.ArgumentParser(description=description, formatter_class=formatter)

parser.add_argument(
    "-m",
    "--mode",
    default="aas",
    choices=OUTPUT_MODES,
    help="""Display mode for translated parameters.
                         'verbose' displays all the information...""",
)
parser.add_argument("-n", "--noafil", action="store_true", help="""Do not add affil at all for arxiv.""")
args = parser.parse_args()

buffer_affil = False  # hold affiliation until after author output
buffer_authors = False  # out put authors in one \author command (adass)
affil_cmd = "affiliation"  # command for latex affiliation
affil_form = r"\{cmd}[{affilId}]{{{affil}}}"  # format of the affiliation
auth_afil_form = "{affilAuth}{affilSep}{affilInd}"  # format of author with affiliation
author_form = r"\author{orcid}{{{initials}~{surname}}}"  # format of the author
author_super = False  # Author affiliation as super script
author_sep = " and "
# AASTeX7 currently requires an affiliation field but it can be empty.
noaffil_cmd = r"\noaffiliation" + "\n" + r"\affiliation{}"

# The default is AAS and if no mode is specified you get that
if args.mode == "arxiv":
    author_form = "{orcid} {initials}{surname}"
    affil_cmd = ""
    affil_out_sep = ", "
    affil_form = r"{cmd}({affilId}) {affil}"
    auth_afil_form = "{affilAuth}{affilSep}({affilInd})"  # format of author with affiliation
    buffer_affil = True
    buffer_authors = True
    author_sep = ", "

if args.mode == "spie":
    affil_cmd = "affil"
    buffer_affil = True

if args.mode == "adass":
    affil_cmd = "affil"
    affil_out_sep = "\n"
    affil_form = r"\{cmd}{{$^{affilId}${affil}}}"
    auth_afil_form = "{affilAuth}{affilSep}$^{affilInd}$"
    author_form = "{initials}~{surname}{affilAuth}"  # initial, surname, affil
    buffer_affil = True
    buffer_authors = True
    author_super = True

if args.mode == "ascom":
    author_form = r"\author[{affilAuth}]{{{initials}~{surname}}}"  # format of the author
    buffer_affil = True
    affil_out_sep = ", "
    auth_afil_form = "{affilInd}{affilAuth}{affilSep}"

if args.mode == "webofc":
    affil_cmd = ""
    author_sep = " \\and\n"
    affil_out_sep = " \\and\n"
    buffer_affil = True
    buffer_authors = True
    author_form = r"    \firstname{{{initials}}} \lastname{{{surname}}} {affilAuth}"
    auth_afil_form = "{affilAuth}{affilSep}\\inst{{{affilInd}}}"
    affil_form = "{affil}"

if args.mode == "lsstdoc":
    affil_cmd = ""
    author_sep = ",\n"
    affil_out_sep = ""
    buffer_affil = True
    buffer_authors = True
    author_form = "{initials}~{surname}"
    affil_form = ""

with open(authorfile) as fh:
    authors = yaml.safe_load(fh)

# This is the database file with all the generic information
# about authors. Locate it relative to this script.
exedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.normpath(os.path.join(exedir, os.path.pardir, "etc", "authordb.yaml"))

with open(dbfile) as fh:
    authordb = yaml.safe_load(fh)

# author db is dict indexed by author id.
# Each entry is a dict with keys
# name: Surname
# initials: A.B.
# orcid: ORCID (can be None)
# affil: List of affiliation labels
# altaffil: List of alternate affiliation text
authorinfo = authordb["authors"]

# dict of all the affiliations, key is a label
# used in author list
affil = authordb["affiliations"]
affilset = []  # it will be a set but I want index() which is supported in list

# Email domains, keyed on affiliation.
emails = authordb["emails"]

# AASTeX7 author files are of the form:
# \author[ORCID]{Initials~Surname}
# \email{manndetory}
# \altaffiliation{Hubble Fellow}   * must come straight after author
# \affiliation{Affil1}
# \affiliation{Affill2}
# Do not yet handle  \correspondingauthor

if WRITE_CSV:
    # Used for arXiv submission
    names = [f"{a['initials']} {a['name']}" for a in authors]
    print(", ".join(names))
    sys.exit(0)

print(
    """%% DO NOT EDIT THIS FILE. IT IS GENERATED FROM db2authors.py"
%% Regenerate using:"""
)
print(f"%%    python $LSST_TEXMF_DIR/bin/db2authors.py -m {args.mode} ")
print()

authOutput = []
allAffil = []
pAuthorOutput = []
indexOutput = []

anum = 0


def get_initials(initials):
    """Get the initials rather than full name.

    Authors db has full name not initials -
    sometimes we just want initials.
    """
    names = re.split(r"[ -\.\~]", initials)
    realInitials = []
    for name in names:
        if len(name) > 0:
            realInitials.append(name[0])
    return "~" + ".~".join(realInitials) + "."


for anum, authorid in enumerate(authors):
    orcid = ""

    try:
        auth = authorinfo[authorid]
    except KeyError as e:
        raise RuntimeError(f"Author ID {authorid} not defined in author database.") from e

    affilOutput = []
    affilAuth = ""
    affilSep = ""
    if author_super and anum < len(authors) - 1:
        # ADASS  comma before the affil except the last entry
        affilSep = ","
    for theAffil in auth["affil"]:
        if theAffil not in affilset:
            affilset.append(theAffil)
            if theAffil == "_":
                affilOutput.append(noaffil_cmd)
            else:
                # Unfortunately you can not output an affil before an author.
                affilOutput.append(
                    affil_form.format(cmd=affil_cmd, affilId=len(affilset), affil=affil[theAffil])
                )

        affilInd = affilset.index(theAffil) + 1
        if args.noafil:
            affilAuth = affilAuth
        else:
            affilAuth = auth_afil_form.format(affilAuth=affilAuth, affilInd=affilInd, affilSep=affilSep)

        affilSep = " "

    if buffer_affil:
        orcid = f"[{affilAuth}]"
    else:
        if "orcid" in auth and auth["orcid"]:
            orcid = "[{}]".format(auth["orcid"])

    orc = auth.get("orcid", "")
    if orc is None:
        orc = ""

    email = auth.get("email", "")
    if "@" in email:
        username, domain = email.split("@", 1)
    else:
        username = email
        domain = auth["affil"][0]
    if "." not in domain:
        # This is a key to a email domain.
        domain = emails.get(domain)
    if args.mode == "aas" and (not domain or not username) and auth["affil"][0] != "_":
        # Only warn if we need the email.
        print(
            f"WARNING: Unable to resolve email address for author '{authorid}' email '{email}'",
            file=sys.stderr,
        )
    if not domain:
        domain = "none.com"
    if not username:
        username = "unknown"
    email = f"{username}@{domain}"

    # For spaces in surnames use a ~
    surname = re.sub(r"\s+", "~", auth["name"])

    # Preference for A.~B.~Surname rather than A.B.~Surname
    initials = re.sub(r"\.(\w)", lambda m: ".~" + m.group(1), auth["initials"])

    # For spaces in initials use a ~
    initials = re.sub(r"\s+", "~", initials)

    # adass has index and paper authors ..
    addr = [a.strip() for a in affil[theAffil].split(",")]
    tute = addr[0]
    ind = len(addr) - 1
    state = ""
    pcode = ""
    country = ""
    if ind > 0:
        country = addr[ind]
        ind = ind - 1
    if ind > 0:
        sc = addr[ind].split()
        ind = ind - 1
        state = sc[0]
        pcode = ""
        if len(sc) == 2:
            pcode = sc[1]
    city = ""
    if ind > 0:
        city = addr[ind]

    pAuthorOutput.append(
        r"\paperauthor"
        f"{{{initials}~{surname}}}{{{email}}}{{{orc}}}"
        f"{{{tute}}}{{}}{{{city}}}{{{state}}}{{{pcode}}}{{{country}}}"
    )

    if args.mode == "arxiv":
        affilOutput = []  # reset this
        affilOutput.append(affil_form.format(cmd=affil_cmd, affilId=len(affilset), affil=tute))

    justInitials = get_initials(initials)
    indexOutput.append(rf"%\aindex{{{surname},{justInitials}}}")

    author = author_form.format(orcid=orcid, initials=initials, surname=surname, affilAuth=affilAuth)
    if buffer_authors:
        if args.mode == "webofc" and orc:
            author += f" \\orcidlink{{{orc}}}"
        authOutput.append(author)
        allAffil = allAffil + affilOutput
    else:
        print(author)
        if auth.get("altaffil"):
            for af in auth["altaffil"]:
                print(rf"\altaffiliation{{{af}}}")

        # The affiliations have to be retrieved via label
        for aflab in auth["affil"]:
            if aflab == "_":
                print(noaffil_cmd)
            else:
                print(rf"\{affil_cmd}{{{affil[aflab]}}}")
        if args.mode == "aas":
            print(rf"\email{{{email}}}")
    print()

if buffer_authors:
    if args.mode == "arxiv":
        print(r"Authors:", end="")
    else:
        print(r"\author{", end="")
    anum = 0
    numAuths = len(authOutput) - 1
    for auth in authOutput:
        print(auth, end="")
        anum = anum + 1
        if (anum == numAuths and numAuths > 1) or (
            args.mode in ("arxiv", "webofc", "lsstdoc") and anum < numAuths
        ):
            print(author_sep, end="")
        else:
            if anum < numAuths:
                print(" ", end="")
    if args.mode == "arxiv":
        print("\n(", end="")
    else:
        print("}")
    if not args.noafil:
        if args.mode == "webofc":
            print("\\institute{")
        print(*allAffil, sep=affil_out_sep, end="")
        if args.mode == "webofc":
            print("\n}")
    if args.mode == "arxiv":
        print(")\n")
    if args.mode == "adass":
        print("")
        print(*pAuthorOutput, sep="\n")
        print("% Yes they said to have these index commands commented out.")
        print(*indexOutput, sep="\n")
