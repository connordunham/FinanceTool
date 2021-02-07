import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1Xl3l43zkO91ba1zSjhbfcqvx9HRm1uc3nRjSRP0ykFk'
SAMPLE_RANGE_NAME = 'A1:D4'
json_file_incorrect = r'C:\Users\dunha\OneDrive\Documents\Investment\invstr\FinanceTool\google_sheets\financer-304116-' \
                      r'9527b86349af.json'
json_file = 'client_secret_214644974504-lnabcc77ujsqnqfjhqu5lb3p1rb4d75l.apps.googleusercontent.com.json'

def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                json_file, SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    print(values_input)

    # if not values_input and not values_expansion:
    if not values_input:
        print('No data found.')

main()

#df=pd.DataFrame(values_input[1:], columns=values_input[0])