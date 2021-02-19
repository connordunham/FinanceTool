from google_sheets.finance_functional import FinanceTool
from datetime import timedelta, time
from utils.threading import  WAIT_TIME_MINS, WAIT_TIME_SECONDS
from utils.threading import ProgramKilled, signal_handler, Job


def run():
    # ______CONFIG________

    JSON_FILE = r'C:\Users\dunha\OneDrive\Documents\Google Oauth2 Keys\temp_oauth.json'
    GOOG_SHT_ID = '1Xl3l43zkO91ba1zSjhbfcqvx9HRm1uc3nRjSRP0ykFk'

    MAIN_OBJ = FinanceTool(GOOG_SHT_ID, JSON_FILE)

    # EXECUTE
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=FinanceTool.update)
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

    FinanceToolObj = FinanceTool()


if __name__ == '__main__':
    run()