import unittest
from bibtools import BibEntry
from io import StringIO
import re

TESTENTRY = """@DocuShare{DMTN-NN,
   author = {Testy McTest},
    title = "{A great title}",
     year = 2001,
    month = nov,
   handle = {DMTN-NN},
     note = {NO note},
      url = {http://nolplace.com} }"""


def make_comparable(str):
    return re.sub(r"\s+", "", str)


class TestBib(unittest.TestCase):

    def testConstructPrint(self):
        be = BibEntry("Testy McTest", "A great title", "nov", "DMTN-NN",
                      2001, "NO note", "http://nolplace.com")
        bestr = ""
        file = StringIO(bestr)
        be.write_latex_bibentry(file)
        bestr = make_comparable(file.getvalue())
        ctest = make_comparable(TESTENTRY)
        self.assertEqual(bestr, ctest)


if __name__ == "__main__":
    unittest.main()
