import os
import csv
from datetime import datetime, timedelta
import requests
import schedule
import time
import logging
import schedule
import time

resolution = "5"

# go back one direcotry
os.chdir('..')

# directories
auth_config_dir = 'auth/config.txt'
fetch_log_dir = 'logs/fetch.log'
stocks_dir = 'fetch/stocks.txt'
auth_access_token_dir = "auth/3_access_token.txt"
output_dir = f"output_{resolution}"
failed_stocks_log_dir = 'logs/failed_stocks.log'


with open(auth_config_dir) as f:
    config = f.readlines()

client_id = config[0].split(' = ')[1].split('\n')[0]
secret_key = config[1].split(' = ')[1].split('\n')[0]
redirect_uri = config[2].split(' = ')[1].split('\n')[0]
response_type = config[3].split(' = ')[1].split('\n')[0]
grant_type = config[4].split(' = ')[1].split('\n')[0]
state = config[5].split(' = ')[1].split('\n')[0]
scope = config[6].split(' = ')[1].split('\n')[0]
nonce = config[7].split(' = ')[1].split('\n')[0]


app_id = client_id

logging.basicConfig(filename=fetch_log_dir, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data():
    # Load the stock symbols from the text file
    with open(stocks_dir, "r") as f:
        stocks = [line.strip() for line in f.readlines()]
    
    with open(auth_access_token_dir) as f:
        access_token = f.readline()

    # Set the date range to fetch data for
    start_date = datetime(2017, 7, 3)
    end_date = datetime.now()
    interval = timedelta(days=99)

    # Set the API endpoint and header
    endpoint = "https://api.fyers.in/data-rest/v2/history"
    headers = {
        "Authorization": f"{app_id}:{access_token}",
        "Content-Type": "application/json"
    }

    # Check if the output directory exists, if not create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through the stock symbols and fetch the data
    failed_stocks = []
    for stock in stocks:
        end_date = datetime.now()
        print(f"Fetching data for {stock}...")

        # Create the output CSV file for this stock
        output_file = os.path.join(output_dir, f"{stock}.csv")

        # Check if the file already exists and if so, load the last date
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                reader = csv.reader(f)
                last_row = list(reader)[-1]
                last_date = datetime.fromtimestamp(int(last_row[0]))
        else:
            last_date = start_date - interval

        # Loop through the date range and fetch data for each interval
        from_date = last_date
        to_date = from_date + interval

        if end_date.weekday() == 5 and last_date.weekday() == 4: # 5 corresponds to Saturday
            end_date = end_date + timedelta(days=2)
            last_date = end_date
        elif end_date.weekday() == 6 and last_date.weekday() == 4: # 6 corresponds to Sunday
            end_date = end_date + timedelta(days=1)
            last_date = end_date

        while last_date < end_date:
            # Fetch the data for this interval
            time.sleep(0.1)
            data = {
                "symbol": stock,
                "resolution": resolution,
                "date_format":"0",
                "range_from": int(from_date.timestamp()),
                "range_to": int(to_date.timestamp()),
            }
            response = requests.post(f'{endpoint}?symbol=NSE:{stock}{"-BE" if stock == "PATANJALI" else "-EQ"}&resolution={resolution}&date_format=0&range_from={data["range_from"]}&range_to={data["range_to"]}&cont_flag=1', headers=headers)

            # If the request was successful, parse the data and append it to the output file
            if response.status_code == 200:
                results = response.json()["candles"]
                rows = [[r[0], r[1], r[2], r[3], r[4], r[5]] for r in results]

                # Append rows to the output CSV file
                with open(output_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    if last_date == start_date - interval:
                        # Write headers if the file was just created
                        writer.writerow(["time", "open", "high", "low", "close", "volume"])
                    writer.writerows(rows)

                last_date = to_date
            else:
                # If the request failed, log the stock symbol and move on to the next stock
                print(f"Failed to fetch data for {stock}.")
                failed_stocks.append({
                    'name': stock,
                    'reason': response.json()['message']
                })
                break

            from_date = last_date + interval
            to_date = min(from_date + interval, end_date)

    # Log the failed stocks to a file
    if failed_stocks:
        with open(failed_stocks_log_dir, "a") as f:
            f.write(f"\nFailed to fetch data for {len(failed_stocks)} stocks:\n")
            for stock in failed_stocks:
                f.write(f"{stock['name']} {stock['reason']}\n")
    else:
        print("All stocks fetched successfully.")


fetch_data()
# schedule the task to run every day at 9pm
# schedule.every().day.at("21:00").do(fetch_data)

# while True:
#     # run pending scheduled tasks
#     schedule.run_pending()
#     time.sleep(1)
