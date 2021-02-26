# Ref link useful finance tools in python: https://www.activestate.com/blog/top-10-python-packages-for-finance-and-financial-modeling/
import pandas as pd
import numpy as np
import pyfolio
#from zipline.api import order_target_percent, record, symbol, set_benchmark, get_open_orders
from datetime import datetime
import pytz


# def initialize(context):
#     context.i = 0
#     context.asset = symbol('AAPL')
#     set_benchmark(symbol('AAPL'))

#
# def handle_data(context, data):
#     # Skip first 200 days to get full windows
#     context.i += 1
#     if context.i < 200:
#         return
#     # Compute averages
#     # data.history() has to be called with the same params
#     # from above and returns a pandas dataframe.
#     short_mavg = data.history(context.asset, 'price', bar_count=50, frequency="1d").mean()
#     long_mavg = data.history(context.asset, 'price', bar_count=200, frequency="1d").mean()
#
#     # Trading logic
#     open_orders = get_open_orders()
#
#     if context.asset not in open_orders:
#         if short_mavg > long_mavg:
#             # order_target orders as many shares as needed to
#             # achieve the desired number of shares.
#             order_target_percent(context.asset, 1.0)
#         elif short_mavg < long_mavg:
#             order_target_percent(context.asset, 0.0)
#
#     # Save values for later inspection
#     record(AAPL=data.current(context.asset, 'price'),
#            short_mavg=short_mavg,
#            long_mavg=long_mavg)

def list_to_df(data, headers):
    return pd.DataFrame(data, columns=headers)
