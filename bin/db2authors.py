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
import csv
import io
import os.path
import re
import string
import sys
from _collections_abc import dict_keys
from abc import ABC, abstractmethod
from dataclasses import asdict as dataclass_asdict
from pathlib import Path
from typing import Any, Self, TypeAlias

import yaml

try:
    from typing import Annotated

    from pydantic import BeforeValidator, dataclasses

    def _coerce_str(v: Any) -> str | None:
        if v is None or isinstance(v, str):
            return v
        return str(v)

    # Allow zipcode to be int or str or None.
    OptStr: TypeAlias = Annotated[str | None, BeforeValidator(_coerce_str)]

except ImportError:
    import dataclasses  # type: ignore[no-redef]

    OptStr: TypeAlias = str | None  # type: ignore[no-redef,misc]


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
class Address:
    """Representation of an address."""

    example_expanded: str
    street: str | None = None
    city: str | None = None
    state: str | None = None
    postcode: OptStr = None
    country_code: str | None = None


@dataclasses.dataclass(frozen=True)
class Affiliation:
    """Representation of an affiliation."""

    institute: str
    department: str | None = None
    ror_id: str | None = None
    email: str | None = None
    address: Address | None = None

    def get_department_and_institute(self) -> str:
        """Return department and institute as a single string."""
        if self.department:
            return f"{self.department}, {self.institute}"
        return self.institute

    def get_full_address_with_institute(self) -> str:
        """Return full address as a string."""
        if not self.address:
            return self.get_department_and_institute()

        # For now assume the example_expanded is a string that contains
        # the full address in a format that can be used.
        if self.address.example_expanded:
            # Use the example expanded address.
            return self.address.example_expanded

        # Otherwise, build the address from the parts.
        parts = [self.get_department_and_institute()]
        if self.address.street:
            parts.append(self.address.street)
        if self.address.city:
            parts.append(self.address.city)
        if self.address.state:
            parts.append(self.address.state)
        if self.address.postcode:
            parts.append(self.address.postcode)
        if self.address.country_code:
            parts.append(self.address.country_code)
        return ", ".join(parts)

    def get_city_with_institute(self) -> str:
        """Return institute, city, and country as a string."""
        if not self.address:
            return self.get_department_and_institute()

        parts = [self.get_department_and_institute()]
        if self.address.city:
            parts.append(self.address.city)
        if self.address.state:
            parts.append(self.address.state)
        if self.address.country_code:
            parts.append(self.address.country_code)
        return ", ".join(parts)


@dataclasses.dataclass(frozen=True)
class Author:
    """Representation of an author."""

    given_name: str
    family_name: str
    email: str
    orcid: str | None
    affiliations: list[Affiliation]
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

    def __init__(self, affiliations: dict[str, Any], authors: dict[str, Any]) -> None:
        self._affiliations = affiliations
        self._authors = authors
        self._reverse_affil = {self.get_affiliation(aid): aid for aid in self._affiliations}

    @classmethod
    def from_authordb(cls, authordb: dict[str, Any]) -> Self:
        return cls(
            affiliations=authordb["affiliations"],
            authors=authordb["authors"],
        )

    def get_author_ids(self) -> dict_keys:
        return self._authors.keys()

    def get_affiliation_ids(self) -> dict_keys:
        return self._affiliations.keys()

    def get_affiliation_id(self, affil: Affiliation) -> str:
        return self._reverse_affil[affil]

    def get_affiliation(self, affiliationid: str) -> Affiliation:
        raw_affil = self._affiliations.get(affiliationid)
        if not raw_affil:
            raise RuntimeError(f"Affiliation {affiliationid!r} not found in affiliation database")
        if "address" in raw_affil and raw_affil["address"]:
            address = Address(
                street=raw_affil["address"].get("street"),
                city=raw_affil["address"].get("city"),
                state=raw_affil["address"].get("state"),
                postcode=raw_affil["address"].get("postcode"),
                country_code=raw_affil["address"].get("country_code"),
                example_expanded=raw_affil["address"]["example_expanded"],
            )
        else:
            address = None
        return Affiliation(
            institute=raw_affil["institute"],
            department=raw_affil.get("department"),
            ror_id=raw_affil.get("ror_id"),
            email=raw_affil.get("email"),
            address=address,
        )

    def get_email_domain_from_id(self, domainid: str) -> str:
        """Get email domain from ID.

        This is used to resolve the email address for authors that do not
        have a full email address but only a key to an email domain.
        """
        if domainid not in self._affiliations:
            return ""
        affil = self._affiliations[domainid]
        if not (domain := affil.get("email")):
            return ""
        return domain

    def get_email_domains(self) -> dict[str, str]:
        """Get a dictionary of known email domains."""
        domains = {}
        for affilid, affil in self._affiliations.items():
            if email := affil.get("email"):
                domains[affilid] = email
        return domains

    def get_author(self, authorid: str) -> Author:
        if authorid not in self._authors:
            raise RuntimeError(f"Author {authorid!r} not found in author database")
        author = self._authors[authorid]

        affiliations: list[Affiliation] = []
        for affil in author["affil"]:
            affiliation = self.get_affiliation(affil)
            if not affiliation:
                raise RuntimeError(f"Author {authorid!r} refers to affiliation {affil} that is not known.")
            affiliations.append(affiliation)

        # email is a bit more involved.
        email = author.get("email", "")
        if email and "@" in email:
            username, domain = email.split("@", 1)
        else:
            username = email
            domain = author["affil"][0]  # Key to look up in email domains
        if "." not in domain:
            # This is a key to a email domain.
            domain = self.get_email_domain_from_id(domain)

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
            given_name=author["given_name"],
            family_name=author["family_name"],
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

    def number_affiliations(self) -> dict[Affiliation, int]:
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

    @abstractmethod
    def generate(self, header: bool = True) -> str:
        """Generate the author text.

        Parameters
        ----------
        header : bool, optional
            If True, include the header in the generated text. Default is True.

        Returns
        -------
        author_text : `str`
            The text in the expected format.
        """
        raise NotImplementedError()


class AASTeX(AuthorTextGenerator):
    """AASTeX 6 specific generation."""

    mode = "aas"

    def _generate_paren_text(self, author: Author) -> str:
        r"""Return the text in the square brackets in the author string.

        Parameters
        ----------
        author : `Author`
            The author record.

        Returns
        -------
        text : `str`
            The text to be inserted between ``\author`` and ``{Author A}``.
            For AASTeX7 this can include the ORCiD. Returns "" if there is
            no ORCiD defined.
        """
        return f"[{author.orcid}]" if author.orcid else ""

    def generate(self, header: bool = True) -> str:
        """Generate AASTeX format."""
        lines = []
        for author in self.authors:
            lines.append("")
            # Text depends on aastex 7 vs 6.
            parentext = self._generate_paren_text(author)
            lines.append(rf"\author{parentext}{{{author.full_latex_name}}}")
            for alt in author.altaffil:
                lines.append(rf"\altaffiliation{{{alt}}}")
            for affil in author.affiliations:
                lines.append(rf"\affiliation{{{affil.get_full_address_with_institute()}}}")
            lines.append(rf"\email{{{author.email}}}")

        return (self.get_header() if header else "") + "\n".join(lines)


class AASTeX7(AASTeX):
    """AASTeX v7 specific generation."""

    mode = "aas7"

    def _generate_paren_text(self, author: Author) -> str:
        r"""Return the text in the square brackets in the author string.

        Parameters
        ----------
        author : `Author`
            The author record.

        Returns
        -------
        text : `str`
            The text to be inserted between ``\\author`` and ``{Author A}``.
            For AASTeX7 this can include ORCiD and the sname and gname
            parameters.
        """
        # AASTeX 7 supports
        #  [orcid]
        #  [orcid,sname=...,gname=...]
        parens = []
        if author.orcid:
            parens.append(author.orcid)
        if author.given_name:
            parens.append(f"gname='{latex2text(author.given_name)}'")
        if author.family_name:
            parens.append(f"sname='{latex2text(author.family_name).replace(',', ' ')}'")
        return "[" + ",".join(parens) + "]" if parens else ""


class LsstDoc(AuthorTextGenerator):
    """LaTeX lsstdoc tech notes."""

    mode = "lsstdoc"

    def generate(self, header: bool = True) -> str:
        authors = list(self.authors)
        last = authors.pop()

        # Join with "," until last author joins with "and"
        lines = [f"{author.full_latex_name}," for author in authors]
        if lines:
            lines.append("and")
        lines.append(last.full_latex_name)

        return (self.get_header() if header else "") + "\\author{\n" + "\n".join(lines) + "\n}"


class Arxiv(AuthorTextGenerator):
    """Generate ArXiv format.

    Authors: Author One (1), Author Two (1 and 2), Author Three (2)
       ((1) Institution One, (2) Institution Two)
    """

    mode = "arxiv"

    def generate(self, header: bool = True) -> str:
        """Generate ArXiv format."""
        affil_to_number = self.number_affiliations()

        author_text = []
        for author in self.authors:
            affil_numbers = [str(affil_to_number[affil]) for affil in author.affiliations]
            author_text.append(f"{author.full_name} ({' and '.join(affil_numbers)})")

        institutions = []
        for affil, number in affil_to_number.items():
            institutions.append(f"({number}) {latex2text(affil.get_department_and_institute())}")

        return f"Authors: {', '.join(author_text)}\n       ({', '.join(institutions)})"


class ProcSpie(AuthorTextGenerator):
    r"""SPIE proceedings.

    \author[a]{Anna A. Author}
    \author[a,b]{Barry B. Author}
    \affil[a]{Affiliation1, Address, City, Country}
    \affil[b]{Affiliation2, Address, City, Country}

    """

    mode = "spie"

    def generate(self, header: bool = True) -> str:
        affil_to_number = self.number_affiliations()
        chars = string.ascii_lowercase + string.ascii_uppercase

        # SPIE prefers labels over numbers, so convert affiliation numbers
        # to labels but once we have more than the number of letters we switch
        # back to numbers.
        affil_to_label: dict[Affiliation, str] = {}
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

        affiliations: list[str] = []
        for affil, label in affil_to_label.items():
            affiliations.append(rf"\affil[{label}]{{{affil.get_full_address_with_institute()}}}")

        return (self.get_header() if header else "") + "\n".join(authors + affiliations)


class WebOfC(AuthorTextGenerator):
    """WebOfC generator."""

    mode = "webofc"

    def generate(self, header: bool = True) -> str:
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
        affiliations = " \\and\n".join(a.get_full_address_with_institute() for a in affil_to_number)

        return (
            (self.get_header() if header else "")
            + "\\author{\n"
            + " \\and\n".join(authors)
            + "\n}\n\\institute{\n"
            + affiliations
            + "\n}"
        )


class ASCOM(AuthorTextGenerator):
    """Astronomy and Computing."""

    mode = "ascom"

    def generate(self, header: bool = True) -> str:
        """Generate A&C format."""
        affil_to_number = self.number_affiliations()

        authors = []
        for author in self.authors:
            affil_numbers = [str(affil_to_number[affil]) for affil in author.affiliations]
            orclink = ""
            if author.orcid:
                orclink = f"\\orcidlink{{{author.orcid}}}"
            author_text = f"\\author[{','.join(affil_numbers)}]{{{author.full_latex_name}{orclink}}}"
            authors.append(author_text)
        affiliations = []
        for affil, number in affil_to_number.items():
            country = ""
            if affil.address and (country_code := affil.address.country_code):
                country = f", country={{{country_code}}}"
            affil_text = f"""\\affiliation[{number}]{{
organization={{{affil.get_department_and_institute()}}}{country}}}"""
            affiliations.append(affil_text)

        return (self.get_header() if header else "") + "\n".join(authors) + "\n" + "\n".join(affiliations)


class ADASS(AuthorTextGenerator):
    """Generate ADASS text."""

    mode = "adass"

    @staticmethod
    def _to_affil_text(affil_to_number: dict[Affiliation, int], affiliations: list[Affiliation]) -> str:
        affil_numbers = [str(affil_to_number[affil]) for affil in affiliations]
        affil_text = " ".join(f"$^{n}$" for n in affil_numbers)
        return affil_text

    def generate(self, header: bool = True) -> str:
        affil_to_number = self.number_affiliations()

        authors = list(self.authors)
        lead_email = authors[0].email
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
            if number > 1:
                email = ""
            else:
                email = rf"; \email{{{lead_email}}}"
            affiliations.append(f"\\affil{{$^{number}${affil.get_city_with_institute()}{email}}}")

        paperauthors = []
        for author in self.authors:
            # Uses primary affiliation.
            affil = author.affiliations[0]
            parsed = {}
            if affil.address:
                parsed["city"] = affil.address.city or ""
                parsed["state"] = affil.address.state or ""
                parsed["postcode"] = affil.address.postcode or ""
                parsed["country"] = affil.address.country_code or ""
            else:
                parsed["city"] = ""
                parsed["state"] = ""
                parsed["postcode"] = ""
                parsed["country"] = ""
            parsed["institute"] = affil.institute or ""
            parsed["department"] = affil.department or ""
            parsed["full_name"] = author.full_latex_name
            parsed["email"] = author.email
            parsed["orcid"] = author.orcid or ""
            paperauthors.append(
                (
                    r"\paperauthor"
                    "{{{full_name}}}{{{email}}}{{{orcid}}}"
                    "{{{institute}}}{{{department}}}{{{city}}}{{{state}}}{{{postcode}}}{{{country}}}"
                ).format(**parsed)
            )

        aindexes = ["%% Must be commented out"]
        for author in self.authors:
            aindexes.append(f"%\\aindex{{{author.latex_name_then_initials}}}")

        return (
            (self.get_header() if header else "")
            + "\\author{"
            + " ".join(author_lines)
            + "}\n"
            + "\n".join(affiliations)
            + "\n"
            + "\n".join(paperauthors)
            + "\n"
            + "\n".join(aindexes)
        )


class MNRAS(AuthorTextGenerator):
    r"""Generate MNRAS format.

    Complication for MNRAS is that it expects the author to be responsible
    for spreading the authors across multiple lines.

    Example output:

    \author[K. T. Smith et al.]{
    Keith T. Smith,$^{1}$
    A. N. Other,$^{2}$
    and Third Author$^{2,3}$
    \\
    $^{1}$Affiliation 1\\
    $^{2}$Affiliation 2\\
    $^{3}$Affiliation 3}
    """

    mode = "mnras"

    def generate(self, header: bool = True) -> str:
        affil_to_number = self.number_affiliations()
        n_authors = len(self.authors)
        authors = []
        for i, author in enumerate(self.authors):
            final_author = i == len(self.authors) - 1
            sep = "," if not final_author else ""

            affil_numbers = [str(affil_to_number[affil]) for affil in author.affiliations]
            author_text = f"{author.full_latex_name}{sep}$^{{{','.join(affil_numbers)}}}$"
            if n_authors > 1 and final_author:
                author_text = "and " + author_text
            authors.append(author_text)

        short_author = self.authors[0].initials_latex_name
        if len(self.authors) == 2:
            short_author = self.authors[0].family_name + " and " + self.authors[1].family_name
        elif len(self.authors) > 2:
            short_author += " et al."

        affiliations = []
        for affil, number in affil_to_number.items():
            affiliations.append(f"$^{number}${affil.get_full_address_with_institute()}")
        affil_text = "\\\\\n".join(affiliations)
        authors_block = "\n".join(authors)
        return f"""{self.get_header() if header else ""}\\author[{short_author}]{{
{authors_block}
\\\\
{affil_text}
}}
"""


class AAP(AuthorTextGenerator):
    r"""Generate A&A format.

    Example output:

    \author{Daniel J. Pierce\inst{1,3}
      \and Apostolos Hadjidimios\inst{2}
      \and Robert J. Plemmons\inst{3}}

    \institute{Boeing Computer Service, P.O. Box 24346,
               MS 7L-21, Seattle, WA 98124-0346, USA
      \and Department of Mathematics, University of Ioannina,
           GR-45 1210, Ioannina, Greece
      \and Department of Computer Science and Mathematics,
           North Carolina State University, Raleigh, NC 27695-8205, USA
    }
    """

    mode = "aap"

    def generate(self, header: bool = True) -> str:
        affil_to_number = self.number_affiliations()
        authors = []
        for author in self.authors:
            affil_numbers = [str(affil_to_number[affil]) for affil in author.affiliations]
            author_text = rf"{author.full_latex_name}\inst{{{','.join(affil_numbers)}}}"
            authors.append(author_text)

        affiliations = []
        for affil in affil_to_number:
            affiliations.append(f"{affil.get_full_address_with_institute()}")
        affil_text = "\n\\and ".join(affiliations)

        authors_block = "\n\\and ".join(authors)
        return f"""{self.get_header() if header else ""}\\author{{
{authors_block}
}}
\\institute{{
{affil_text}
}}
"""


@dataclasses.dataclass
class AASAuthorRow:
    """Representation of a row in the AAS author CSV file."""

    is_corresponding: str = ""
    author_order: int = 0
    title: str = ""
    given_name: str = ""
    middle_name: str = ""
    family_name: str = ""
    email: str = ""
    telephone: str = ""
    institution: str = ""
    department: str = ""
    address1: str = ""
    address2: str = ""
    city: str = ""
    state: str = ""
    postcode: str = ""
    country: str = ""


class AASCSV(AuthorTextGenerator):
    """Generate CSV format for AAS journals.

    The template XLSX file is at
    https://aas.msubmit.net/html/Authors_Template.xls

    The columns are:

    * Is Corresponding Author (enter Yes)
    * Author Order
    * Title
    * Given Name/First Name
    * Middle Initial(s) or Name
    * Family Name/Surname
    * Email
    * Telephone
    * Institution
    * Department
    * Address Line 1
    * Address Line 2
    * City
    * State/Province
    * Zip/Postal Code
    * Country

    No attempt is made to fill in the "Is Corresponding Author", Title, or
    Telephone fields.
    """

    mode = "aascsv"

    def generate(self, header: bool = True) -> str:
        # Declare the field names from the dataclass but do not use them
        # to write the header since we want to match the template exactly.
        # Need to write to a string buffer since csv.writer needs a file-like
        # object.
        output = io.StringIO()
        writer = csv.writer(output, dialect=csv.excel)

        # Not sure how critical it is to match the names exactly with the
        # template.
        writer.writerow(
            [
                "Is Corresponding Author (enter Yes)",
                "Author Order",
                "Title",
                "Given Name/First Name",
                "Middle Initial(s) or Name",
                "Family Name/Surname",
                "Email",
                "Telephone",
                "Institution",
                "Department",
                "Address Line 1",
                "Address Line 2",
                "City",
                "State/Province",
                "Zip/Postal Code",
                "Country",
            ]
        )

        author_order = 0
        for author in self.authors:
            author_order += 1
            # Only use information from the first affiliation.
            affil = author.affiliations[0] if author.affiliations else None
            if affil is None:
                raise RuntimeError(f"Author {author.full_name} has no affiliation")
            # Require an affiliation with an address.
            if affil.address is None:
                raise RuntimeError(
                    f"Author {author.full_name} has no address in their first affiliation {affil}"
                )

            # Middle name is not really tracked in our database but is
            # requested for the AAS CSV format. Split on space and assume the
            # first part is the given name and the rest is middle name.
            # This will not work for all names but it's the best we can do.
            # This means that "K. Simon Krughoff" becomes "K." for given name.
            parts = latex2text(author.given_name).split()
            given_name = parts.pop(0) if parts else ""
            middle_name = " ".join(parts) if parts else ""

            row = AASAuthorRow(
                author_order=author_order,
                given_name=given_name,
                middle_name=middle_name,
                family_name=latex2text(author.family_name),
                email=author.email,
                address1=latex2text(affil.address.street) if affil.address.street else "",
                city=latex2text(affil.address.city) if affil.address.city else "",
                state=latex2text(affil.address.state) if affil.address.state else "",
                postcode=affil.address.postcode if affil.address.postcode else "",
                country=affil.address.country_code if affil.address.country_code else "",
                institution=latex2text(affil.institute),
                department=latex2text(affil.department or ""),
            )
            writer.writerow(dataclass_asdict(row).values())

        return output.getvalue()


def dump_csvall(factory: AuthorFactory) -> None:
    """Generate CSV of ALL authors for easier lookup of ID .
    Authorid, Name, Institution id
    put this in authors.csv
    """
    author_ids = factory.get_author_ids()
    with open("authors.csv", "w", newline="") as outf:
        writer = csv.writer(outf)
        writer.writerow(["Rubin AuthorID", "Name", "Affiliation ID(s)", "AASTEX"])
        for authorid in author_ids:
            author = factory.get_author(authorid)
            aas7_generator = AASTeX7([author])
            # people seeing the full affiliation copied it so putting IDs
            affils = " / ".join(factory.get_affiliation_id(a) for a in author.affiliations)
            # Generate aas7 string using the AASTeX7 generator
            aas7_text = aas7_generator.generate(header=False)
            # the email should not be plain ..
            aas7_text = aas7_text.replace("@", " AT ")
            writer.writerow([authorid, latex2text(author.full_name), affils, aas7_text])
    affil_ids = factory.get_affiliation_ids()
    with open("affiliations.csv", "w") as outf:
        writer = csv.writer(outf)
        writer.writerow(["ID", "Affiliation"])
        for id in affil_ids:
            affil = factory.get_affiliation(id)
            writer.writerow([id, latex2text(affil.get_full_address_with_institute())])


def load_dni(donotinclude: str) -> set[str]:
    """
    Load  the standard 'do not include' file and return a list of author IDs.
    Look for a local one also and add that.

    Parameters
    ----------
    donotinclude : `str`
        Path to the file containing one author ID per line YAML format.
        Same format as authors.yaml

    Returns
    -------
    list[str]
        A list of author IDs (strings)
    """
    authorids: set[str] = set()
    with open(donotinclude, encoding="utf-8") as f:
        authorids = set(yaml.safe_load(f) or [])
    dnip = Path("dni.yaml")
    if dnip.exists():  # local per doc
        with dnip.open(encoding="utf-8") as f:
            dni_local = yaml.safe_load(f)
            authorids.update(dni_local)

    if len(authorids) > 0:
        print(f"WARNING: Not including {authorids}", file=sys.stderr)
    return authorids


if __name__ == "__main__":
    # There is a file listing all the authors and a file mapping
    # those authors to full names and affiliations

    # This is the author list. It's a yaml file with authorID that
    # maps to the database file below.  For now we assume this file is in
    # the current working directory.
    authorfile = os.path.join("authors.yaml")

    # this should probably be a dict with the value of affil_cmd
    # the keys could then be passed to the arg parser.
    OUTPUT_MODES = [
        "aas",
        "aas7",
        "spie",
        "adass",
        "arxiv",
        "ascom",
        "webofc",
        "lsstdoc",
        "csvall",
        "mnras",
        "aap",
        "aascsv",
    ]

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
    dnifile = os.path.normpath(os.path.join(exedir, os.path.pardir, "etc", "dni.yaml"))

    with open(dbfile) as fh:
        authordb = yaml.safe_load(fh)

    factory = AuthorFactory.from_authordb(authordb)

    if args.mode == "csvall":
        dump_csvall(factory)
        exit(0)

    with open(authorfile) as fh:
        authors = yaml.safe_load(fh)

    dni_list = load_dni(dnifile)
    authors = [a for a in authors if a not in dni_list]
    authors = [factory.get_author(authorid) for authorid in authors]

    generator_lut: dict[str, type[AuthorTextGenerator]] = {
        "aas": AASTeX,
        "aas7": AASTeX7,
        "lsstdoc": LsstDoc,
        "arxiv": Arxiv,
        "spie": ProcSpie,
        "webofc": WebOfC,
        "ascom": ASCOM,
        "adass": ADASS,
        "mnras": MNRAS,
        "aap": AAP,
        "aascsv": AASCSV,
    }
    if args.mode not in generator_lut:
        raise RuntimeError(f"Unknown generator mode: {args.mode}")

    generator = generator_lut[args.mode](authors)
    print(generator.generate())
