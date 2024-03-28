import re
import unittest
from io import StringIO

from bibtools import BibEntry

TESTENTRY = """@Misc{DMTN-005,
      author = {Testy McTest},
       title = "{A great title}",
   publisher = "{test pub}",
        year = 2001,
       month = nov,
      handle = {DMTN-005},
        note = {NO note},
         url = {http://nolplace.com} }"""


def make_comparable(instr):
    return re.sub(r"\s+", "", instr)


class TestBib(unittest.TestCase):
    be = BibEntry(
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
        bestr = ""
        file = StringIO(bestr)
        TestBib.be.write_latex_bibentry(file)
        bestr = make_comparable(file.getvalue())
        ctest = make_comparable(TESTENTRY)
        self.assertEqual(bestr, ctest)

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
        self.assertTrue(beg.handle > TestBib.be.handle)
        self.assertTrue(bel.handle < TestBib.be.handle)
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
