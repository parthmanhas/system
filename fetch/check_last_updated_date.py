import pandas as pd
import os
import logging
import datetime

resolution = '5'

last_updated_log_dir = './logs/last_updated.log'
output_dir = f'./output_{resolution}'


logging.basicConfig(filename=last_updated_log_dir, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Get list of all csv files in output directory
files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]

# Loop through each file
for file in files:
    # Read csv file into a pandas dataframe
    df = pd.read_csv(f"{output_dir}/{file}")
    last_candle_time = df.tail(1)['time']
    logging.info(f"Last candle for stock:{file.split('.')[0]} is epoch:{last_candle_time}, str:{datetime.datetime.fromtimestamp(last_candle_time).strftime('%Y-%m-%d')}")

    # last candle convert to datetime obj
    # add 1 to it
    # if it is saturday do not run
    # if it is sunday do not run
    # if it is monday run, from_range = monday date, to_range = monday_date
        
