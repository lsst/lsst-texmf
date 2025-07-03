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
        print("Parsing into AuthorDbYaml object...\n")
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
        adbfile.write(adb.model_dump_json(indent=2))
    return authordb_path


class AuthorDbAuthor(BaseModel):
    """Model for an author entry in the authordb.yaml file."""

    name: str = Field(description="Author's surname.")

    initials: str = Field(description="Author's given name.")

    affil: list[str] = Field(default_factory=list, description="Affiliation IDs")

    alt_affil: list[str] = Field(default_factory=list, description="Alternative affiliations / notes.")

    orcid: str | None = Field(
        default=None,
        description="Author's ORCiD identifier (optional)",
    )

    email: str | None = Field(
        default=None,
        description=(
            "Author's email username (if using a known email provider given "
            "their affiliation ID) or ``username@provider`` (to specify the "
            "provider) or their full email address."
        ),
    )

    @property
    def is_collaboration(self) -> bool:
        """Check if the author is a collaboration."""
        return self.initials == "" and self.affil == ["_"]


class AuthorDbYaml(BaseModel):
    """Model for the authordb.yaml file in lsst/lsst-texmf."""

    affiliations: dict[str, str] = Field(
        description=(
            "Mapping of affiliation IDs to affiliation info. Affiliations "
            "are their name, a comma, and their address."
        )
    )

    emails: dict[str, str] = Field(description=("Mapping of affiliation IDs to email domains."))

    authors: dict[str, AuthorDbAuthor] = Field(description="Mapping of author IDs to author information")


if __name__ == "__main__":
    description = __doc__
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)

    adb = load_authordb()

    print("Successfully parsed AuthorDb with:\n")
    print(f"  - {len(adb.affiliations)} affiliations\n")
    print(f"  - {len(adb.emails)} email domains\n")
    print(f"  - {len(adb.authors)} authors\n")

    file = dump_authordb(adb, "new_adb.yaml")
    print(f"Wrote {file}")

    adb = load_authordb(file)
    print(f"Successfully parsed AuthorDb {file} with:\n")
    print(f"  - {len(adb.affiliations)} affiliations\n")
    print(f"  - {len(adb.emails)} email domains\n")
    print(f"  - {len(adb.authors)} authors\n")
