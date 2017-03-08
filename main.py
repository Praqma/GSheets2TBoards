from __future__ import print_function
import httplib2
import os
import requests
import webbrowser
import fileinput
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
        print('Storing credentials to ' + credential_path)
    return credentials


def main():

    print("""
    Hi there!
    Welcome to Google Sheet to Trello Board converter.
        Before we can get started, a couple of things are needed; the spreadsheet's ID.
        Spreadsheet ID is the the collection of numbers and characters between /d/ and / in the sheet's URL like:
        https://docs.google.com/spreadsheets/d/1HFU0lhE45XY7yQTgo35wRKJtNneKma87tES9M82LnGQ/edit
                      where the id is: 1HFU0lhE45XY7yQTgo35wRKJtNneKma87tES9M82LnGQ.
    If you are using the 'Template - Conference Planning' with the id in the example, just push enter.
            """)
    spreadsheet_id=input("Enter the spreadsheet's ID:")


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

    if spreadsheet_id=='':
        spreadsheet_id = '1HFU0lhE45XY7yQTgo35wRKJtNneKma87tES9M82LnGQ'

    range_others = ['Stem data!B2', 'Stem data!B5', 'Stem data!B6', 'Stem data!A12:A32']
    results_other=service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id, ranges=range_others).execute()
    date = results_other['valueRanges'][0]['values'][0][0]
    title = results_other['valueRanges'][1]['values'][0][0]
    if 'values' in results_other['valueRanges'][2]:
        color = results_other['valueRanges'][2]['values'][0][0]
    else:
        color = ""
    columns = results_other['valueRanges'][3]['values']

    range_data = ['Tasks!A3:G']
    results=service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id, ranges=range_data).execute()
    values = results.get('valueRanges', [])
    tasks = []
    if not values:
        print('No data found.')
    else:
        for range in values:
            for row in range['values']:
                tasks.append({'task': row[0], 'description': row[1], 'column': row[2], 'assigned': row[3], 'date': row[5]})

        print("""
    Please copy this link in your browser:
https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=Praqma%20Sheetconv&key=72ff9314b2d9e1cca758d131e761117e
    Press 'accept' to let the script have access to your account.""")
        api_token = input("\nPaste the token you receive on Trello in here: ")
        #kept these as documentation from the old client
        #client = TrelloClient(
            #api_key='72ff9314b2d9e1cca758d131e761117e',
            #api_secret='a475e69f4a864b6d7d2c729f00a255cefc89194c903d450f8da081ba911b016d',
            #token=api_token,
            #token_secret='your-oauth-token-secret'
        #)

        res = requests.post("https://api.trello.com/1/boards?name="+title+"&key=72ff9314b2d9e1cca758d131e761117e&token=4dd3769e27219fa66d54faa1a08e620cf2e555952d80b2bff302c476a8a8f8c0")
        board = res.json()

        res = requests.put("https://api.trello.com/1/boards/"+board['id']+"/prefs/background?value="+color+"&key=72ff9314b2d9e1cca758d131e761117e&token=4dd3769e27219fa66d54faa1a08e620cf2e555952d80b2bff302c476a8a8f8c0")

        columns = columns[::-1]

        res = requests.get("https://api.trello.com/1/boards/"+board['id']+"/lists?key=72ff9314b2d9e1cca758d131e761117e&token=4dd3769e27219fa66d54faa1a08e620cf2e555952d80b2bff302c476a8a8f8c0")
        lists = res.json()

        for l in lists:
            requests.put("https://api.trello.com/1/lists/"+l['id']+"/closed?value=true&key=72ff9314b2d9e1cca758d131e761117e&token=4dd3769e27219fa66d54faa1a08e620cf2e555952d80b2bff302c476a8a8f8c0")

        for col in columns:
            requests.post("https://api.trello.com/1/boards/"+board['id']+"/lists?name="+col[0]+"&key=72ff9314b2d9e1cca758d131e761117e&token=4dd3769e27219fa66d54faa1a08e620cf2e555952d80b2bff302c476a8a8f8c0")

        res = requests.get("https://api.trello.com/1/lists/"+board['id']+"/lists?key=72ff9314b2d9e1cca758d131e761117e&token=4dd3769e27219fa66d54faa1a08e620cf2e555952d80b2bff302c476a8a8f8c0")

        res = requests.get("https://api.trello.com/1/boards/"+board['id']+"/lists?key=72ff9314b2d9e1cca758d131e761117e&token=4dd3769e27219fa66d54faa1a08e620cf2e555952d80b2bff302c476a8a8f8c0")
        lists = res.json()

        print("\n    Loading the goodies into Trello...")
        for the_list in lists:
            for col in columns:
                if the_list['name'] == col[0]:
                    for i in tasks:
                        if i['column'] == col[0]:
                            requests.post("https://api.trello.com/1/lists/"+the_list['id']+"/cards?name="+i['task']+"&due="+i['date']+"&key=72ff9314b2d9e1cca758d131e761117e&token=4dd3769e27219fa66d54faa1a08e620cf2e555952d80b2bff302c476a8a8f8c0")

        print("\n    Goodies loaded! Go into www.trello.com to find your new board named "+title+"!")

        print("\n    Off you go, organize an outstanding event! \n")

if __name__ == '__main__':
    main()
