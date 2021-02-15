import pandas as pd
import pygsheets
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle
import threading,time, signal
from datetime import timedelta

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
WAIT_TIME_MINS = 10
# WAIT_TIME_SECONDS = WAIT_TIME_MINS * 60
WAIT_TIME_SECONDS = 1


""" Safe kill of program """
class ProgramKilled(Exception):
    pass
def foo():
    print(time.ctime())
def signal_handler(signum, frame):
    raise ProgramKilled

class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)



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
        #self.create_gsheet()
        self.Grab_sheet()


        #Portfolio Maintenance Varsself.cur_time = time.ctime()
        self._PORTFOLIO_DATA = []
        self._PORTFOLIO_RANGE = "A1:H49"
        self.num_stocks_held = 0

        # Time vars
        self.cur_time = 0
        self.cur_date = 0
        self.cur_day = 0
        self.cur_hour  = 0

        self.update_time()



        print(self.cur_hour)

        self.weekly_chg_tracker = {"Portfolio Holdings": "A50:H"}

    # Updates the neccassary parts of spread sheet every 10 minutes
    def update(self):

        self.update_time()

        if int(self.cur_hour) > 0:
            self.preopen_update()

        self.write(self._PORTFOLIO_DATA, self._PORTFOLIO_RANGE)

        # Write latest update time
        time = pd.DataFrame([self.cur_time], columns=["Time Last Updated"])
        self.write(time, "J1:J2", "Portfolio Holdings")


    # Updates neccassry fields of spread sheet at 9:00am
    def preopen_update(self):


        data = self.read("A1:H49", "Portfolio Holdings")
        main_table_headers = data[0]
        main_table = data[1:]

        self._PORTFOLIO_DATA = pd.DataFrame(main_table, columns=main_table_headers)
        self.num_stocks_held = len(main_table)
        self.opening_value = self.calc_port_value()

        print('Premarket update completed at: ' + self.cur_time)

    def calc_port_value(self):

        for ticker in self._PORTFOLIO_DATA['Stock']:
            print(ticker)


    def create_gsheet(self):
        self.authorization =pygsheets.authorize(client_secret=self.JSON_FILE)
        self.google_sheet = self.authorization.open('Sheet1')
        self.active_sheet = self.google_sheet[0]


    def read(self, sheet_range, sheet=None):

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

    def close(self):
        self.write(self._PORTFOLIO_DATA, self._PORTFOLIO_RANGE)

    # Update cells values in the google sheet
    def write(self, df, loc="A1:A:100", work_sheet=False):
        """

        :param data: [Dict] where the key is the column name, and def is the values
        :param loc: [tuple] Init cell to place data in google sheet ()
        :return:
        """

        if work_sheet is not False:
            range = work_sheet + "!" + loc
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

    #TODO delete if not used by May

    # def set_active_sheet(self, new_sheet=False):
    #         if new_sheet is False:
    #             self.active_sheet = self.sheet
    #         else:
    #             self.active_sheet = self.sheet.worksheet_by_title(new_sheet)


    def update_time(self):
        self.cur_time = time.ctime()
        temp = self.cur_time.split()
        self.cur_date = temp[1] + " " + temp[2] + " " + temp[4]
        self.cur_day = temp[0]
        self.cur_hour = temp[3].split(':')
        self.cur_hour = self.cur_hour[0]

    def Grab_sheet(self):

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

    def Create_Service(self, client_secret_file, api_service_name, api_version, *scopes):
        SCOPES = [scope for scope in scopes[0]]
        #print("SCOPES: " + SCOPES)


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
                #return service
        except Exception as e:
            print(e)
            #return None

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)






if __name__ == '__main__':

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


    # CONFIG ---------
    SAMPLE_SPREADSHEET_ID_input = '1Xl3l43zkO91ba1zSjhbfcqvx9HRm1uc3nRjSRP0ykFk'
    SAMPLE_RANGE_NAME = 'A1:D4'
    json_file = r'C:\Users\dunha\OneDrive\Documents\Google Oauth2 Keys\temp_oauth.json'

    # Create sheet
    gsheet = GoogleSheet(SAMPLE_SPREADSHEET_ID_input, json_file)

    # EXECUTE
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=gsheet.update)
    job.start()

    # MAIN LOOP
    while True:
        try:
            time.sleep(1)
        except ProgramKilled:
            print
            "Program killed: running cleanup code"
            job.stop()
            break

    gsheet.preopen_update()

    gsheet.close()


    # LEGACY
    """ g sheet write test """
    # data = [['Alex', 10], ['Bob', 12], ['Clarke', 13]]
    # df = pd.DataFrame(data, columns=['Name', 'Age'])
    # gsheet.write(df, 'A9:H100')




