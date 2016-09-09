from __future__ import print_function
import httplib2
import os
from trello import TrelloClient
import webbrowser
import fileinput
import dateparser
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import sys

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GSheets2TBoards'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():

    print("""Hi there!\nWelcome to Google Sheet to Trello Board converter.
    Before we can get started, a couple of things are needed; spreadsheets id.
    Spreadsheet id is the the collection of numbers and chars after /d/ in the sheets URL like:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
                      where the id is: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
            """)
    spreadsheetId=input('Enter spreadsheet id:')
    print (spreadsheetId)
    if sys.version_info <= (3, 0):
        sys.stdout.write('Sorry, requires Python 3.x, not Python 2.x\n')
        sys.exit(1)

    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1g9ri4om_g29N2j6jPrVXMZpI719R9fmeBBufR4ry2ts'
    rangeName = 'Pre-conf!A3:G'
    sheet=service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    sheetName=sheet['properties']['title']

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    tasks = []

    if not values:
        print('No data found.')
    else:
        for row in values:

            if len(row)>6:
                date= dateparser.parse(row[6])
                tasks.append({'task': row[0], 'description': row[1], 'date': row[6]})

            else:
                print("Task with name %s does not have a date"% row[0])

        print("Opening auth website")
        webbrowser.open_new(
            'https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=Praqma%20Sheetconv&key=72ff9314b2d9e1cca758d131e761117e')
        api_token = input("paste the token you receive in here: ")
        print(api_token)
        client = TrelloClient(
            api_key='72ff9314b2d9e1cca758d131e761117e',
            api_secret='a475e69f4a864b6d7d2c729f00a255cefc89194c903d450f8da081ba911b016d',
            token=api_token,
            token_secret='your-oauth-token-secret'
        )

        board = client.add_board(sheetName)
        id = board.id

        list = board.add_list('Todo')
        for i in tasks:
            print(i)
            list.add_card(name=i['task'], due=i['date'],desc=i['description'])

if __name__ == '__main__':
    main()
