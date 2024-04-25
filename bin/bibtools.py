"""Representation of a bibtex bibentry.

It can construct from a string and output to the bib file as needed.
It is comparable hence sortable.
"""

import collections.abc
import sys

import pybtex.database

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

    def __init__(
        self,
        author=None,
        title=None,
        month=None,
        handle=None,
        year=None,
        note="",
        url="",
        publisher="",
    ):
        self.author = author
        self.title = title
        self.month = month
        self.handle = handle
        self.note = note
        self.url = url
        self.year = year
        self.type = "@Misc"
        self.publisher = publisher

        if "" == note and handle:
            prefix, _ = self.handle.split("-", 1)
            series = TN_SERIES.get(prefix, "")
            self.note = f"Vera C. Rubin Observatory {series} {self.handle}"

    def get_pybtex(self) -> pybtex.database.Entry:
        """Retrieve the entry in standard pybtex form."""
        return pybtex.database.Entry.from_string(self._form_bib_entry_string(), "bibtex")

    def __str__(self) -> str:
        """Return entry as bibtex string."""
        return self.get_pybtex().to_string("bibtex")

    def write_latex_bibentry(self, fd=sys.stdout):
        """Write a bibentry for document info passed.

        Parameters
        ----------
        fd : `typing.IO`, optional
            File to write to. Defaults stdout.
        """
        print(str(self), file=fd)

    def _form_bib_entry_string(self) -> str:
        """Return the internal string form of the bib entry.

        This is not yet normalized by pybtex.
        """
        return f"""{self.type}{{{self.handle},
            author = {{{self.author}}},
             title = "{{{self.title}}}",
         publisher = "{{{self.publisher}}}",
              year = {self.year},
             month = {self.month},
            handle = {{{self.handle}}},
              note = "{{{self.note}}}",
              url = {{{self.url}}}
        }}
        """

    def __eq__(self, other):
        ret = True
        ret = ret and self.handle == other.handle
        ret = ret and (self.author.strip() == other.author.strip())
        ret = ret and (self.title.strip() == other.title.strip())
        ret = ret and (self.publisher.strip() == other.publisher.strip())
        ret = ret and self.month == other.month
        ret = ret and (self.note.strip() == other.note.strip())
        # this fails no idea why ret = ret and (self.url == other.url)
        ret = ret and (self.year == other.year)
        ret = ret and (self.type.strip() == other.type.strip())

        return ret

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        # sorting on handles only
        return self.handle < other.handle

    def __le__(self, other):
        return self.handle <= other.handle

    def __gt__(self, other):
        return self.handle > other.handle

    def __ge__(self, other):
        return self.handle >= other.handle


class BibDict(collections.abc.MutableMapping):
    """BibTeX compatible dictionary.

    Keys are case insensitive but the original case is preserved. This allows
    DMTN-056 and dmtn-056 to be treated as identical keys without changing
    the key that was originally given.

    Does not support constructor parameters.
    """

    def __init__(self):
        self._dict = {}

    def __contains__(self, key):
        return key.lower() in self._dict

    def __getitem__(self, key):
        return self._dict[key.lower()]["val"]

    def __setitem__(self, key, value):
        self._dict[key.lower()] = {"key": key, "val": value}

    def __delitem__(self, key):
        del self._dict[key.lower()]

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        for kv in self._dict.values():
            yield kv["key"]
