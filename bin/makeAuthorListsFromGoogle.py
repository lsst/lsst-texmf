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
import os
import os.path
import pickle
import re
from typing import Any

import yaml
from authordb import AuthorDbAuthor, dump_authordb, load_authordb
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauth2client.client import Credentials
from pydantic import BaseModel, Field
from pylatexenc.latexencode import unicode_to_latex

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "Process Authors Google Sheet"

# Fields in the form we care about
EMAIL = 1
UPDATE = 4
AUTHORID = 5
AUTHORIDALT = 6
SURNAME = 7
NAME = 8
AFFIL = 9
ORCID = 10


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


class AuthorYaml(BaseModel):
    """Model for the author dict temp file."""

    authors: dict[str, AuthorDbAuthor] = Field(description="Mapping of author IDs to author information")


def get_initials(names: str, div: str = " ") -> str:
    """Get first letter of word (upto 5) to make an id"""
    all = names.split(div)
    initials = ""
    count = 0
    for n in all:
        count = count + 1
        if len(n) > 0:
            initials = f"{initials}{n[0]}"
        if count > 5:
            break
    return initials


def write_yaml(name: str, values: Any) -> None:
    """Write given dat to  the file name  YAML"""
    with open(name, "w") as file:
        yaml.dump(values, file)


def write_model(name: str, authors: dict[str, AuthorDbAuthor]) -> None:
    """Write given data to  the file name  YAML"""
    adb = AuthorYaml(authors=authors)
    with open(name, "w") as file:
        yaml.dump(adb.model_dump(), file)


def load_model(filename: str) -> dict[str, AuthorDbAuthor]:
    """Read authors  data from the YAML file"""
    with open(filename) as file:
        yaml_data = yaml.safe_load(file)
        print("Parsing into AuthorYaml object...\n")
        adb = AuthorYaml.model_validate(yaml_data)
    return adb.authors


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


def strip_utf(ins: str) -> str:
    """Want simple ids wiht now latex or unicode"""
    outs = unicode_to_latex(ins)
    outs = re.sub(r"[\\'c}{]", "", outs)
    return outs


def make_id(name: str, surname: str) -> str:
    """Make id form surnameinitials no space lowecase"""
    initials = get_initials(name)
    id = strip_utf(f"{surname}{initials}")  # last name initial
    id = id.lower().replace(" ", "")
    return id


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
        toupdate = []
        notfound = []
        newauthors: dict[str, AuthorDbAuthor] = {}
        newaffils: dict[str, str] = {}
        newdomains: dict[str, str] = {}
        authordb = load_authordb()
        authors = authordb.authors
        affils = authordb.affiliations
        domains = authordb.emails

        for row in values:
            id = str(row[AUTHORID]).replace(" ", "")
            if len(id) == 0:  # may be an update
                id = row[AUTHORIDALT]
                if len(id) == 0 or id == "NEW":  # no id
                    id = make_id(row[NAME], row[SURNAME])
                # loaded the authorids from authordb and check ..
                update = "but" in row[UPDATE]
                if update:
                    print(f"Update author {id}  ")
                    if id not in authors:
                        print(f"      but  author {id} - NOT FOUND ")
                        notfound.append(id)
                    toupdate.append(id)
                else:
                    if id in authors:
                        print(f"Perhaps check  clash - author {id} - {row[AUTHORID]}, {row[AUTHORIDALT]} ")
                        clash.append(id)
                    else:
                        print(f"New author {id} - {row[NAME]}, {row[SURNAME]} ")
            # we have an id or a new id now
            if id not in authorids:
                authorids.append(id)

            # next are we updating or creating?
            if len(row) > 6 and len(row[AUTHORIDALT]) > 0:
                # affiliation is it known
                affilidForm = str(row[AFFIL]).split("/")
                affilids = []
                for affilid in affilidForm:
                    if affilid not in affils:
                        if len(affilid) < 10:
                            print(f"Affiliation does not exist :{affilid}")
                        else:  # assume its new
                            affil = affilid
                            affilid = get_initials(affil)
                            newaffils[affilid] = affil
                    affilids.append(affilid)
                    # we have a name so we need to gather the rest.
                if len(row) > ORCID:
                    orcid = str(row[ORCID]).replace("https://orcid.org/", "")
                else:
                    orcid = None
                email: str = handle_email(row[EMAIL], domains, affilid, newdomains)
                author: AuthorDbAuthor = AuthorDbAuthor(
                    initials=unicode_to_latex(row[NAME]),
                    name=unicode_to_latex(row[SURNAME]),
                    orcid=orcid,
                    email=email,
                    affil=affilids,
                    altaffil=[],
                )
                newauthors[id] = author
        authorids = sorted(authorids)
        print(
            "\n"
            f" Clash: {', '.join(clash)} \n"
            f" Not FOUND: {', '.join(notfound)} \n"
            f"got {len(authorids)} authors, "
            f"{len(newauthors) - len(toupdate)} new  and {len(toupdate)} to update, author entries.\n"
            f" {len(newdomains)} new email domains. \n"
            f" {len(newaffils)} new affiliations \n"
            f" {len(clash)} author entries need to be checked (see above) \n"
            f" {len(notfound)} author updates wher authorid not found (see above) \n"
        )
        write_yaml("authors.yaml", authorids)
        write_model("new_authors.yaml", newauthors)
        write_yaml("new_affiliations.yaml", newaffils)
        write_yaml("new_domains.yaml", newdomains)
    return


def get_sheet(sheet_id: str, range: str) -> dict[str, Any]:
    """Grab the google sheet and return data from sheet.

    Parameters
    ----------
    sheet_id : `str`
        GoogelSheet Id like
        ``1R1h41KVtN2gKXJAVzd4KLlcF-FnNhpt1G06YhzwuWiY``
    range : `str`
        List of ``TabName!An:Zn``  ranges
    """
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range).execute()
    return result


def process_google(sheet_id, sheets) -> None:
    """Grab the googlesheet and process data.
    will create new_authos new_afilliations and new_domains
    """
    print(f"Processing Google Sheet ID: {sheet_id}")
    print(f"Sheet ranges: {sheets}")
    for r in sheets:
        result = get_sheet(sheet_id, r)
        values: list[Any] = result.get("values", [])
        genFiles(values)


def merge_authors(author_file: str) -> None:
    """Take the given author yaml file and merge to authodd
    this file shold mathc the AuthorYaml class in authodb.py
    """
    print(f"Merging authors using file: {author_file}")
    authors = load_model(author_file)
    adb = load_authordb()
    print(f"Have {len(adb.authors)} authors")
    adb.authors.update(authors)
    print(f"After update have {len(adb.authors)} authors")
    dump_authordb(adb, "new_adb.yaml")


if __name__ == "__main__":
    description = __doc__ or "Process Google Sheets and merge authors."
    formatter = argparse.RawDescriptionHelpFormatter

    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)

    # Required --process-google with 2+ args: id + sheets
    parser.add_argument(
        "-p",
        "--process-google",
        nargs="+",
        metavar=("ID", "SHEET"),
        help="Process Google Sheet: provide the ID and one or more sheet ranges (e.g. Model!A1:D)",
    )

    # Optional --merge-authors with one file
    parser.add_argument(
        "-m",
        "--merge-authors",
        metavar="AUTHOR_FILE",
        help="Path to YAML file to use for merging authors",
    )

    args = parser.parse_args()

    did_something = False

    if args.process_google:
        sheet_id = args.process_google[0]
        sheet_ranges = args.process_google[1:]
        process_google(sheet_id, sheet_ranges)
        did_something = True

    if args.merge_authors:
        merge_authors(args.merge_authors)
        did_something = True

    if not did_something:
        parser.print_help()
