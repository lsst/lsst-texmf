#!/usr/bin/env python3

"""
Load the author list and database from the support directory and
convert it to an author tex file using AASTeX6.1 syntax.

  python3 db2authors.py > authors.tex

The list of authors for the paper should be defined in a authors.yaml
file in the current working directory.  This YAML file contains a
sequence of author IDs matching the keys in the author database
file in the etc/authordb.yaml file in this package.

This program requires the "yaml" package to be installed.

"""

import argparse
import dataclasses
import os.path
import re
import string
import sys
from _collections_abc import dict_keys
from abc import ABC, abstractmethod
from typing import Any, Self

import yaml


def latex2text(latex: str) -> str:
    """Convert a LaTeX string into a plain text string.

    Parameters
    ----------
    latex : `str`
        Latex string to convert.

    Returns
    -------
    plain : `str`
        The plain text version.
    """
    from pylatexenc.latex2text import LatexNodes2Text

    return LatexNodes2Text().latex_to_text(latex)


@dataclasses.dataclass(frozen=True)
class Author:
    """Representation of an author."""

    given_name: str
    family_name: str
    email: str
    orcid: str | None
    affiliations: list[str]
    altaffil: list[str]

    @property
    def full_name(self) -> str:
        """Return full name with spaces and no latex."""
        latex_name = self.full_latex_name
        return latex2text(latex_name)

    @property
    def full_latex_name(self) -> str:
        """Return full name with latex spaces."""
        if not self.given_name:
            full = self.family_name
        else:
            full = f"{self.given_name}~{self.family_name}"
        return full.replace(" ", "~")

    @property
    def latex_name_then_initials(self) -> str:
        """Return Given Name, Initials"""
        if not self.given_name:
            initials = ""
        else:
            initials = ", " + self.initials
        return f"{self.family_name}{initials}".replace(" ", "~")

    @property
    def initials_latex_name(self) -> str:
        """Return full name but using initials for given name."""
        if not self.given_name:
            full = self.family_name
        else:
            full = f"{self.initials}~{self.family_name}"
        return full.replace(" ", "~")

    @property
    def initials(self) -> str:
        """Return initials instead of full given name.

        Notes
        -----
        G. Mark -> G. M.
        Kian-Tat -> K-T.
        """
        if not self.given_name:
            # Non-human collaboration.
            return ""
        initials = []
        # Split on whitespace, latex space ~.
        for name in re.split(r"[\s\~]", self.given_name):
            if "-" in name:
                parts = name.split("-")
                sub_initials = [c[0] for c in parts]
                initials.append("-".join(sub_initials))
            else:
                initials.append(name[0])
        return ". ".join(initials) + "."


class AuthorFactory:
    """Extract author information from author database."""

    def __init__(
        self, affiliations: dict[str, str], email_domains: dict[str, str], authors: dict[str, Any]
    ) -> None:
        self._affiliations = affiliations
        self._email_domains = email_domains
        self._authors = authors

    @classmethod
    def from_authordb(cls, authordb: dict[str, Any]) -> Self:
        return cls(
            affiliations=authordb["affiliations"],
            email_domains=authordb["emails"],
            authors=authordb["authors"],
        )

    def get_author_ids(self) -> dict_keys:
        return self._authors.keys()

    def get_affiliation_ids(self) -> dict_keys:
        return self._affiliations.keys()

    def get_email_domains(self) -> dict:
        return self._email_domains

    def get_affiliation(self, affiliationid: str) -> str:
        return str(self._affiliations.get(affiliationid))

    def get_author(self, authorid: str) -> Author:
        if authorid not in self._authors:
            raise RuntimeError(f"Author {authorid!r} not found in author database")
        author = self._authors[authorid]

        affiliations = []
        for affil in author["affil"]:
            affiliation = self._affiliations.get(affil)
            if not affiliation:
                raise RuntimeError(f"Author {authorid!r} refers to affiliation {affil} that is not known.")
            affiliations.append(affiliation)

        # email is a bit more involved.
        email = author.get("email", "")
        if "@" in email:
            username, domain = email.split("@", 1)
        else:
            username = email
            domain = author["affil"][0]  # Key to look up in email domains
        if "." not in domain:
            # This is a key to a email domain.
            domain = self._email_domains.get(domain)

        # In theory should only warn if this is AAS but we do not know the
        # mode here.
        if (not domain or not username) and author["affil"][0] != "_":
            # Only warn if we need the email.
            print(
                f"WARNING: Unable to resolve email address for author '{authorid}' email '{email}'",
                file=sys.stderr,
            )
        if not domain:
            domain = "none.com"
        if not username:
            username = "unknown"
        email = f"{username}@{domain}"

        return Author(
            given_name=author["initials"],
            family_name=author["name"],
            orcid=author.get("orcid"),
            email=email,
            affiliations=affiliations,
            altaffil=list(author["altaffil"]),
        )


class AuthorTextGenerator(ABC):
    """Class to create some text for authors."""

    mode: str = "undefined"

    def __init__(self, authors: list[Author]) -> None:
        self.authors = authors

    def get_header(self) -> str:
        return f"""%% DO NOT EDIT THIS FILE. IT IS GENERATED FROM db2authors.py"
%% Regenerate using:
%%    python $LSST_TEXMF_DIR/bin/db2authors.py -m {self.mode}

"""

    def number_affiliations(self) -> dict[str, int]:
        """Assign number to each affiliation."""
        # Affiliations found so far.
        affil_to_number = {}
        counter = 0
        for author in self.authors:
            for affiliation in author.affiliations:
                if affiliation not in affil_to_number:
                    counter += 1
                    affil_to_number[affiliation] = counter

        return affil_to_number

    @classmethod
    def parse_affiliation(cls, affiliation: str) -> dict[str, str]:
        """Given a mailing address, try to parse it.

        Would be better for authordb affiliations to be pre-parsed.
        """
        addr = [a.strip() for a in affiliation.split(",")]
        # We have a problem with departments in affiliations.
        # Until we have proper Affiliation object we have to kluge things
        # and try to spot when departments are involved in addition to the
        # institute.
        combined_institutes: list[str] = []
        combining = True
        modified: list[str] = []
        for a in addr:
            if combining:
                if "Dep" in a or "Faculty" in a:
                    combined_institutes.append(a)
                    continue
                else:
                    # Run of out of departments. Merge with the next and then
                    # disable combinations.
                    combined_institutes.append(a)
                    a = ", ".join(combined_institutes)
                    combining = False
            modified.append(a)
        addr = modified

        institute = addr[0]
        ind = len(addr) - 1
        state = ""
        pcode = ""
        country = ""
        if ind > 0:
            country = addr[ind]
            ind = ind - 1
        if ind > 0:
            sc = addr[ind].split()
            ind = ind - 1
            state = sc[0]
            pcode = ""
            if len(sc) == 2:
                pcode = sc[1]
        city = ""
        if ind > 0:
            city = addr[ind]
        return {"institute": institute, "city": city, "country": country, "state": state, "postcode": pcode}

    @abstractmethod
    def generate(self) -> str:
        """Generate the author text.

        Returns
        -------
        author_text : `str`
            The text in the expected format.
        """
        raise NotImplementedError()


class AASTeX(AuthorTextGenerator):
    """AASTeX specific generation."""

    mode = "aas"

    def generate(self) -> str:
        """Generate AASTeX format."""
        lines = []
        for author in self.authors:
            lines.append("")
            orcid = f"[{author.orcid}]" if author.orcid else ""
            lines.append(rf"\author{orcid}{{{author.full_latex_name}}}")
            for alt in author.altaffil:
                lines.append(rf"\altaffiliation{{{alt}}}")
            for affil in author.affiliations:
                lines.append(rf"\affiliation{{{affil}}}")
            lines.append(rf"\email{{{author.email}}}")

        return self.get_header() + "\n".join(lines)


class LsstDoc(AuthorTextGenerator):
    """LaTeX lsstdoc tech notes."""

    mode = "lsstdoc"

    def generate(self) -> str:
        authors = list(self.authors)
        last = authors.pop()

        # Join with "," until last author joins with "and"
        lines = [f"{author.full_latex_name}," for author in authors]
        if lines:
            lines.append("and")
        lines.append(last.full_latex_name)

        return self.get_header() + "\\author{\n" + "\n".join(lines) + "\n}"


class Arxiv(AuthorTextGenerator):
    """Generate ArXiv format.

    Authors: Author One (1), Author Two (1 and 2), Author Three (2)
       ((1) Institution One, (2) Institution Two)
    """

    mode = "arxiv"

    def generate(self) -> str:
        """Generate ArXiv format."""
        affil_to_number = self.number_affiliations()

        author_text = []
        for author in self.authors:
            affil_numbers = [str(affil_to_number[affil]) for affil in author.affiliations]
            author_text.append(f"{author.full_name} ({' and '.join(affil_numbers)})")

        institutions = []
        for affil, number in affil_to_number.items():
            parsed = self.parse_affiliation(affil)
            institutions.append(f"({number}) {latex2text(parsed['institute'])}")

        return f"Authors: {', '.join(author_text)}\n       ({', '.join(institutions)})"


class ProcSpie(AuthorTextGenerator):
    r"""SPIE proceedings.

    \author[a]{Anna A. Author}
    \author[a,b]{Barry B. Author}
    \affil[a]{Affiliation1, Address, City, Country}
    \affil[b]{Affiliation2, Address, City, Country}

    """

    mode = "spie"

    def generate(self) -> str:
        affil_to_number = self.number_affiliations()
        chars = string.ascii_lowercase + string.ascii_uppercase

        # SPIE prefers labels over numbers, so convert affiliation numbers
        # to labels but once we have more than the number of letters we switch
        # back to numbers.
        affil_to_label = {}
        label_counter = 1
        for affil, number in affil_to_number.items():
            # Offset from affiliation number into an array index.
            char_index = number - 1
            if char_index < len(chars):
                label = chars[char_index]
            else:
                label = str(label_counter)
                label_counter += 1
            affil_to_label[affil] = label

        authors = []
        for author in self.authors:
            labels = [affil_to_label[affil] for affil in author.affiliations]
            authors.append(rf"\author[{','.join(labels)}]{{{author.full_latex_name}}}")

        affiliations = []
        for affil, label in affil_to_label.items():
            affiliations.append(rf"\affil[{label}]{{{affil}}}")

        return self.get_header() + "\n".join(authors + affiliations)


class WebOfC(AuthorTextGenerator):
    """WebOfC generator."""

    mode = "webofc"

    def generate(self) -> str:
        affil_to_number = self.number_affiliations()

        authors = []
        for author in self.authors:
            author_text = rf"\firstname{{{author.given_name}}} \lastname{{{author.family_name}}}"
            affil_numbers = [affil_to_number[affil] for affil in author.affiliations]
            author_text += " " + " ".join(rf"\inst{{{n}}}" for n in affil_numbers)
            if author.orcid:
                author_text += rf" \orcidlink{{{author.orcid}}}"
            authors.append(author_text)

        # The dict is ordered correctly by default.
        affiliations = " \\and\n".join(affil_to_number)

        return (
            self.get_header()
            + "\\author{\n"
            + " \\and\n".join(authors)
            + "\n}\n\\institute{\n"
            + affiliations
            + "\n}"
        )


class ASCOM(AuthorTextGenerator):
    """Astronomy and Computing."""

    mode = "ascom"

    def generate(self) -> str:
        """Generate A&C format."""
        affil_to_number = self.number_affiliations()

        authors = []
        for author in self.authors:
            affil_numbers = [str(affil_to_number[affil]) for affil in author.affiliations]
            author_text = f"\\author[{','.join(affil_numbers)}]{{{author.full_latex_name}}}"
            if author.orcid:
                author_text += f"[orcid={author.orcid}]"
            authors.append(author_text)

        affiliations = []
        for affil, number in affil_to_number.items():
            parsed = self.parse_affiliation(affil)
            affil_text = f"""\\affiliation[{number}]{{organization={{{parsed["institute"]}}},
                country={{{parsed["country"]}}}
               }}"""
            affiliations.append(affil_text)

        return self.get_header() + "\n".join(authors) + "\n" + "\n".join(affiliations)


class ADASS(AuthorTextGenerator):
    """Generate ADASS text."""

    mode = "adass"

    @staticmethod
    def _to_affil_text(affil_to_number: dict[str, int], affiliations: list[str]) -> str:
        affil_numbers = [str(affil_to_number[affil]) for affil in affiliations]
        affil_text = " ".join(f"$^{n}$" for n in affil_numbers)
        return affil_text

    def generate(self) -> str:
        affil_to_number = self.number_affiliations()

        authors = list(self.authors)
        last = authors.pop()
        author_lines = []
        for author in authors:
            author_text = author.full_latex_name + ","
            affil_text = self._to_affil_text(affil_to_number, author.affiliations)
            author_lines.append(author_text + affil_text)

        final_and = ""
        if author_lines:
            final_and = "and "
        author_lines.append(
            final_and + last.full_latex_name + self._to_affil_text(affil_to_number, last.affiliations)
        )

        affiliations = []
        for affil, number in affil_to_number.items():
            affiliations.append(f"\\affil{{$^{number}${affil}}}")

        paperauthors = []
        for author in self.authors:
            # Uses primary affiliation.
            parsed = self.parse_affiliation(author.affiliations[0])
            parsed["full_name"] = author.full_latex_name
            parsed["email"] = author.email
            parsed["orcid"] = author.orcid or ""
            paperauthors.append(
                (
                    r"\paperauthor"
                    "{{{full_name}}}{{{email}}}{{{orcid}}}"
                    "{{{institute}}}{{}}{{{city}}}{{{state}}}{{{postcode}}}{{{country}}}"
                ).format(**parsed)
            )

        aindexes = ["%% Must be commented out"]
        for author in self.authors:
            aindexes.append(f"%\\aindex{{{author.latex_name_then_initials}}}")

        return (
            self.get_header()
            + "\\author{"
            + " ".join(author_lines)
            + "}\n"
            + "\n".join(affiliations)
            + "\n"
            + "\n".join(paperauthors)
            + "\n"
            + "\n".join(aindexes)
        )


def dump_csvall(factory: AuthorFactory) -> None:
    """Generate CSV of ALL authors for easier lookup of ID .
    Authorid, Name, Institution id
    put this in authors.csv
    """
    author_ids = factory.get_author_ids()
    with open("authors.csv", "w") as outf:
        print("Rubin ID, Name, Affiliation(s)", file=outf)
        for authorid in author_ids:
            author = factory.get_author(authorid)
            affils = " | ".join(author.affiliations)
            line = f'{authorid},{latex2text(author.full_name)},"{latex2text(affils)}"'
            print(line, file=outf)
    affil_ids = factory.get_affiliation_ids()
    with open("affiliations.csv", "w") as outf:
        print("ID, Affiliation", file=outf)
        for id in affil_ids:
            affil = factory.get_affiliation(id)
            line = f'{id},"{latex2text(affil)}"'
            print(line, file=outf)


if __name__ == "__main__":
    # There is a file listing all the authors and a file mapping
    # those authors to full names and affiliations

    # This is the author list. It's a yaml file with authorID that
    # maps to the database file below.  For now we assume this file is in
    # the current working directory.
    authorfile = os.path.join("authors.yaml")

    # this should probably be a dict with the value of affil_cmd
    # the keys could then be passed to the arg parser.
    OUTPUT_MODES = ["aas", "spie", "adass", "arxiv", "ascom", "webofc", "lsstdoc", "csvall"]

    description = __doc__
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)

    parser.add_argument(
        "-m",
        "--mode",
        default="aas",
        choices=OUTPUT_MODES,
        help="""Display mode for translated parameters.
                            'verbose' displays all the information...""",
    )
    parser.add_argument("-n", "--noafil", action="store_true", help="""Do not add affil at all for arxiv.""")
    args = parser.parse_args()

    # This is the database file with all the generic information
    # about authors. Locate it relative to this script.
    exedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.normpath(os.path.join(exedir, os.path.pardir, "etc", "authordb.yaml"))

    with open(dbfile) as fh:
        authordb = yaml.safe_load(fh)

    factory = AuthorFactory.from_authordb(authordb)

    if args.mode == "csvall":
        dump_csvall(factory)
        exit(0)

    with open(authorfile) as fh:
        authors = yaml.safe_load(fh)

    authors = [factory.get_author(authorid) for authorid in authors]

    generator_lut: dict[str, type[AuthorTextGenerator]] = {
        "aas": AASTeX,
        "lsstdoc": LsstDoc,
        "arxiv": Arxiv,
        "spie": ProcSpie,
        "webofc": WebOfC,
        "ascom": ASCOM,
        "adass": ADASS,
    }
    if args.mode not in generator_lut:
        raise RuntimeError(f"Unknown generator mode: {args.mode}")

    generator = generator_lut[args.mode](authors)
    print(generator.generate())
