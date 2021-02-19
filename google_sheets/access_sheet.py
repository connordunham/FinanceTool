
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
        self._TERMINATE = False

        #Google Sheet Vars
        self.SHEET_ID = ID
        self.JSON_FILE = JSON
        self.sheet = None
        self.google_sheet = None
        self.active_sheet = self.sheet
        self.service = None
        self.values_input = None
        self.sheet_names = []  #TODO add function that captures all sheet names
        self.Grab_sheet()



    # Update cells values in the google sheet
    def write( self, df, loc="A1:A:100", sheet=False ):
        """

        :param data: [Dict] where the key is the column name, and def is the values
        :param loc: [tuple] Init cell to place data in google sheet ()
        :return:
        """

        if sheet is not False:
            range = sheet + "!" + loc
        else:
            range = loc

        self.Create_Service(self.JSON_FILE, 'sheets', 'v4', ['https://www.googleapis.com/auth/spreadsheets'])

        response_date = self.service.spreadsheets().values().update(
            spreadsheetId=self.SHEET_ID,
            valueInputOption='RAW',
            range=range,
            body=dict(
                majorDimension='ROWS',
                values=df.T.reset_index().T.values.tolist())
        ).execute()
        print('Sheet successfully Updated')

    def read( self, sheet_range, sheet=None ):

        if sheet is not None:
            sheet_range = sheet + '!' + sheet_range

        result_input = self.sheet.values().get(spreadsheetId=self.SHEET_ID,
                                               range=sheet_range).execute()
        self.values_input = result_input.get('values', [])

        # if not values_input and not values_expansion:
        if not self.values_input:
            print('No data found.')
        else:
            return self.values_input

    # Access google sheet object through api
    def Grab_sheet( self ):

        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print(self.JSON_FILE)
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.JSON_FILE, SCOPES)  # here enter the name of your downloaded JSON file
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        self.sheet = self.service.spreadsheets()

        print("Got sheet")


    #Creates google sheets api service from oauth json file
    def Create_Service( self, client_secret_file, api_service_name, api_version, *scopes ):
        SCOPES = [scope for scope in scopes[0]]
        # print("SCOPES: " + SCOPES)

        cred = None

        if os.path.exists('token_write.pickle'):
            with open('token_write.pickle', 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
                cred = flow.run_local_server()

            with open('token_write.pickle', 'wb') as token:
                pickle.dump(cred, token)

        try:
            self.service = build(api_service_name, api_version, credentials=cred)
            print(api_service_name, 'service created successfully')
            # return service
        except Exception as e:
            print(e)
            # return None
