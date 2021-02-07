import pandas as pd
import pygsheets
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']




class GoogleSheet:

    global values_input, service


    def __init__(self, ID, JSON):
        """

        :param ID: Id for sheet found in sheet url
        :param JSON: directory to JSON file from google api
        """

        self.SHEET_ID = ID
        self.JSON_FILE = JSON
        self.sheet = None
        self.google_sheet = None
        self.active_sheet = self.sheet
        self.service = None
        self.values_input = None
        self.create_gsheet()
        #self.grab_sheet()

    def create_gsheet(self):
        self.authorization =pygsheets.authorize(client_secret=self.JSON_FILE)
        self.google_sheet = self.authorization.open('Sheet1')
        self.active_sheet = self.google_sheet[0]

    #replaced by create_gsheet
    def grab_sheet(self):

        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    json_file, SCOPES)  # here enter the name of your downloaded JSON file
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        self.sheet = self.service.spreadsheets()

        self.set_active_sheet()

        print("Got sheet")


    def read(self, sheet_range):
        result_input = self.sheet.values().get(spreadsheetId=self.SHEET_ID,
                                          range=sheet_range).execute()
        self.values_input = result_input.get('values', [])

        # if not values_input and not values_expansion:
        if not self.values_input:
            print('No data found.')
        else:
            return self.values_input

    def write(self, data, loc, work_sheet=False):
        """

        :param data: [Dict] where the key is the column name, and def is the values
        :param loc: [tuple] Init cell to place data in google sheet ()
        :return:
        """
        self.active_sheet.set_dataframe(data, loc)
        print('Sheet successfully Updated')

    def set_active_sheet(self, new_sheet=False):
        if new_sheet is False:
            self.active_sheet = self.sheet
        else:
            self.active_sheet = self.sheet.worksheet_by_title(new_sheet)

    def format_data_for_write(self, data):
        """

        :param data: [Dict] where the key is the column name, and def is the values
        :return:
        """
        pass
        #
        # df = pd.DataFrame(data, columns=data.keys())
        #
        # {
        #     "values": [],
        #     "range": ""
        # }


if __name__ == '__main__':
    # here enter the id of your google sheet
    SAMPLE_SPREADSHEET_ID_input = '1Xl3l43zkO91ba1zSjhbfcqvx9HRm1uc3nRjSRP0ykFk'
    SAMPLE_RANGE_NAME = 'A1:D4'
    json_file_incorrect = r'C:\Users\dunha\OneDrive\Documents\Investment\invstr\FinanceTool\google_sheets\financer-304116-' \
                          r'9527b86349af.json'
    json_file = 'client_secret_214644974504-lnabcc77ujsqnqfjhqu5lb3p1rb4d75l.apps.googleusercontent.com.json'

    gsheet = GoogleSheet(SAMPLE_SPREADSHEET_ID_input, json_file)
    values = gsheet.read('A1:D3')
    df = pd.DataFrame()
    df['name'] = ['John', 'Steve', 'Sarah']
    #gsheet.write(df, (5, 1))



    print(values)

