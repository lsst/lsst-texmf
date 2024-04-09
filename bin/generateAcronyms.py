#!/usr/bin/env python3

r"""Utility that can be used to automatically generate a list of acronyms,
abbreviations and glossary entries from multiple TeX files.

Acronynm and glossary entries are read from the :file:`glossarydefs.csv` in
the lsst-texmf distribution. Optionally, this list may be augmented with local
definitions stored in :file:`myacronyms.txt`. Adding terms to
:file:`skipacronyms.txt` will cause them to be excluded.

By default, terms are written to a table in :file:`acronyms.tex` which may
then be included in a LaTeX document.

Alternatively, if the ``-g`` (or ``--glossary``) option is passed, they will be
written to :file:`aglossary.tex` in LaTeX glossary format instead. All
glossary lookup keys are the glossary name. For items to appear in the
glossary you must ``\gls{ITEM}`` at least once.

Passing ``-u`` or ``--update`` will process all LaTeX files to identify
potential glossary entries and will mark them with ``\gls``.

Use ``-m`` or ``--mode`` with ["txt", "rst","tex"] to choose output formats
"""

import argparse
import csv
import os.path
import re
import sys
import warnings

glsFile = "aglossary.tex"
OUTPUT_MODES = ["txt", "rst", "tex"]
specialChars = "_$&%^#"
specialCharsRe = re.compile(r"[_$&%^#]")

try:
    import pypandoc

    # raises OSError if pypandoc is available but pandoc isn't.
    pypandoc.get_pandoc_path()
except (ImportError, OSError):
    pypandoc = None


#  Match for extracting acronyms from the glossary myacronyms .txt files
MATCH_ACRONYM = r"^([\w/&\-\+ -']+)\s*:\s*(.*)$"
MATCH_ACRONYM_RE = re.compile(MATCH_ACRONYM)
# following regular expression define an acronym-like string as follows:
# - including upper case characters and numbers
# - starting with a letter
CAP_ACRONYM = re.compile(r"\b[A-Z][A-Z0-9]+\b")
pypandoc = None  # it can not handle gls


def _parse_line(line):
    """Parse a line and return an acronym and definition.

    Parameters
    ----------
    line : `str`
        Line to analyze.

    Returns
    -------
    acronym, definition : tuple(str, str)
        Acronym and definition. Tuple of None, None if the line has
        no acronym definition.
    """
    nothing = (None, None)

    # Blank lines
    line = line.strip()
    if not line:
        return nothing

    # Comment lines
    if line.startswith("#"):
        return nothing

    matched = MATCH_ACRONYM_RE.match(line)
    if not matched:
        return nothing

    acr, defn = matched.groups()
    return acr.rstrip(), defn


def read_glossarydef(filename, utags, init=None):
    """Read glossary  definitions from LSST format glossarydefs.csv file.

    Parameters
    ----------
    filename : `str`
        Path to LSST  format  glossary file. This is a csv file with the
        name, definition, tags etc ..
    utags : `set'
        List of tags supplied by user to decide which definition to keep when
        there are many.
    init : `dict`
        Initial definitions to augment with the content from this file.

    Returns
    -------

    acronyms : `dict`
        Dictionary with the acronyms as keys. The values are sets containing
        one or more definition associated with that acronym.
        Empty dict if the file can not be opened.
    """

    if init is None:
        definitions = {}
    else:
        definitions = init.copy()

    lc = 0
    with open(filename, "r") as fd:
        reader = csv.reader(fd, delimiter=",", quotechar='"')
        for row in reader:
            if len(row) < 2:  # blank line
                continue
            lc = lc + 1
            if lc == 1:
                continue  # There is a header line
            ind = 0
            try:
                acr = row[ind]
                defn = row[ind + 1]
                tags = row[ind + 2]
                entryType = row[ind + 5]
            except BaseException as ex:
                print(f"Error reading {filename} line {lc}-{row}")
                raise ex

            if not doGlossary and entryType == "G":
                # in the case I want only the acronym table and
                # I read a type "G" (glossary) definition, I discard it
                continue
            tagset = set()
            hasTag = False
            if tags:
                tagset.update(tags.split())
                hasTag = tagset.intersection(utags)
            if acr is None:
                continue

            if acr not in definitions:
                definitions[acr] = set()
            # Ok lets try to do something with Tags .. like if its tagged take
            # this one
            # should possibly keep the tags with the acronym ..
            # I will take the first definition - iff i get a tag match later
            # replace it

            if hasTag and definitions[acr]:
                # removed any other def take tagged one
                definitions[acr] = set()
            if not definitions[acr]:
                # already have a def and not matching tag so ignore new one
                definitions[acr].add((defn, entryType))

    return definitions


def read_myacronyms(
    filename="myacronyms.txt", allow_duplicates=False, defaults=None, utags=None
):
    """Read the supplied file and extract acronyms or glossary entries.

    File must contain lines in format if it is myacronyms.txt :

    ACRONYM:Definition

    but may be of the full glossarydef format if it is myglossarydefs.csv:

    ENTRY,Definition,TAGs,Doc Tags, Alternative terms ,Type

    The last entry, Type,  being A for acronym, G for glossary entry.


    A warning is issued if a duplicate identical definition is found in the
    simple format (for only acronyms). It is an error for the same acronym
    to have multiple differing entries.

    Parameters
    ----------
    filename : `str`
        Name of file to open.
    defaults : `dict`, optional
        `dict` containing default values to seed the returned definitions.
        The caller's dictionary will not be updated.
        Items in the current file override the values from the defaults
        without warning.

    Returns
    -------
    definitions : `dict`
        Dictionary with acronym as key and definition as value.
    """
    definitions = {}
    if filename.endswith(".csv"):
        localdefs = read_glossarydef(filename, utags)
        # flatten the set to a single entry for each glossarydef
        definitions = {d: options.pop() for d, options in localdefs.items()}
    else:
        with open(filename, "r") as fd:
            for line in fd:
                acr, defn = _parse_line(line)
                if acr is None:
                    continue

                if acr in definitions:
                    if defn != definitions[acr]:
                        raise RuntimeError(
                            "Duplicate definitions of {} differ in {}".format(
                                acr, filename
                            )
                        )
                    else:
                        warnings.warn(
                            UserWarning(
                                "Entry {} exists multiple times"
                                " with same definition in {}, you may"
                                " want to try using a tag (-t)".format(acr, filename)
                            )
                        )
                # myacronyms will contains by definition only acronyms
                definitions[acr] = (defn, "A")

    # Merge with the defaults
    if defaults is None:
        combined = definitions
    else:
        combined = defaults.copy()
        combined.update(definitions)

    return combined


def read_skip_acronyms(file_name="skipacronyms.txt"):
    """Read the supplied file to obtain a list of terms to skip.

    File must contain lines in format of one term per line. Repeat
    values are ignored.

    Parameters
    ----------
    file_name
        Name of file to open. The file does not need to exist.

    Returns
    -------
    skip : `set`
        Set containing terms to be skipped.
    """
    skip = set()
    if not os.path.exists(file_name):
        return skip

    with open(file_name, "r") as fd:
        for line in fd:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):  # comment
                continue

            skip.add(line)
    return skip


def find_matches_per_line(filename, acronyms, ignore_str=" %"):
    """Return list of matching acronyms in file.

    Parameters
    ----------
    filename : `str`
        Path to file.
    acronyms : `set`
        List of possible acronyms present in file.
    ignore_str : `str`, optional
        Anything from this string on in a line is not searched.
        Every line is searched if set to None. Default is tex comment.

    Returns
    -------
    matches : `set`
        List of matching acronyms from supplied list.
    missing : `set`
        List of acronyms used but not matched.
    """

    pattern = r"\b(" + "|".join(re.escape(w) for w in acronyms) + r")\b"
    regex = re.compile(pattern)

    matches = set()
    with open(filename, "r") as fd:
        for line in fd:
            if ignore_str:
                posn = line.find(ignore_str)
                if posn > -1:
                    line = line[:posn]
            # Now to test every acronym. We cannot use a simple "in"
            # because we do not want DMS to match DMS and DMSST
            these = regex.findall(line)
            matches.update(these)

    return matches, set()


def find_matches_combo(filename, acronyms, ignore_str=" %"):
    """Return list of matching acronyms in file.

    Parameters
    ----------
    filename : `str`
        Path to file.
    acronyms : `set`
        List of possible acronyms present in file.
    ignore_str : `str`, optional
        Anything from this string on in a line is not searched.
        Every line is searched if set to None. Default is tex comment.
        Only used if pypandoc is not available.

    Returns
    -------
    matches : `set`
        List of matching acronyms from supplied list.
    missing : `set`
        Set of acronyms found in the text but that do not have any definitions.
    """

    if pypandoc is not None:
        # Use markdown rather than plain text because
        # for plain text \textbf{Int} is converted to "INT"
        # for emphasis.
        # \gls{XXX} however is completely removed
        text = pypandoc.convert_file(filename, "markdown", format="latex")
    else:
        # Read the content of the file into a single string
        lines = []
        with open(filename, "r") as fd:
            for line in fd:
                if ignore_str:
                    posn = line.find(ignore_str)
                    if posn > -1:
                        line = line[:posn]
                line = line.strip()

                # Latex specific ignore
                if (
                    line.startswith(r"\def")
                    or line.startswith(r"\newcommand")
                    or line.startswith(r"\renewcommand")
                    or line.startswith("%")
                ):
                    continue
                line = escape_for_tex(line)
                lines.append(line)

            text = " ".join(lines)

    # Do two passes. First look for usages of acronyms that have lower
    # case characters, number or special characters.
    # These do not look like "normal" acronyms so special case them.
    # Also single character acronyms (which should probably be banned)
    # CAP_ACRONYM cannot be used here since it search for substrings
    nonstandard = {
        a for a in acronyms if not a.isupper() or not a.isalpha() or len(a) == 1
    }

    # findall matches non-overlapping left to right in the order that
    # we give alternate strings. Therefor when we build the regex
    # ensure that we supply strings sorted by length. Ideally we would also
    # take into account word boundaries but for now length ensures that
    # R&D matches before R and D.
    sorted_nonstandard = sorted(nonstandard, key=len, reverse=True)

    # This pattern matches all defined acronyms, even those with lower
    # case characters and things like "&"
    pattern = r"\b(" + "|".join(re.escape(w) for w in sorted_nonstandard) + r")\b"
    regex = re.compile(pattern)

    matches = set(regex.findall(text))

    # Now look for all acronym-like strings in the text, defined as a
    # collection of 2 or more upper case characters with word boundaries
    # either side.
    regex = CAP_ACRONYM
    used = set(regex.findall(text))

    gls = set()
    if doGlossary:
        # now Glossary entries Gls gls use group ( )
        # to catch what's between { }
        regex = re.compile(r"ls{([\w ]+)}")
        gls = set(regex.findall(text))
        used.update(gls)

    # For all acronyms that were used and have existing definitions, add
    # them to the current list of matches
    matches.update(used & acronyms)
    # For all gls entries  that were used and have existing definitions, add
    matches.update(gls & acronyms)
    # still a problems for COMPOUND ENTRIES like NASA ROSES  ..
    # ROSES is tagged as missing

    # Calculate all the acronyms we found in the text but which do not
    # have definitions.
    missing = used - matches

    return matches, missing


find_matches = find_matches_combo


def escape_for_tex(str):
    """Escape tex nasties and return new string.
    But watch out for double whamies .."""
    text = str
    for c in specialChars:
        text = text.replace(c, f"\\{c}")
        text = text.replace(f"\\\\{c}", f"\\{c}")
    return text


def write_latex_glossary(acronyms, fd=sys.stdout):
    """Write a glossary file with newglossaryitem per definition  -
    or new acronym if it is type A for acronym.

    Parameters
    ----------
    acronyms : `list`
        List of 2-tuples with acronym and definition.
    fd : `file`, optional
    """

    print(
        f"% DO NOT EDIT - generated by {sys.argv[0]} from "
        "https://lsst-texmf.lsst.io/.",
        file=fd,
    )
    for acr, defn in acronyms:
        definition = escape_for_tex(defn[0])
        # entry has a lookup and a display version
        # the display one needs escaping
        acr2 = escape_for_tex(acr)
        if defn[1] == "A":
            print(
                "\\newacronym{{{}}} {{{}}} {{{}}}".format(acr, acr2, definition),
                file=fd,
            )
        else:
            print(
                "\\newglossaryentry{{{}}} {{name={{{}}},"
                " description={{{}}}}}".format(acr, acr2, definition),
                file=fd,
            )


def write_latex_table(acronyms, dotex=True, dorst=False, fd=sys.stdout):
    """Write latex table to supplied file descriptor.

    Parameters
    ----------
    acronyms : `list`
        List of 2-tuples with acronym and definition.
    """
    sep = " & "
    end = r" \\\hline"
    if dorst:
        print(r""".. _table-label: """, file=fd)
        print(r"""""", file=fd)
        print(r"""======= ===========""", file=fd)

    if dotex:
        print(
            r"""\addtocounter{table}{-1}
\begin{longtable}{p{0.145\textwidth}p{0.8\textwidth}}\hline
\textbf{Acronym} & \textbf{Description}  \\\hline
""",
            file=fd,
        )
    else:
        print("Acronym\tDescription", file=fd)
        if dorst:
            print(r"""======= ===========""", file=fd)
        sep = "\t"
        end = ""
    for acr, defn in acronyms:
        if len(defn) > 1:
            defn = defn[0]
        acr = escape_for_tex(acr)
        print(f"{acr}{sep}{defn}{end}", file=fd)
    if dotex:
        print(r"\end{longtable}", file=fd)
    if dorst:
        print(r"""======= ===========""", file=fd)


def forceConverge(prevCount, utags, noadorn, skipnone):
    """Run through the glossary looking for defnitions until
    no more are added.
    """
    while True:
        count = main({glsFile}, True, utags, True, False, "tex", noadorn, skipnone)
        # If no glossary items are added we are done
        if count == prevCount:
            break
        prevCount = count


def setup_paths():
    defaults_dir = os.path.join(os.path.dirname(__file__), os.path.pardir, "etc")
    lsst_glossary_path = os.path.join(defaults_dir, "glossarydefs.csv")
    global_skip_path = os.path.join(defaults_dir, "skipacronyms.txt")
    return (lsst_glossary_path, global_skip_path)


def main(texfiles, doGlossary, utags, dotex, dorst, mode, noadorn, skipnone=False):
    """Run program and generate acronyms file."""

    if not texfiles:
        raise RuntimeError("No files supplied.")

    lsst_glossary_path, global_skip_path = setup_paths()

    # Read the full set
    lsst_definitions = read_glossarydef(lsst_glossary_path, utags)

    # Read the local set  myacronyms.txt or  myglossarydefs.csv
    try:
        local_definitions = read_myacronyms()
    except FileNotFoundError:
        try:
            local_definitions = read_myacronyms(
                filename="myglossarydefs.csv", utags=utags
            )
        except FileNotFoundError:
            local_definitions = {}

    # Get list of acronyms to ignore
    global_skip = read_skip_acronyms(global_skip_path)

    try:
        # Read optional local skip file
        local_skip = read_skip_acronyms()
    except FileNotFoundError:
        skip = global_skip
    else:
        skip = global_skip | local_skip

    # Remove the skipped items
    if not skipnone:
        for s in skip:
            if s in local_definitions:
                local_definitions.pop(s)
            if s in lsst_definitions:
                lsst_definitions.pop(s)

    # Master list of all acronyms
    acronyms = set(lsst_definitions) | set(local_definitions)

    # Scan each supplied tex file looking for the acronym
    matches = set()
    missing = set()
    for f in texfiles:
        local_matches, local_missing = find_matches(f, acronyms)
        matches.update(local_matches)
        missing.update(local_missing)

    print("Matched {} acronyms".format(len(matches)), file=sys.stderr)

    # Report missing definitions, taking into account skips
    missing = missing - skip

    if len(missing):
        print(
            "List of potential acronyms found in your text "
            "that you may be missing. Please ignore if not relevant "
            "(note that the list may not be complete)."
        )
        for m in missing:
            print("Missing definition: {}".format(m), file=sys.stderr)

    # Attach definitions to matches
    results = []
    for acr in sorted(matches):
        if acr in local_definitions:
            results.append((acr, local_definitions[acr]))
        elif acr in lsst_definitions:
            options = lsst_definitions[acr]
            if len(options) > 1:
                print(
                    "Entry {} exists multiple ({}) times. "
                    "Including all definitions.".format(acr, len(options)),
                    file=sys.stderr,
                )
            for a in options:
                results.append((acr, a))
        else:
            raise RuntimeError("Internal error handling {}".format(acr))

    acrFile = f"acronyms.{mode}"
    if doGlossary and dotex:  # otherwise its just a table
        if not noadorn:
            results = update_gls_entries(results, lsst_definitions)
        with open(glsFile, "w") as gfd:
            write_latex_glossary(results, fd=gfd)
    else:
        with open(acrFile, "w") as fd:
            write_latex_table(results, dotex, dorst, fd=fd)
    return len(results)


def update_gls_entries(results, GLSlist):
    r"""Scan through the acronym and gls definitions and add \gls where
    appropriate (similar to -u for the files)"""

    new_result = []
    regexmap = make_regexmap(GLSlist)

    for entry in results:
        defn = entry[1][0]
        type = entry[1][1]
        acr = entry[0]
        if type == "A":  # just see if we have a glossary match
            if defn in GLSlist:  # ok we gls the entire thing
                defn = r"\gls{" + defn + "}"
            else:
                defn = sub_line(entry[1][0], regexmap, GLSlist)
        new_result.append((acr, (defn, type)))

    return new_result


def loadGLSlist():
    """Load all the glossary items from the generated glossary file.
    we can then use those entries to go back and search for them in the
    tex files to see of they have \\gls"""

    with open(glsFile, "r") as fin:
        # match gls entry but only take the first group
        regex = re.compile(r"\\new.+\s*{(.+)}\s*{.+}\s*")
        text = fin.read()
        GLSlist = set(regex.findall(text))
    return GLSlist


def glsfn(s):
    """put \\gls{} -- used in the regexp substitution"""
    return s.group(1) + "\\gls{" + s.group(2) + "}" + s.group(3)


def make_regexmap(GLSlist):
    """Make a re map of regexps for substitution"""
    regexmap = {}
    for g in GLSlist:
        regexmap[g] = re.compile(r"([,\s(](?<!={))(" + g + r")(\b)")
    return regexmap


def sub_line(line, regexmap, GLSlist):
    r"""for given line put \gls around gls items not already adorned.
    :return: modified line
    """
    nline = line
    for g in GLSlist:
        regx = regexmap[g]
        res = regx.search(line)
        if res is not None:  # ok now .. more checks
            # check its not a word in a GLS item but not
            # too greedy
            glsed = re.search(r"gls{.+" + g + "[a-z,A-Z, ]*}", line)
            if not glsed:  # already glsed or contained in one
                # .. find and add \gls -
                nline = regx.sub(glsfn, line)
    return nline


def updateFile(inFile, GLSlist):
    """Update the tex file by looking for acronyms
    and glossary items GLSlist."""
    newf = inFile
    oldf = newf.replace(".tex", ".tex.old")
    os.rename(newf, oldf)
    regexmap = make_regexmap(GLSlist)
    try:
        with open(oldf, "r") as fin, open(newf, "w") as fout:
            for line in fin:
                if not (
                    line.startswith("%")
                    or "entry" in line
                    or "seciton" in line
                    or "title" in line
                    or "author" in line
                ):  # it is a comment ignore
                    line = sub_line(line, regexmap, GLSlist)
                fout.write(line)
    except BaseException:
        print("Reverting File  because  error:", sys.exc_info()[0])
        os.rename(oldf, newf)
        sys.exit(1)


def update(texfiles):
    """Update the passed tex files by looking for acronyms and glossary items
    loaded from aglossary.tex."""

    if not texfiles:
        raise RuntimeError("No files supplied.")

    print("Updating texfiles the original files will be .old ")
    print(
        """If glossary items contain \\gls refs you may need to run this
              again to catch the entries in aglossary.tex """
    )
    GLSlist = loadGLSlist()  # Grab all the found glossary and acronyms
    for f in texfiles:
        # in each file look for each glossary item and replace wit \gls{item}
        updateFile(f, GLSlist)


def load_translation(locale, filename):
    """load a translation file for given locale
    simplistic for now - append local to file name
    load in a dict assume acronynm, definition, [tag].
    We need to use the tag for overloaded acronyms.
    This will also check for repeat acronym without tag"""

    transfile = filename.replace(".csv", f"_{locale}.csv")
    translation = {}
    with open(transfile, "r") as fd:
        reader = csv.reader(fd, delimiter=",", quotechar='"')
        for lc, row in enumerate(reader):
            try:
                ind = 0
                acr = escape_for_tex(row[ind])
                defn = escape_for_tex(row[ind + 1])
                tag = ""
                # if there is a tag its overloaded - so make a map of tags to defns
                if len(row) > 2:
                    tag = row[ind + 2]
                if tag:
                    trans = {}
                    if acr in translation:
                        trans = translation[acr]
                    if tag in trans:
                        raise ValueError(
                            f"Duplicate tag {tag} for {acr} in {transfile} line {lc}"
                        )
                    trans[tag] = defn
                    translation[acr] = trans
                else:
                    if acr in translation:
                        raise ValueError(
                            f"Duplicate translation for {acr} in {transfile} line {lc} without tag"
                        )
                    translation[acr] = defn
            except BaseException as ex:
                print("Error reading {} on line {} - {}".format(transfile, lc, row))
                raise ex
    return translation


def dump_gls(filename, out_file):
    """Read the definition file and just output a latex table,
    include spanish where available and also do that for a csv to
    be used on the glossary page."""

    sep = " & "
    end = r" \\"
    lc = 0
    translate = load_translation("es", filename)
    gfile = "htmlglossary.csv"
    fullgloss = "fullgls.tex"
    with open(filename, "r") as fd:
        reader = csv.reader(fd, delimiter=",", quotechar='"')
        with open(out_file, "w") as ofd, open(gfile, "w") as ogfile, open(
            fullgloss, "w"
        ) as fg:
            print(
                r"""\addtocounter{table}{-1}
            \begin{longtable}{p{0.15\textwidth}p{0.7\textwidth}p{0.15\textwidth}}\hline
            \textbf{Entry} & \textbf{Description} & \textbf{Tags}  \\\hline
            """,
                file=ofd,
            )
            for row in reader:
                try:
                    lc = lc + 1
                    if len(row) < 6:  # now strict no blanks and 6 cols
                        raise ValueError("Too few columns.")
                    if len(row) > 6:  # now strict no blanks and 6 cols
                        raise ValueError("Too many columns.")
                    if lc == 1:
                        continue  # There is a header line
                    ind = 0
                    acr = row[ind]
                    # put every glossary entry in a file.. unless it has an odd char
                    # AI&T seems ok as acronym breaks glossary
                    if not specialCharsRe.search(acr):
                        print(f"\\gls{{{acr}}}", file=fg)
                    defn = escape_for_tex(row[ind + 1])
                    tags = row[ind + 2]
                    trans = None
                    if acr in translate:
                        # it may be a map of tags
                        transm = translate[acr]
                        if type(transm) is dict:
                            # The TAG is the key if it's set up properly
                            if tags in transm:
                                trans = transm[tags]
                            else:
                                print(
                                    f"Warning: {tags} not in {transm.keys()}  for {acr}"
                                )
                                k = transm.keys()[0]
                                trans = transm[k]
                        else:  # it is a simple string
                            trans = translate[acr]
                    if "," in acr:
                        csv_acr = f'"{acr}"'
                    else:
                        csv_acr = acr
                    print(",".join([csv_acr, f'"{defn}"', tags]), file=ogfile)
                    if trans:
                        trans = escape_for_tex(trans)
                        print(",".join([acr, f'"{trans}"', f"{tags}"]), file=ogfile)
                        defn = defn + "\n\n" + escape_for_tex(trans)
                    print(sep.join([acr, defn, tags]) + end, file=ofd)
                except BaseException as ex:
                    print("Error reading {} on line {} - {}".format(filename, lc, row))
                    raise ex
            print(r"\end{longtable}", file=ofd)
    return lc


if __name__ == "__main__":
    description = __doc__
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)

    parser.add_argument("files", metavar="FN", nargs="+", help="FILE to process")
    parser.add_argument(
        "-g",
        "--glossary",
        action="store_true",
        help=""" Generate aglossary.tex a glossary file for
                                 acronyms and glossary entries.""",
    )
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="""Update files to put \\gls on acronyms and
                                glossary entries .""",
    )
    parser.add_argument(
        "-m",
        "--mode",
        default="tex",
        choices=OUTPUT_MODES,
        help="""Output mode for table.
                                verbose' displays all the information...""",
    )
    parser.add_argument(
        "-t",
        "--tags",
        help="""Space separated list of tags between quotes
                                to use in selecting definitions.""",
    )
    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="""Check the glossary file loads correctly
                                 to run on push. Pass dummy filename""",
    )
    parser.add_argument(
        "-n",
        "--noadorn",
        action="store_true",
        help=r"""Do not adorn the glossary/acronym entries
                                 with \gls (only done for glossary mode)""",
    )
    parser.add_argument(
        "-d",
        "--dump",
        action="store_true",
        help=""" Generate glossary dump file using passed
                                 filename containing  all entries.""",
    )
    parser.add_argument(
        "-s",
        "--skipnone",
        action="store_true",
        help=""" Do not load skip acronyms file""",
    )
    args = parser.parse_args()
    doGlossary = args.glossary
    doCheck = args.check
    skipnone = args.skipnone

    texfiles = args.files
    tagstr = args.tags
    utags = set()
    dotex = args.mode == "tex"
    dorst = args.mode == "rst"
    noadorn = args.noadorn

    if args.dump:
        # just format the full list in a table
        dump_gls(setup_paths()[0], texfiles[0])
        print("Dumped glossary defs to", texfiles[0])
        exit(0)

    if tagstr:
        utags.update(tagstr.split())

    if doCheck:
        # For now load the glossary .. see if we get an excpetion
        # return appropriate exit code to make ci pass or fail
        # also dump all entries to file so we can make a pdf outside
        status = 0
        try:
            dump_gls(setup_paths()[0], texfiles[0])
        except BaseException as ex:
            status = 1
            print(f"Exception:{ex}")
        exit(status)

    if doGlossary or (not args.update):
        # Allow update to really just update/rewrite files not regenerate
        # glossary
        count = main(
            texfiles, doGlossary, utags, dotex, dorst, args.mode, noadorn, skipnone
        )
        if doGlossary and dotex:
            forceConverge(count, utags, noadorn, skipnone)
    # Go through files on second pass  or on demand and \gls  or not (-u)
    if args.update:
        update(texfiles)
