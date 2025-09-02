"""Representation of a bibtex bibentry.

It can construct from a string and output to the bib file as needed.
It is comparable hence sortable.
"""

import collections.abc
import posixpath
import sys
import urllib.parse
from typing import IO, Any, NamedTuple

import pybtex.database

TN_SERIES = {
    "DMTN": "Data Management Technical Note",
    "RTN": "Technical Note",
    "PSTN": "Project Science Technical Note",
    "SCTR": "Commissioning Technical Report",
    "SITCOMTN": "Commissioning Technical Note",
    "SMTN": "Simulations Team Technical Note",
    "SQR": "SQuaRE Technical Note",
    "ITTN": "Information Technology Technical Note",
    "TSTN": "Telescope and Site Technical Note",
    "DMTR": "Data Management Test Report",
    "LDM": "Data Management Controlled Document",
    "LSE": "Systems Engineering Controlled Document",
    "LCA": "Camera Controlled Document",
    "LTS": "Telescope & Site Controlled Document",
    "LPM": "Project Controlled Document",
    "LEP": "Education and Public Outreach Controlled Document",
    "CTN": "Camera Technical Note",
    "RDO": "Data Management Operations Controlled Document",
    "Agreement": "Formal Construction Agreement",
    "Document": "Informal Construction Document",
    "Publication": "LSST Construction Publication",
    "Report": "Construction Report",
}


def get_ads_bibcode(entry: pybtex.database.Entry) -> str | None:
    """Extract the ADS bibcode from the entry."""
    adsurl = entry.fields.get("adsurl")
    if not adsurl:
        return None

    parsed = urllib.parse.urlparse(adsurl)
    # Old URLs put bibcode in the query params.
    if parsed.query:
        # Sometimes a bib file latex escapes the &.
        qs = parsed.query.replace("\\&", "&")
        parsed_query = urllib.parse.parse_qs(qs)
        bibcode = parsed_query.get("bibcode", [None])[0]
    else:
        bibcode = posixpath.basename(parsed.path)

    # Some old bib files try to escape the % or &
    bibcode = str(bibcode).replace("\\%", "%")
    bibcode = str(bibcode).replace("\\&", "&")
    return urllib.parse.unquote(bibcode) if bibcode else None


class BibEntry:
    """A class to represent a BibEntry
    not all entries have all fields
    """

    def __init__(
        self,
        author: str = "",
        title: str = "",
        month: str = "",
        handle: str = "",
        year: int | None = None,
        note: str = "",
        url: str = "",
        publisher: str = "",
        report_type: str | None = None,
        doi: str | None = None,
    ):
        self.author = author
        self.title = title
        self.month = month
        self.handle = handle
        self.note = note
        self.url = url
        self.year = year
        self.type = "@TechReport"
        self.publisher = publisher
        self.report_type = report_type
        self.doi = doi

        if self.handle and not report_type:
            prefix, _ = self.handle.split("-", 1)
            series = TN_SERIES.get(prefix, "")
            self.report_type = series
            if self.type.lower() == "@misc" and not self.note:
                self.note = f"Vera C. Rubin Observatory {series} {self.handle}"

    def get_pybtex(self) -> pybtex.database.Entry:
        """Retrieve the entry in standard pybtex form."""
        return pybtex.database.Entry.from_string(self._form_bib_entry_string(), "bibtex")

    def __str__(self) -> str:
        """Return entry as bibtex string."""
        return self.get_pybtex().to_string("bibtex")

    def write_latex_bibentry(self, fd: IO | None = sys.stdout) -> None:
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
        if self.note:
            note = f'\n             note = "{{{self.note}}}",'
        else:
            note = ""
        if self.doi:
            doi = f"\n               doi = {{{self.doi}}},"
        else:
            doi = ""
        if self.type.lower() == "@techreport":
            entry = f"""{self.type}{{{self.handle},
                author = {{{self.author}}},
                title = "{{{self.title}}}",
            institution = "{{{self.publisher}}}",
                year = {self.year},
                month = {self.month},
                handle = {{{self.handle}}},
                type = "{{{self.report_type}}}",
                number = {{{self.handle}}},{note}{doi}
                url = {{{self.url}}}
            }}
"""
        else:
            entry = f"""{self.type}{{{self.handle},
            author = {{{self.author}}},
             title = "{{{self.title}}}",
         publisher = "{{{self.publisher}}}",
              year = {self.year},
             month = {self.month},
            handle = {{{self.handle}}},{note}{doi}
              url = {{{self.url}}}
        }}"""
        return entry

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BibEntry):
            return NotImplemented
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

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, BibEntry):
            return NotImplemented
        # sorting on handles only
        return self.handle < other.handle

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, BibEntry):
            return NotImplemented
        return self.handle <= other.handle

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, BibEntry):
            return NotImplemented
        return self.handle > other.handle

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, BibEntry):
            return NotImplemented
        return self.handle >= other.handle


class _BibDictItem(NamedTuple):
    key: str
    value: pybtex.database.Entry


class BibDict(collections.abc.MutableMapping):
    """BibTeX compatible dictionary.

    Keys are case insensitive but the original case is preserved. This allows
    DMTN-056 and dmtn-056 to be treated as identical keys without changing
    the key that was originally given.

    Does not support constructor parameters.
    """

    def __init__(self) -> None:
        self._dict: dict[str, _BibDictItem] = {}

    def __contains__(self, key: Any) -> bool:
        return key.lower() in self._dict

    def __getitem__(self, key: str) -> pybtex.database.Entry:
        return self._dict[key.lower()].value

    def __setitem__(self, key: str, value: pybtex.database.Entry) -> None:
        self._dict[key.lower()] = _BibDictItem(key=key, value=value)

    def __delitem__(self, key: str) -> None:
        del self._dict[key.lower()]

    def __len__(self) -> int:
        return len(self._dict)

    def __iter__(self) -> collections.abc.Iterator[str]:
        for kv in self._dict.values():
            yield kv.key
