import os
import pandas as pd
import logging
import datetime
import requests
import time

resolution = '5'

# directories
log_file_dir = './logs/fetch_missing_dates.log'
input_dir = "./output_5"
output_dir = "./output_5"
auth_config_file_dir = './auth/config.txt'
auth_access_token_file_dir = "./auth/access_token.txt"
verify_log_dir = './logs/verify.log'
fetch_missing_dates_log_fir = './logs/fetch_missing_dates.log'

# configure logging
logging.basicConfig(filename=log_file_dir, level=logging.INFO)

with open(auth_config_file_dir) as f:
    config = f.readlines()

client_id = config[0].split(' = ')[1].split('\n')[0]
secret_key = config[1].split(' = ')[1].split('\n')[0]
redirect_uri = config[2].split(' = ')[1].split('\n')[0]
response_type = config[3].split(' = ')[1].split('\n')[0]
grant_type = config[4].split(' = ')[1].split('\n')[0]
state = config[5].split(' = ')[1].split('\n')[0]
scope = config[6].split(' = ')[1].split('\n')[0]
nonce = config[7].split(' = ')[1].split('\n')[0]

resolution = "5"
app_id = client_id

with open(auth_access_token_file_dir) as f:
        access_token = f.readline()

endpoint = "https://api.fyers.in/data-rest/v2/history"
headers = {
    "Authorization": f"{app_id}:{access_token}",
    "Content-Type": "application/json"
}


def fetch_stock_data(stock, data):
    # data will contain only ONE date
    if data['range_from'] != data['range_to']:
        raise Exception(f"Different dates for in {stock}")
    response = requests.post(f'{endpoint}?symbol=NSE:{stock}{"-BE" if stock == "PATANJALI" else "-EQ"}&resolution={resolution}&date_format=0&range_from={data["range_from"]}&range_to={data["range_to"]}&cont_flag=1', headers=headers)

    # If the request was successful, parse the data and append it to the output file
    if response.status_code == 200:
        results = response.json()["candles"]
        rows = [[r[0], r[1], r[2], r[3], r[4], r[5]] for r in results]
        df = pd.DataFrame(rows, columns=["time", "open", "high", "low", "close", "volume"])
        return df
    else:
        date_str = datetime.datetime.fromtimestamp(data['from_date']).strftime('%Y-%m-%d')
        raise Exception(f"Error fetching data for {stock} {date_str}")

# parse log file to get missing data
log_file = verify_log_dir

verify_fetch_data_file = fetch_missing_dates_log_fir
verified_stocks_and_dates = {}

with open(verify_fetch_data_file, "r") as f:
    for line in f:
        if 'ERROR' not in line:
            split_line = line.split(':')
            date = split_line[2].split(' ')[3]
            stock = split_line[2].split(' ')[7].split('\\')[1].split('.')[0]
        if stock in verified_stocks_and_dates:
            verified_stocks_and_dates[stock].append(date)
        else:
            verified_stocks_and_dates[stock] = []
            verified_stocks_and_dates[stock].append(date)

with open(log_file, "r") as f:
    for line in f:
        epoch_times = []
        if "Missing candles for file:" in line:
            # extract stock file name
            stock = line.split(":")[-1].split('.')[0].strip()
        elif "Missing dates:" in line:
            # extract missing dates
            missing_dates = line.split(":")[-1].strip().split(', ')
            missing_dates = [item.replace("'", '').replace("[", '').replace("]", '') for item in missing_dates]
            missing_dates = [date for date in missing_dates if len(date) > 0]
            if not missing_dates:
                break
            for date_str in missing_dates:
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                epoch_time = int(date_obj.timestamp())
                if (stock not in verified_stocks_and_dates) or (date_str not in verified_stocks_and_dates[stock]):
                    epoch_times.append(epoch_time)


            # fetch missing data for each date and append to output file
            for epoch_time in epoch_times:
                try:
                    date_str = datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d')
                    data = {
                        "symbol": stock,
                        "resolution": resolution,
                        "date_format":"0",
                        "range_from": int(epoch_time),
                        "range_to": int(epoch_time),
                    }
                    # if date_str and stock are present in verify_fetch_log then skip
                    time.sleep(0.1)
                    data = fetch_stock_data(stock, data)

                    # append data to output file
                    output_file = os.path.join(output_dir, f"{stock}.csv")
                    if os.path.isfile(output_file):
                        # append to existing data
                        existing_data = pd.read_csv(output_file)
                        existing_data = pd.concat([existing_data, data], ignore_index=True)
                        existing_data = data.sort_values(by=["time"])
                        existing_data.to_csv(output_file, index=False)
                    else:
                        # create new file
                        logging.error(f"Creating new file {output_file}, this stock file did not exist!!!")
                        data.to_csv(output_file, index=False)

                    logging.info(f"Fetched data for {date_str} and added to {output_file}")
                except Exception as e:
                    logging.error(f"Error fetching data for {date_str} in {stock}: {e}")

# remove dates from verify.log for which data was fetched
updated_data = []
with open(log_file, "r") as f:
    for line in f:
        epoch_times = []
        if "Missing candles for file:" in line:
            # extract stock file name
            stock = line.split(":")[-1].split('.')[0].strip()
            updated_data.append(line.split('\n')[0])
        elif "Missing dates:" in line or "All fetched:" in line:
            # extract missing dates
            missing_dates = line.split(":")[-1].strip().split(', ')
            missing_dates = [item.replace("'", '').replace("[", '').replace("]", '') for item in missing_dates]
            missing_dates = set(missing_dates) - set(verified_stocks_and_dates[stock])
            missing_dates = [date for date in missing_dates if len(date) > 0]
            if not missing_dates:
                updated_data.append(f"All fetched: {list(missing_dates)}")
            else:
                updated_data.append(f"Missing dates: {list(missing_dates)}")


with open(log_file, "w") as f:
    updated_data = '\n'.join(updated_data)
    f.write(updated_data)
