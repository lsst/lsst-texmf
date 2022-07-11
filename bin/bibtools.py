"""This class represents a bibtex bibentry.
it can construct from a string and output to the bib file as needed.
it is comparable hence sortable.
"""

import sys

TN_SERIES = {
    "DMTN": "Data Management Technical Note",
    "RTN": "Technical Note",
    "PSTN": "Project Science Technical Note",
    "SCTR": "Commissioning Technical Report",
    "SITCOMTN": "Commissioning Technical Note",
    "SMTN": "Simulations Team Technical Note",
    "SQR": "SQuaRE Technical Note",
    "DMTR": "Data Management Test Report",
    "LDM": "Data Management Controlled Document",
}


class BibEntry:
    """A class to represent a BibEntry
    not all entries have all fields
    """

    def __init__(self, author=None, title=None, month=None, handle=None, year=None, note="", url=""):
        self.author = author
        self.title = title
        self.month = month
        self.handle = handle
        self.note = note
        self.url = url
        self.year = year
        self.type = "@DocuShare"
        if "" == note and handle:
            prefix, _ = self.handle.split("-", 1)
            series = TN_SERIES.get(prefix, "")
            self.note = f"{{Vera C. Rubin Observatory {series}}}"

    def write_latex_bibentry(self, fd=sys.stdout):
        """ Write a bibentry for document info passed.
        Parameters
        ----------
        fd : default stdout : file to write to
        """

        print("{}{{{},".format(self.type, self.handle), file=fd)
        print("   author = {{{}}},".format(self.author), file=fd)
        print('    title = "{{{}}}",'.format(self.title), file=fd)
        print("     year = {},".format(self.year), file=fd)
        print("    month = {},".format(self.month), file=fd)
        print("   handle = {{{}}},".format(self.handle), file=fd)
        print("     note = {{{}}},".format(self.note), file=fd)
        print("      url = {{{}}} }}".format(self.url), file=fd)
