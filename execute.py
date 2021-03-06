from google_sheets.finance_functional import FinanceTool
from datetime import timedelta
import time
from utils.threading import  WAIT_TIME_MINS, WAIT_TIME_SECONDS
from utils.threading import ProgramKilled, signal_handler, Job


def main():
    # ______CONFIG________
    JSON_FILE = r'C:\Users\dunha\OneDrive\Documents\Google Oauth2 Keys\client_secret_214644974504-bqknepannatov47c18t9amh49jj9mpa0.apps.googleusercontent.com.json'
    JSON_FILE = r'C:\Users\dunha\OneDrive\Documents\Google Oauth2 Keys\temp_oauth.json'


    GOOG_SHT_ID = '1Xl3l43zkO91ba1zSjhbfcqvx9HRm1uc3nRjSRP0ykFk'

    MAIN_OBJ = FinanceTool(GOOG_SHT_ID, JSON_FILE)

    # EXECUTE
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=MAIN_OBJ.update)
    job.start()
    c = 20
    # MAIN LOOP
    while True:
        try:
            time.sleep(2)
            c += 1
            h = c%24
            print("Hour is %d" % h)
            MAIN_OBJ.cur_hour = h


        except ProgramKilled:
            print
            "Program killed: running cleanup code"
            job.stop()
            break

if __name__ == '__main__':
    main()