#!/usr/bin/env python3

r"""Utility that interogates ook (lsst.io) to get doc metadata
then generates a bibfile fpr inclusion in texmf.
"""

import argparse
from algoliasearch.search_client import SearchClient
from datetime import datetime
import sys
import calendar

MAXREC = 5000


def write_latex_bibentry(auth, title, year, month, handle, fd=sys.stdout):
    """ Write a bibentry for document info passed
    Parameters
    ----------
    auth : `str``
        Author list ready for tex
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


def generate_bibfile(outfile, query):

    client = SearchClient.create('0OJETYIVL5', 'b7bd2f1080a5c4fe5eee502462bcc9d3')
    index = client.init_index('document_dev')

    params = {
        'attributesToRetrieve': [
            'handle',
            'series',
            'h1',
            'baseUrl',
            'sourceUpdateTime',
            'sourceUpdateTimestamp',
            'authorNames'
        ],
        'hitsPerPage': MAXREC
    }

    res = index.search(query, params)

    print('## DO NOT EDIT THIS FILE. It is generated from generateBibfile.py\n'
          '## Add static entries in etc/static_entries.bib (or remove them if they clash.\n'
          '## This files should contain ALL entries on www.lsst.io ', file=outfile)

    bcount = 0
    for count, d in enumerate(res['hits']):
        if d['series'] == "TESTN":
            continue
        bcount = bcount + 1
        authors = " and "
        authors = authors.join(d['authorNames'])
        dt = d['sourceUpdateTimestamp']
        date = datetime.fromtimestamp(dt)
        month = calendar.month_abbr[date.month].lower()
        write_latex_bibentry(checkFixAuthAndComma(fixTexSS(authors)), fixTex(d['h1']),
                             date.year, month, d['handle'], outfile)
        print(file=outfile)

    print(f"Got {count} records max:{MAXREC} produced {bcount} bibentries to {outfile}")


def fixTex(text):
    specialChars = "_$&%^#"
    for c in specialChars:
        text = text.replace(c, f"\\{c}")
    return text


def checkFixAuthAndComma(authors):
    if "," in authors and "and" not in authors:
        #a bit heav handed but
        authors = authors.replace(",", "and")


def fixTexSS(text):
    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        for ci, co in [('’', "'"),
                       ('…', '...'),
                       ('…', '...'),
                       ('“', '"'),
                       ('”', '"'),
                       ('´', "'"),
                       (' ', ' '),
                       ('—', '-'),
                       ('\U0010fc0e', '?'),  # '?' in a square
                       ('？', '?'),
                       ('à', '\\`{a}'),  # grave
                       ('á', "\\'{a}"),  # acute
                       ('â', '\\r{a}'),
                       ('Ç', '\\c{C}'),
                       ('ć', "\\'{c}"),
                       ('ç', '\\c{c}'),
                       ('ë', '\\"{e}'),
                       ('é', "\\'{e}"),
                       ('è', "\\`{e}"),
                       ('ê', '\\r{e}'),
                       ('¡', 'i'),
                       ('í', "\\'{i}"),
                       ('ó', "\\'{o}"),
                       ('ñ', '\\~{n}'),
                       ('ö', '\\"{o}'),
                       ('û', '\\r{u}'),
                       ('ü', '\\"{u}'),
                       ('ù', "\\`{u}"),
                       ('ž', '{\\v z}'),
                       ('Ž', '{\\v Z}'),
                       ('􏰎', ' '),
                       ('ï', '\\"{i}'),  # really i dieresis
                       ('ô', '\\r{o}'),
                       ('–', '-'),
                       ('‘', "'"),
                       ('ʻ', '\''),
                       ('¹', ''),
                       ('²', ''),
                       ('³', ''),
                       ('²', ''),
                       ('⁴', ''),
                       ('⁵', ''),
                       ('⁶', ''),
                       ('⁷', ''),
                       ('⁸', ''),
                       ]:
            text = text.replace(ci, co)
    return text


if __name__ == "__main__":
    description = __doc__
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=formatter)

    parser.add_argument('bibfile', help='Name of file to output bib entries to')
    parser.add_argument("-q", "--query", help="""Query string (optional)""")

    args = parser.parse_args()

    outfile = sys.stdout
    if args.bibfile:
        outfile = open(args.bibfile, 'w')

    generate_bibfile(outfile, args.query)
    outfile.close()