import re
import unittest

import pybtex.database
from bibtools import BibEntry

TESTENTRY = """@Misc{DMTN-005,
      author = {Testy McTest},
       title = "{A great title}",
   publisher = "{test pub}",
        year = 2001,
       month = nov,
      handle = {DMTN-005},
        note = "{NO note}",
         url = {http://nolplace.com} }"""


def make_comparable(instr):
    """Remove whitespace."""
    return re.sub(r"\s+", "", instr)


class TestBib(unittest.TestCase):
    """Test bib entries."""

    def setUp(self):
        self.be = BibEntry(
            "Testy McTest",
            "A great title",
            "nov",
            "DMTN-005",
            2001,
            "NO note",
            "http://nolplace.com",
            "test pub",
        )

    def testConstructPrint(self):
        ref_bib = pybtex.database.BibliographyData.from_string(TESTENTRY, "bibtex")
        ref_entry = ref_bib.to_string("bibtex")

        entry = str(self.be)

        self.assertEqual(entry, ref_entry)

    def testCompare(self):
        bel = BibEntry(
            "Testy McTest",
            "A great title",
            "nov",
            "DMTN-003",
            2001,
            "NO note",
            "http://nolplace.com",
        )
        beg = BibEntry(
            "Testy McTest",
            "A great title",
            "nov",
            "DMTN-006",
            2001,
            "NO note",
            "http://nolplace.com",
        )

        #  why does this fail self.assertGreater(beg,TestBib.be)
        self.assertTrue(beg.handle > self.be.handle)
        self.assertTrue(bel.handle < self.be.handle)
        self.assertEqual(bel, bel)
        # same entry bunch of spaces..
        bels = BibEntry(
            " Testy McTest ",
            "   A great title",
            "nov",
            "DMTN-003",
            2001,
            "NO note",
            "http:://nolplace.com",
        )
        self.assertEqual(bels, bel)
        self.assertFalse(bel == beg)


if __name__ == "__main__":
    unittest.main()
