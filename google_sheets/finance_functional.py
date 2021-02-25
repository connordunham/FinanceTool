import pandas as pd
import time
from FinanceTool.google_sheets.access_sheet import GoogleSheet
from FinanceTool.utils.sheet_ranges import SHEET_RANGES
from FinanceTool.utils.constants import TRADING_DAYS, NON_TRADING_DAYS # TODO create new python file with these constants


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
        
        # Flags
        self.weekly_update_flag = False
        self.preopen_flag = False
        self.closing_flag = False

        self.update_time()



        print(self.cur_hour)

        self.weekly_chg_tracker = {"Portfolio Holdings": "A50:H"}

    # Updates the neccassary parts of spread sheet every 10 minutes
    def update(self):
        # Update time variables
        self.update_time()
        # Update flag variables
        self.set_flags()

        if self.cur_hour > 9 and self.preopen_flag:
            self.preopen_update()
            
        if self.curhour > 5 and self.close_flag:
            self.close_

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
        
        #Reset preopen flag
        self.preopen_flag = False
        print('Premarket update completed at: ' + self.cur_time)
        
    def closing_update(self):
        data =  self.read(SHEET_RANGES['Historic']['DAILY_READ'], sheet="Historic")Historic
        historic_data_daily_headers = data[0]
        historic_data_daily_data = data[1:]
        #TODO parse this data and add a new
        self.write(historic_data_daily, SHEET_RANGES['Historic']['DAILY_WRITE'] #TODO see if his data needs to convert to pandas df
   
        #TODO update other charts and areas at end of day
        #RESET close flag
        self.close_flag = Flase
   
              
        
        

    # Calculate porfolio value by summings current holdings
    def calc_port_value(self):

        for ticker in self._PORTFOLIO_DATA['Stock']:
            print(ticker)
            #TODO add porfolio value calculation


    def close(self):
        self.write(self._PORTFOLIO_DATA, SHEET_RANGES['portfolio_holdings']['CURRENT_HOLDINGS'])

    def set_flags(self):
        # Set premarket update flag if its a trading day
        # if self.cur_day is in TRADING_DAYS and self.cur_time < 8 and self.cur_day is not in NON_TRADING_DAYS:
        if self.cur_day is in TRADING_DAYS and self.cur_time < 8:
            
            # Set premarket  update flag
            self.preopen_flag = True
            self.closing_flag = True
            
            # Set weekly update flag after hours on Friday
            if self.cur_day == 'Fri':
                self.weekly_update_flag = True
            
            
         
    
    def update_time(self):
        self.cur_time = time.ctime()
        temp = self.cur_time.split()
        self.cur_date = temp[1] + " " + temp[2] + " " + temp[4]
        self.cur_year = int(temp[4])
        self.cur_day = temp[0]
        # Further parsing to get the current hour
        self.cur_hour = temp[3].split(':')
        self.cur_hour = int(self.cur_hour[0])

    def read( self, sheet_range, sheet=None ):
        data = self.GOOGLE_SHEET.read(sheet_range, sheet=sheet)
        return data[0]

    def write( self,  df, loc="A1:A:100", sheet=False ):
        self.GOOGLE_SHEET.write(df, loc=loc, sheet=sheet)



