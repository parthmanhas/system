import pandas as pd
import os
import logging

resolution = '5'

verify_log_dir = './logs/verify.log'
output_dir = f'./output_{resolution}'


logging.basicConfig(filename=verify_log_dir, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Get list of all csv files in output directory
files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]

# assume public holidays are stored in a list called 'holidays'
holidays = [
    "2017-01-26",
    "2017-02-24",
    "2017-03-13",
    "2017-04-04",
    "2017-04-14",
    "2017-04-14",
    "2017-05-01",
    "2017-06-26",
    "2017-08-15",
    "2017-08-25",
    "2017-10-02",
    "2017-10-19",
    "2017-10-20",
    "2017-12-25",
    "2018-01-26",
    "2018-02-13",
    "2018-03-02",
    "2018-03-29",
    "2018-03-30",
    "2018-05-01",
    "2018-08-15",
    "2018-05-22",
    "2018-09-13",
    "2018-09-20",
    "2018-10-02",
    "2018-10-18",
    "2018-11-07",
    "2018-11-08",
    "2018-11-23",
    "2018-12-25",
    "2019-03-04",
    "2019-03-21",
    "2019-04-17",
    "2019-04-19",
    "2019-05-01",
    "2019-06-05",
    "2019-08-12",
    "2019-08-15",
    "2019-09-02",
    "2019-09-10",
    "2019-10-02",
    "2019-10-08",
    "2019-10-28",
    "2019-11-12",
    "2019-12-25",
    "2020-02-21",
    "2020-03-10",
    "2020-04-02",
    "2020-04-06",
    "2020-04-10",
    "2020-04-14",
    "2020-05-01",
    "2020-05-25",
    "2020-10-02",
    "2020-11-16",
    "2020-11-30",
    "2020-12-25",
    "2021-01-26",
    "2021-03-11",
    "2021-03-29",
    "2021-04-02",
    "2021-04-14",
    "2021-04-21",
    "2021-05-13",
    "2021-07-21",
    "2021-08-19",
    "2021-09-10",
    "2021-10-15",
    "2021-11-04",
    "2021-11-05",
    "2021-11-19",
    "2022-01-26",
    "2022-03-01",
    "2022-03-18",
    "2022-04-14",
    "2022-04-15",
    "2022-05-03",
    "2022-08-09",
    "2022-08-15",
    "2022-08-31",
    "2022-10-05",
    "2022-10-24",
    "2022-10-26",
    "2022-11-08",
    "2023-01-26",
    "2023-03-07",
    "2023-03-30",
    "2023-04-04",
    "2023-04-07",
    "2023-04-14",
    "2023-05-01",
    "2023-06-28",
    "2023-08-15",
    "2023-09-19",
    "2023-10-02",
    "2023-10-24",
    "2023-11-14",
    "2023-11-27",
    "2023-12-25"
]

# Loop through each file
for file in files:
    # Read csv file into a pandas dataframe
    df = pd.read_csv("output_5/" + file)
    df = pd.read_csv(f"{output_dir}/{file}")

    # Convert epoch time to date format
    df['date'] = pd.to_datetime(df['time'], unit='s').dt.date

    # filter out weekends
    df = df[pd.to_datetime(df['time']).dt.dayofweek < 5]

    # filter out public holidays
    df = df[~df['date'].isin(holidays)]

    # Group by date and count the number of rows for each date
    count_df = df.groupby('date')['time'].count().reset_index(name='count')

    # Get list of dates where the count is not equal to 75
    missing_dates = count_df[count_df['count'] != 75]['date'].tolist()

    formatted_dates = [date.strftime('%Y-%m-%d') for date in missing_dates]
    if missing_dates:
        logging.info(f"Missing candles for file: {file}")
        logging.info(f"Missing dates: {formatted_dates}")
