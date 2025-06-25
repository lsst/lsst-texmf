#!/usr/bin/env python3

r"""Script to generate lml files from the autho sign up google form.

You must pass the sheet Identifier you wish to process.

To access google you have to do some setup
``https://developers.google.com/sheets/api/quickstart/python``

You need  client secret from
''https://console.cloud.google.com/auth''
roughly you must create a client secret for OAUTH using this wizard
``https://console.developers.google.com/start/api?id=sheets.googleapis.com``
Accept the blurb and go to the APIs
click CANCEL on the next screen to get to the `create credentials`
hit create credentials choose OATH client
Configure a product - just put in a name like `Rubin Authors`
Create web application id
Give it a name hit ok on the next screen
now you can download the client id - call it client_secret.json
as expected below.
You have to do this once to allow the script to access your google stuff
from this machine.
"""

import argparse
import dataclasses
import os
import os.path
import pickle
from typing import Any, NamedTuple

import yaml
from db2authors import AuthorFactory
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauth2client.client import Credentials

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "Process Authors Google Sheet"

# Fields in the form we care about
EMAIL = 1
AUTHORID = 5
AUTHORIDALT = 6
SURNAME = 7
NAME = 8
AFFIL = 9
ORCID = 10


@dataclasses.dataclass(frozen=True)
class AuthorY:
    """Representation of an author.
    matching the yaml file authorsdb
    """

    initials: str
    name: str
    email: str
    orcid: str | None
    affil: list[str]
    altaffil: list[str]


class Row(NamedTuple):
    """convenice tupple for handling the row"""

    id: str
    name: str
    affil: str


def get_credentials() -> Credentials:
    """Get valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns
    -------
    creds : `Credentials`
        Credentials, the obtained credential.
    """
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds


def get_initials(names: str, div: str = " ") -> str:
    """Get first letter of word (upto 5) to make an id"""
    all = names.split(div)
    initials = ""
    count = 0
    for n in all:
        count = count + 1
        initials = f"{initials}{n[0]}"
        if count > 5:
            break
    return initials


def write_yaml(name: str, values: Any) -> None:
    """Write given dat to  the file name  YAML"""
    with open(name, "w") as file:
        yaml.dump(values, file)


def handle_email(email: str, domains: dict[str, str], affilid: str, newdomains: dict[str, str]) -> str:
    """Figure out if we know the domain or if we need a new one"""
    theEmail = email
    if "@" in email:
        split = email.split("@")
        mailid = split[0]
        domain = split[1]
        # check if we have the domain
        # easy if the affil matches
        if affilid in domains and domains[affilid] == domain:
            return f"{mailid}@{affilid}"
        # ok perhpas we   know the domain but it is not the affil
        if domain in domains.values():
            domainid = list(domains.keys())[list(domains.values()).index(domain)]
            return f"{mailid}@{domainid}"
        # right then - we need a new one
        if affilid in domains:
            # can not use the affilid so try to make an id
            domainid = domain.split(".")[0]
            while domainid in domains:  # hopefully not ever
                domainid = f"{domainid}Z"
        else:  # an afill without a domain .. possibly new
            domainid = affilid
        newdomains[domainid] = domain
        return f"{mailid}@{domainid}"

    return theEmail


def genFiles(values: list) -> None:
    """Generate Files.
    authors.yaml - with all authorids
    addupdatelist.yaml - authors that need to be created/updated.

    values contains the selected cells from a google sheet with format
    timestamp
    Email Address
    Affirmation
    Are you a Rubin Observatory Builder?
    If you found your entry, please enter your authorid here, (May be NEW)
    Please enter your surname (aka family name or last name)
    Please enter your full name, without your surname,
    Please enter your affilid
    ORCID (optional)
    Any comments, questions, or concerns?
    """
    if not values:
        print("No data found.")
    else:
        authorids = []
        clash = []
        newauthors: dict[str, AuthorY] = {}
        newaffils: dict[str, str] = {}
        newdomains: dict[str, str] = {}
        exedir = os.path.abspath(os.path.dirname(__file__))
        dbfile = os.path.normpath(os.path.join(exedir, os.path.pardir, "etc", "authordb.yaml"))
        with open(dbfile) as fh:
            authordb = yaml.safe_load(fh)

        factory = AuthorFactory.from_authordb(authordb)
        authors = factory.get_author_ids()
        affils = factory.get_affiliation_ids()
        domains = factory.get_emaili_domains()

        for row in values:
            id = row[AUTHORID]
            if len(id) == 0:  # may be an update
                id = row[AUTHORIDALT]
                initials = get_initials(row[NAME])
                id = f"{row[SURNAME]}{initials}"  # last name initial
                id = id.lower()
                # loaded the authorids from suthordb and check ..
                if id in authors:
                    print(f"Perhaps check  clash - author {id} - {row[AUTHORID]}, {row[AUTHORIDALT]} ")
                    clash.append(id)
                print(f"New author {id} - {row[NAME]}, {row[SURNAME]} ")
            # we have an id or a new id now
            if id not in authorids:
                authorids.append(id)

            # next are we updating or creating?
            if len(row) > 6 and len(row[AUTHORIDALT]) > 0:
                # affiliation is it known
                affilid = row[AFFIL]
                if affilid not in affils:
                    if len(affilid) < 10:
                        print(f"Affiliation does not exist :{affilid}")
                    else:  # assue its new
                        affil = affilid
                        affilid = get_initials(affil)
                        newaffils[affilid] = affil

                # we have a name so we need to gather the rest.
                orcid = row[ORCID]
                if len(orcid) == 0:
                    orcid = None
                email: str = handle_email(row[EMAIL], domains, affilid, newdomains)
                author: AuthorY = AuthorY(
                    initials=row[NAME],
                    name=row[SURNAME],
                    orcid=orcid,
                    email=email,
                    affil=[affilid],
                    altaffil=[],
                )
                newauthors[id] = author
        authorids = sorted(authorids)
        print(
            f"got {len(authorids)} authors, "
            f"{len(newauthors)} new or updated author entries. "
            f"{len(newdomains)} new email domains. "
            f" {len(clash)} author entries need to be checked"
        )
        write_yaml("authors.yaml", authorids)
        write_yaml("new_authors.yaml", newauthors)
        write_yaml("new_affiliations.yaml", newaffils)
        write_yaml("new_domains.yaml", newdomains)
    return


def get_sheet(sheet_id: str, range: str) -> dict[str, Any]:
    """Grab the google sheet and return data from sheet.

    Parameters
    ----------
    sheetId : `str`
        GoogelSheet Id like
        ``1R1h41KVtN2gKXJAVzd4KLlcF-FnNhpt1G06YhzwuWiY``
    sheets : `str`
        List of ``TabName!An:Zn``  ranges
    """
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range).execute()
    return result


def main(sheetId: str, sheets: str) -> None:
    """Grab the googlesheet and process data."""
    for r in sheets:
        print(f"Google {sheetId} , Sheet {r}")
        result = get_sheet(sheetId, r)
        values: list[Any] = result.get("values", [])
        genFiles(values)


if __name__ == "__main__":
    description = __doc__
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)

    parser.add_argument(
        "id",
        help="""ID of the google sheet like
                                18wu9f4ov79YDMR1CTEciqAhCawJ7n47C8L9pTAxe""",
    )
    parser.add_argument(
        "sheet",
        nargs="+",
        help="""Sheet names  and ranges to process
                             within the google sheet e.g. Model!A1:H""",
    )
    args = parser.parse_args()
    sheetId = args.id
    sheets = args.sheet

    main(sheetId, sheets)
