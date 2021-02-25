import pandas as pd
import time
from FinanceTool.google_sheets.access_sheet import GoogleSheet
from FinanceTool.utils.sheet_ranges import SHEET_RANGES


class FinanceTool:

    global values_input, service


    def __init__(self, ID, JSON):
        """

        :param ID: Id for sheet found in sheet url
        :param JSON: directory to JSON file from google api
        """
        self._TERMINATE = False

        self.GOOGLE_SHEET = GoogleSheet(ID, JSON)

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

        self.write(self._PORTFOLIO_DATA, SHEET_RANGES['portfolio_holdings']['CURRENT_HOLDINGS'])

        # Write latest update time
        time = pd.DataFrame([self.cur_time], columns=["Time Last Updated"])
        self.write(time, "J1:J2", "Portfolio Holdings")


    # Updates neccassry fields of spread sheet at 9:00am
    def preopen_update(self):

        print(SHEET_RANGES['Portfolio_Holdings']['CURRENT_HOLDINGS'])

        data = self.read(SHEET_RANGES['Portfolio_Holdings']['CURRENT_HOLDINGS'], sheet="Portfolio Holdings")
        main_table_headers = data[0]
        main_table = data[1:]

        self._PORTFOLIO_DATA = pd.DataFrame(main_table, columns=main_table_headers)
        self.num_stocks_held = len(main_table)
        self.opening_value = self.calc_port_value()

        print('Premarket update completed at: ' + self.cur_time)

    def calc_port_value(self):

        for ticker in self._PORTFOLIO_DATA['Stock']:
            print(ticker)


    def close(self):
        self.write(self._PORTFOLIO_DATA, SHEET_RANGES['portfolio_holdings']['CURRENT_HOLDINGS'])



    def update_time(self):
        self.cur_time = time.ctime()
        temp = self.cur_time.split()
        self.cur_date = temp[1] + " " + temp[2] + " " + temp[4]
        self.cur_day = temp[0]
        self.cur_hour = temp[3].split(':')
        self.cur_hour = self.cur_hour[0]

    def read( self, sheet_range, sheet=None ):
        self.GOOGLE_SHEET.read(sheet_range, sheet=sheet)

    def write( self,  df, loc="A1:A:100", sheet=False ):
        self.GOOGLE_SHEET.write(df, loc=loc, sheet=sheet)



