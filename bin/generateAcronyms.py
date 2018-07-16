#!/usr/bin/env python3

"""
Utility that can be used to generate automatically the Acronyms of
multiple TeX files, it reads the known acronyms from the Web and the
"myacronyms.tex" and "skipacronyms.txt" files if exist and generates a
"acronyms.tex" that can be included in the document
"""
import warnings
import os.path
import sys
import re

try:
    import pypandoc
except ImportError:
    pypandoc = None

MATCH_ACRONYM = "^([\w/&\-\+]+)\s*:\s*(.*)$"
MATCH_ACRONYM_RE = re.compile(MATCH_ACRONYM)


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
    return (acr, defn)


def read_definitions(filename, init=None):
    """Read acronym definitions from Gaia format glossary.txt file.

    Parameters
    ----------
    filename : `str`
        Path to Gaia format file.
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

    with open(filename, "r") as fd:
        for line in fd:

            acr, defn = _parse_line(line)
            if acr is None:
                continue

            if acr not in definitions:
                definitions[acr] = set()

            definitions[acr].add(defn)

    return definitions


def read_myacronyms(filename="myacronyms.txt", allow_duplicates=False, defaults=None):
    """Read the supplied file and extract standard acronyms.

    File must contain lines in format:

    ACRYONYM:Definition

    A warning is issued if a duplicate identical definition is found.
    It is an error for the same acronym to have multiple differing entries.

    Parameters
    ----------
    file_name : `str`
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

    with open(filename, "r") as fd:
        for line in fd:
            acr, defn = _parse_line(line)
            if acr is None:
                continue

            if acr in definitions:
                if defn != definitions[acr]:
                    raise RuntimeError("Duplicate definitions of {} differ in {}".format(acr, filename))
                else:
                    warnings.warn(UserWarning("Entry {} exists multiple times with same"
                                              " definition in {}".format(acr, filename)))

            definitions[acr] = defn

    # Merge with the defaults
    if defaults is None:
        combined = definitions
    else:
        combined = defaults.copy()
        combined.update(definitions)

    return combined


def read_skip_acronyms(file_name="skipacronyms.txt"):
    """Read the supplied file to obtain list of acronyms to skip.

    File must contain lines in format of one word per line. Repeat
    values are ignored.

    Parameters
    ----------
    file_name
        Name of file to open. The file does not need to exist.

    Returns
    -------
    skip : `set`
        Set containing acronyms to be skipped.
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

            if " " in line:
                warnings.warn(UserWarning("Entry '{}' contains a space. Ignoring it for"
                                          " skip list".format(line)))
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
                if (line.startswith(r"\def") or line.startswith(r"\newcommand") or
                        line.startswith(r"\renewcommand") or line.startswith("%")):
                    continue
                line = line.replace(r"\&", "&")
                line = line.replace(r"\_", "_")

                lines.append(line)

            text = " ".join(lines)

    # Do two passes. First look for usages of acronyms that have lower
    # case characters, number or special characters.
    # These do not look like "normal" acronyms so special case them.
    # Also single character acronyms (which should probably be banned)
    nonstandard = {a for a in acronyms if not a.isupper() or not a.isalpha() or len(a) == 1}

    # findall matches non-overlapping left to right in the order that
    # we give alternate strings. Therefore when we build the regex
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
    regex = re.compile(r"\b[A-Z][A-Z]+\b")
    used = set(regex.findall(text))

    # For all acronyms that were used and have existing definitions, add
    # them to the current list of matches
    matches.update(used & acronyms)

    # Calculate all the acronyms we found in the text but which do not
    # have definitions.
    missing = used - matches

    return matches, missing


find_matches = find_matches_combo


def write_latex_table(acronyms, fd=sys.stdout):
    """Write latex table to supplied file descriptor.

    Parameters
    ----------
    acronyms : `list`
        List of 2-tuples with acronym and definition.
    """
    print(r"""\addtocounter{table}{-1}
\begin{longtable}{|l|p{0.8\textwidth}|}\hline
\textbf{Acronym} & \textbf{Description}  \\\hline
""", file=fd)
    for acr, defn in acronyms:
        acr = acr.replace("&", r"\&")
        acr = acr.replace("_", r"\_")
        print("{} & {} {}".format(acr, defn, r"\\\hline"), file=fd)

    print(r"\end{longtable}", file=fd)


def main(texfiles):
    """Run program and generate acronyms file."""

    if not texfiles:
        raise RuntimeError("No files supplied.")

    defaults_dir = os.path.join(os.path.dirname(__file__), os.path.pardir, "etc")
    gaia_glossary_path = os.path.join(defaults_dir, "glossary.txt")
    lsst_acronyms_path = os.path.join(defaults_dir, "lsstacronyms.txt")
    global_skip_path = os.path.join(defaults_dir, "skipacronyms.txt")

    # Read the Gaia set
    global_definitions = read_definitions(gaia_glossary_path)

    # Now read the LSST global definitions
    lsst_definitions = read_definitions(lsst_acronyms_path)

    # Merge global with lsst such that LSST overrides.
    # If instead we wish to merge with global, use init kwarg in
    # read_definitions above
    global_definitions.update(lsst_definitions)
    lsst_definitions = global_definitions

    # Read the local set
    try:
        local_definitions = read_myacronyms()
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
                print("Entry {} exists multiple ({}) times. "
                      "Including all definitions.".format(acr, len(options)),
                      file=sys.stderr)
            for a in options:
                results.append((acr, a))
        else:
            raise RuntimeError("Internal error handling {}".format(acr))

    with open("acronyms.tex", "w") as fd:
        write_latex_table(results, fd=fd)


if __name__ == "__main__":
    texfiles = sys.argv
    texfiles.pop(0)
    main(texfiles)
