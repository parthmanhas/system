import pandas as pd
import numpy as np
import time
import datetime
import glob
import os
import time
import math
import sys

resolution = '5'

# directories
output = f'output_{resolution}'

file = r'D:\strats\python\data\5_min\ASIANPAINT.csv'
df = pd.read_csv(file)
df['time'] = df['time'].apply(lambda x : datetime.datetime.fromtimestamp(x))
df['date'] = df['time'].apply(lambda x : x.date().strftime('%Y-%m-%d'))
df['time'] = df['time'].apply(lambda x : x.time().strftime('%H:%M:%S'))
df = df[['date', 'time', 'open', 'high', 'low', 'close', 'volume']]

# Define a function to determine if a candle is an inside candle
def is_inside_candle(row):
    if row['high'] <= row['prev_candle_high'] and row['low'] >= row['prev_candle_low']:
        return True
    else:
        return False

# Calculate the previous candle high and low for each row
df['prev_candle_high'] = df['high'].shift(1)
df['prev_candle_low'] = df['low'].shift(1)

# Determine if each candle is an inside candle
df['is_inside_candle'] = df.apply(is_inside_candle, axis=1)

# Define the signal to be long if the current candle is an inside candle and the previous candle was bullish, short if the current candle is an inside candle and the previous candle was bearish, and flat otherwise
df['signal'] = 'flat'
df.loc[(df['is_inside_candle']) & (df['close'] > df['open'].shift(1)), 'signal'] = 'long'
df.loc[(df['is_inside_candle']) & (df['close'] < df['open'].shift(1)), 'signal'] = 'short'

# danger
# df = df.dropna(subset=df.columns.values)

# Calculate the returns of the strategy
df['return'] = df['signal'].shift(1) * (df['close'] - df['close'].shift(1))

# Calculate the cumulative returns of the strategy
df['cum_return'] = df['return'].cumsum()

# Print the cumulative returns of the strategy
print(df['cum_return'].iloc[-1])