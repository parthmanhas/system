import os
import pandas as pd
from multiprocessing import Pool
import time
import logging

resolution = '5' 

sort_by_date_log_dir = './logs/sort_by_date.log'
output_dir = f'./output_{resolution}'

start = time.time()
# set up logging
logging.basicConfig(filename=sort_by_date_log_dir, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


# Set the number of worker processes to the number of available CPUs
NUM_WORKERS = os.cpu_count()


def remove_duplicates(filename):
    # Read CSV file and sort by time
    df = pd.read_csv(f'{output_dir}/{filename}')
    df = df.sort_values(by=["time"])

    # Write cleaned data back to the same CSV file
    df.to_csv(f'{output_dir}/{filename}', index=False)

    # Log the filename and time taken to sort
    print(f"{filename}: Sorted by date in {time.time()-start:.2f} seconds")
    logging.info(f"{filename}: Sorted by date in {time.time()-start:.2f} seconds")


if __name__ == "__main__":
    import time

    start = time.time()

    # Get list of CSV files in the output directory
    file_list = os.listdir(output_dir)
    csv_files = [file for file in file_list if file.endswith('.csv')]

    # Create a Pool of worker processes to remove duplicates
    with Pool(NUM_WORKERS) as p:
        p.map(remove_duplicates, csv_files)

    # Log the time taken to sort all by date
    print(f"Sorted by date all files in {time.time()-start:.2f} seconds")
    logging.info(f"Sorted by date all files in {time.time()-start:.2f} seconds")
