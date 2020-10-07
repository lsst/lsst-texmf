#!/usr/bin/env python3

r"""This script will generate latex tables from cells in a google sheet.
You must pass the sheet Identifier and Sheet name(s) you wish to process.
Identify your table by putting in a cell in column A `Table ID` where ID
is the unique name used as the label in tex and will be the name of the
file holding the table.
Column B should hold the description.
Column C is an integer value for the number of columns you want to extract.
Column D is an integer for the number of columns you want to skip
         not including the first
Column E can hold an optional Longtable format for the table.
The next row is assumed to be a title row and will be bold.
All following rows are output accordingly as table rows.
If the word Total appears in Column A the row will be bold.

To access google you have to do some setup
``https://developers.google.com/sheets/api/quickstart/python``
roughly you must create a client secret for OAUTH using this wizard
``https://console.developers.google.com/start/api?id=sheets.googleapis.com``
Accept the blurb and go to the APIs
click CANCEL on the next screen to get to the `create credentials`
hit create credentials choose OATH client
Configure a product - just put in a name like `LSST DOCS`
Create web application id
Give it a name hit ok on the next screen
now you can download the client id - call it client_secret.json
as expected below.
You have to do this once to allow the script to access your google stuff
from this machine.
"""


import httplib2
import os
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauth2client.client import Credentials

import argparse

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'LSST Tables from Google Sheet'


def get_credentials() -> Credentials:
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds



def complete_and_close_table(tout):
    if tout:
        print(r"\end{longtable} \normalsize", file=tout)
        tout.close()
        return
    else:
        raise Exception('Expected and open file to end table in')


def outhead(ncols, tout, name, cap, form=None):
    print(r"\tiny \begin{longtable} {", file=tout, end='')
    c = 1
    if (form is None):
        print(" |p{0.22\\textwidth} ", file=tout, end='')
        for c in range(1, ncols + 1):
            print(" |r ", file=tout, end='')
        print("|} ", file=tout, )
    else:
        print(form + "} ", file=tout, end='')

    print(r"\caption{%s \label{tab:%s}}\\ " % (cap, name), file=tout)
    print(r"\hline ", file=tout)
    return


def outputrow(tout, pre, row, cols, skip):
    skipped = 0
    for i in range(cols):
        if (i > 0 and skipped < skip):
            skipped = skipped + 1
        else:
            try:
                print("%s{%s}" % (pre, fixTex(row[i])), end='', file=tout)
            except IndexError:
                pass
            if i < cols-1:
                print("&", end='', file=tout)
    print(r" \\ \hline", file=tout)


def fixTex(text):
    ret = text.replace("_", "\\_")
    ret = ret.replace("/", "/ ")
    ret = ret.replace("$", "\\$")
    ret = ret.replace("%", "\\%")
    ret = ret.replace("^", "\\^")
    return ret


def genTables(values):
    """
    values contains the selected cells from a google sheet
    this routine goes through the rows looking for rows indicating a new table
    Such rows contain Table in the first cell followed by description,
    number of columns, number of cols to skip eg. my table with 5 columns would
    be preceded by
    ``Table myTable, "This the description", 5, 0``
    Sometimes for wide tables with yearly data we wish to skip some years
    the last number allows that.
    The next row after the declaration is the first output and it is in bold
    assumed to contain the header.
    """

    name = ''
    tout = None

    if not values:
        print('No data found.')
    else:
        cols = 0
        skip = 0
        bold_next = False
        for row in values:
            if (row and 'Table' in row[0]):  # got a new table
                if name:
                    complete_and_close_table(tout)
                vals = row[0].split(' ')
                name = vals[1]
                print("Create new table %s" % name)
                tout = open(name + '.tex', 'w')

                cap = row[1]
                cols = int(row[2])
                skip = int(row[3])
                form = None
                if (row[4]):
                    form = row[4]

                outhead(cols-skip, tout, name, cap, form)
                bold_next = True
            else:
                if name and row:
                    if (row[0].startswith('Year') or
                            row[0].startswith('Total') or
                            bold_next):
                        # print header/total in bold
                        outputrow(tout, "\\textbf", row, cols, skip)
                        bold_next = False
                    else:
                        outputrow(tout, "", row, cols, skip)
    complete_and_close_table(tout)
    return


def get_sheet(sheet_id, range):
    """
    grab the google sheet and return data from sheet
    :String sheetId: GoogelSheet Id like 1R1h41KVtN2gKXJAVzd4KLlcF-FnNhpt1G06YhzwuWiY
    :String sheets: List of TabName\!An:Zn  ranges

    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=range ).execute()
    return result


def main(sheetId, sheets):
    """
    grab the googlesheet and process tables in each sheet
    """

    for r in sheets:
        print("Google %s , Sheet %s" % (sheetId, r))
        result = get_sheet(sheetId, r)
        values = result.get('values', [])
        genTables(values)


if __name__ == '__main__':
    description = __doc__
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=formatter)

    parser.add_argument('id', help="""ID of the google sheet like
                                18wu9f4ov79YDMR1CTEciqAhCawJ7n47C8L9pTAxe""")
    parser.add_argument('sheet', nargs='+',
                        help="""Sheet names  and ranges to process
                             within the google sheet e.g. Model!A1:H""")
    args = parser.parse_args()
    sheetId = args.id
    sheets = args.sheet

    main(sheetId, sheets)
