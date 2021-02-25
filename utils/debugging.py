from datetime import datetime
from inspect import getframeinfo, stack

global FILE_PATH
FILE_PATH = None

#strings to be printed in trace logs
DEBUG_TYPES = ['GOOG_UTL', 'MORN_UPD', 'REG_UPD', 'HOUR_UPD', 'AFT_UPD']

def print_debug(msg_type, msg, file_location=None, list=None):

    # Write to file if file has been passed
    if file_location is not None:
        global FILE_PATH
        FILE_PATH = file_location
    caller = getframeinfo(stack()[1][0])

    # Way to print list
    if list is None:
        l = ""
    else:
        l = list

    print_msg = str(datetime.now()) + "INVSTR DEBUG: %s %s Line: %d %s" % (msg_type, caller.filename.split("\\")[-1], caller.lineno, msg) + str(l)
    if msg_type in DEBUG_TYPES:
        print(print_msg)

    if FILE_PATH is not None:
        with open(FILE_PATH + "software_logs.txt", 'a') as f:
            f.write(print_msg + "\n")
            f.close()

