"""Handle AuthorDB Yaml file"""

from __future__ import annotations

import argparse
import os
import re
from typing import Annotated, Self

import yaml
from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator


def load_authordb(file_name: str | None = None) -> AuthorDbYaml:
    """Load the authordb.yaml file."""
    # Get the contents of the authordb.yaml file
    # This is the database file with all the generic information
    # about authors. Locate it relative to this script.
    if file_name:
        authordb_path = file_name
    else:
        exedir = os.path.abspath(os.path.dirname(__file__))
        authordb_path = os.path.normpath(os.path.join(exedir, os.path.pardir, "etc", "authordb.yaml"))

    with open(authordb_path) as adbfile:
        authordb_yaml = yaml.safe_load(adbfile)
        print(f"Parsing into AuthorDbYaml object from {authordb_path}")
        adb = AuthorDbYaml.model_validate(authordb_yaml, strict=True)
    return adb


def dump_authordb(adb: AuthorDbYaml, file_name: str | None = None) -> str:
    """Write  the authordb.yaml file."""
    # Write the contents of the authordb.yaml file
    # This is the database file with all the generic information
    # about authors.
    if file_name:
        authordb_path = file_name
    else:
        exedir = os.path.abspath(os.path.dirname(__file__))
        authordb_path = os.path.normpath(os.path.join(exedir, os.path.pardir, "etc", "authordb.yaml"))

    with open(authordb_path, "w") as adbfile:
        print(f"Writing AuthorDbYaml object to {authordb_path}...\n")
        yaml.safe_dump(adb.model_dump(), adbfile, allow_unicode=True)
    return authordb_path


def check_orcid(orcid: str | None) -> str | None:
    """Check that the ORCID field looks like an ORCID."""
    if orcid is None:
        return None

    # We could strip https://orcid.org/ prefix easily enough but we want
    # to use this tooling to check for consistency in the authordb YAML
    # file and not to work around known issues.
    if re.match(r"^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$", orcid):
        # Looks fine. Return as is.
        return orcid
    if re.match(r"^\d{15}[0-9X]$", orcid):
        return "-".join(orcid[i : i + 4] for i in range(0, len(orcid), 4))

    raise ValueError(f"Given ORCiD does not match standard form: {orcid}")


def check_ror(ror_id: str | None) -> str | None:
    """Check that the ROR looks reasonable."""
    if ror_id is None:
        return None

    if ror_id.startswith("http"):
        raise ValueError(f"ROR ID should not include the domain prefix: {ror_id}")

    if re.match("^0[a-z0-9]{8}$", ror_id):
        # Looks fine.
        return ror_id

    raise ValueError(f"The given ROR looks suspect: {ror_id}")


class Address(BaseModel):
    """Representation of an address."""

    example_expanded: str
    street: str | None = None
    city: str | None = None
    state: str | None = None
    postcode: str | None = None
    country_code: str | None = None


class Affiliation(BaseModel):
    """Representation of an affiliation."""

    institute: str
    department: str | None = None
    ror_id: Annotated[str | None, AfterValidator(check_ror)] = None
    email: str | None = None
    address: Address | None = None
    model_config = ConfigDict(extra="forbid")


class AuthorDbAuthor(BaseModel):
    """Model for an author entry in the authordb.yaml file."""

    family_name: str = Field(description="Author's surname.")
    given_name: str = Field(description="Author's given name or names.")
    affil: list[str] = Field(default_factory=list, description="Affiliation IDs")
    altaffil: list[str] = Field(default_factory=list, description="Alternative affiliations / notes.")
    orcid: Annotated[str | None, AfterValidator(check_orcid)] = Field(
        default=None,
        description="Author's ORCiD identifier (optional)",
    )
    email: str | None = Field(
        default=None,
        description=(
            "Author's email username (if using a known email provider given "
            "their affiliation ID) or ``username@provider`` (to specify the "
            "provider)."
        ),
    )
    model_config = ConfigDict(extra="forbid")

    @property
    def is_collaboration(self) -> bool:
        """Check if the author is a collaboration."""
        return self.given_name == "" and self.affil == ["_"]


class AuthorDbYaml(BaseModel):
    """Model for the authordb.yaml file in lsst/lsst-texmf."""

    affiliations: dict[str, Affiliation] = Field(
        description=("Mapping of affiliation IDs to affiliation info.")
    )
    authors: dict[str, AuthorDbAuthor] = Field(description="Mapping of author IDs to author information")

    def get_email_domains(self) -> dict[str, str]:
        """Get a dictionary of known email domains."""
        domains = {}
        for affilid, affil in self.affiliations.items():
            if affil.email:
                domains[affilid] = affil.email
        return domains

    @model_validator(mode="after")
    def check_author_emails(self) -> Self:
        for authorid, author in self.authors.items():
            if not author.email:
                continue
            if "@" in author.email:
                _, affil_id = author.email.split("@")
                if "." in affil_id:
                    # Fully specified email so nothing to check.
                    continue
            else:
                # Using first affiliation.
                affil_id = author.affil[0]

            affil = self.affiliations.get(affil_id)
            if not affil:
                raise ValueError(f"Author {authorid} refers to unknown affiliation of {affil_id} for email")

            if not affil.email:
                raise ValueError(
                    f"Author {authorid} has email defined but associated affiliation "
                    f"{affil_id} has no email defined"
                )

        return self

    @model_validator(mode="after")
    def check_author_id(self) -> Self:
        incorrect_ids = set()
        prefix_chars = 2  # Some family names are two characters
        for authorid, author in self.authors.items():
            # Check that first two characters of family_name match the
            # first two characters of the author ID.
            # Teams do not follow the convention.
            if not author.given_name:
                continue

            # de X and van Y sometimes drop the prefix in the author ID.
            # For some names there are multiple family names and the first
            # one is not always used.
            lower = author.family_name.lower()
            lower = re.sub("[^a-zA-Z ]+", "", lower)
            comparisons = {lower[:prefix_chars]}
            for prefix in ("van ", "de ", "von der ", "rodrigues de ", "villicana "):
                if lower.startswith(prefix):
                    modified = lower.removeprefix(prefix)
                    comparisons.add(modified[:prefix_chars])
                    break

            if authorid[:prefix_chars].lower() not in comparisons:
                print(comparisons, authorid)
                incorrect_ids.add(f"{authorid} vs {author.family_name!r}")

        if incorrect_ids:
            raise ValueError(f"Author IDs that do not seem to be related to family name: {incorrect_ids}")
        return self


if __name__ == "__main__":
    description = __doc__
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)

    adb = load_authordb()

    print("Successfully parsed AuthorDb with:")
    print(f"  - {len(adb.affiliations)} affiliations")
    print(f"  - {len(adb.authors)} authors")

    file = dump_authordb(adb, "new_adb.yaml")
    print(f"Wrote {file}")

    adb = load_authordb(file)
    print(f"Successfully parsed AuthorDb {file} with:")
    print(f"  - {len(adb.affiliations)} affiliations")
    print(f"  - {len(adb.authors)} authors")
