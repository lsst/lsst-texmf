"""Handle AuthorDB Yaml file"""

from __future__ import annotations

import argparse
import os

import yaml
from pydantic import BaseModel, Field


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
        adb = AuthorDbYaml.model_validate(authordb_yaml)
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
    ror_id: str | None = None
    email: str | None = None
    address: Address | None = None


class AuthorDbAuthor(BaseModel):
    """Model for an author entry in the authordb.yaml file."""

    name: str = Field(description="Author's surname.")

    initials: str = Field(description="Author's given name.")

    affil: list[str] = Field(default_factory=list, description="Affiliation IDs")

    altaffil: list[str] = Field(default_factory=list, description="Alternative affiliations / notes.")

    orcid: str | None = Field(
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

    @property
    def is_collaboration(self) -> bool:
        """Check if the author is a collaboration."""
        return self.initials == "" and self.affil == ["_"]


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
