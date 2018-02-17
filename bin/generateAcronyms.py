#!/usr/bin/env python3

"""
Utility that can be used to generate automatically the Acronyms of
multiple TeX files, it reads the known acronyms from the Web and the
"myacronyms.tex" and "skipacronyms.tex" files if exist and generates a
"acronyms.tex" that can be included in the document
"""
import warnings
import os.path
import sys
import re


def read_gaia(filename):
    """Read Gaia format glossary.txt file.

    Parameters
    ----------
    filename : `str`
        Path to Gaia format file.

    Returns
    -------
    acronyms : `dict`
        Dictionary with the acronyms as keys. The values are sets containing
        one or more definition associated with that acronym.
        Empty dict if the file can not be opened.
    """
    definitions = {}

    with open(filename, "r") as fd:
        for line in fd:
            line = line.strip()
            if ' : ' not in line:
                continue

            acr, defn = line.split(":", maxsplit=1)
            acr = acr.strip()
            defn = defn.strip()

            if acr not in definitions:
                definitions[acr] = set()

            definitions[acr].add(defn)

    return definitions


def read_myacronyms(filename="myacronyms.tex", defaults=None):
    """Read the supplied file and extract standard acronyms.

    File must contain lines in format:

    ACRYONYM:Definition

    A warning is issued if a duplicate identical definition is found.
    It is an error for the same acronym to have multiple differing entries.

    Parameters
    ----------
    file_name
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
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):  # comment
                continue

            acr, defn = line.split(":", maxsplit=1)
            acr = acr.strip()
            defn = defn.strip()

            if acr in definitions:
                if defn != definitions[acr]:
                    raise RuntimeError("Duplicate definitions of {} differ".format(acr))
                else:
                    warnings.warn(UserWarning("Entry {} exists multiple times with same"
                                              " definition".format(acr)))

            definitions[acr] = defn

    # Merge with the defaults
    if defaults is None:
        combined = definitions
    else:
        combined = defaults.copy()
        combined.update(definitions)

    return combined


def read_skip_acronyms(file_name="skipacronyms.tex"):
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


def find_matches(filename, acronyms, ignore_str=" %"):
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

    return matches


def find_matches_f(filename, acronyms, ignore_str=" %"):
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
    """

    pattern = r"\b(" + "|".join(re.escape(w) for w in acronyms) + r")\b"
    regex = re.compile(pattern)

    lines = []
    with open(filename, "r") as fd:
        for line in fd:
            if ignore_str:
                posn = line.find(ignore_str)
                if posn > -1:
                    line = line[:posn]
            line = line.strip()
            lines.append(line)

    text = " ".join(lines)
    matches = regex.findall(text)

    return set(matches)


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

    global_acronyms = read_gaia(gaia_glossary_path)
    lsst_defaults = read_myacronyms(lsst_acronyms_path)

    # Augment with the local one
    try:
        local_definitions = read_myacronyms(defaults=lsst_defaults)
    except FileNotFoundError:
        local_definitions = lsst_defaults

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
        if s in global_acronyms:
            global_acronyms.pop(s)

    # Master list of all acronyms
    acronyms = set(global_acronyms.keys()) | set(local_definitions.keys())

    # Scan each supplied tex file looking for the acronym
    matches = set()
    for f in texfiles:
        local_matches = find_matches(f, acronyms)
        matches.update(local_matches)

    print("Matched {} acronyms".format(len(matches)), file=sys.stderr)

    # Attach definitions to matches
    results = []
    for acr in sorted(matches):
        if acr in local_definitions:
            results.append((acr, local_definitions[acr]))
        elif acr in global_acronyms:
            options = global_acronyms[acr]
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
