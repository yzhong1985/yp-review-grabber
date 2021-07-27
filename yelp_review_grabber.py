import sys
import argparse

# for testing purposes
def display_info():
    print("starting_index: ", start_idx)
    print("ending_index: ", end_index)
    print("time_interval: ", time_interval)
    print("wait_between_batch: ", wait_between_batch)
    print("source_filepath: ", source_filepath)
    print("proxy_used: ", proxy_used)

LOG_FILE_PATH = 'worklog.txt' # output log path

num_in_file = 5 # defines how many business should be stored in a file and output (1 batch)
time_interval = 60  # defines the time interval between request (a random +/-5 seconds will be applied to the value)
wait_between_batch = 0 # defines how long the program should wait until next batch
output_folder = 'output/'
proxy_used = ''

start_idx = 0
end_index = -1
source_filepath = ''

# arguments setting
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--start", required=True, type=int, help="specify the starting index. Note:index starts from 0")
ap.add_argument("-e", "--end", type=int, help="specify the ending index")
ap.add_argument("-n", "--n_in_batch", type=int, default=5, help="how many business should be stored in a file and output (1 batch)")
ap.add_argument("-t", '--time', type=int, default=60, help="defines the time interval between request (in seconds)")
ap.add_argument("-w", '--wait', type=int, default=0, help="defines the wait time between batches (in seconds)")
ap.add_argument("-f", "--filepath", default='SBRC_Doctor_Reviews.csv', help='specifiy the input source file')
ap.add_argument("-p", "--proxy", default="", help="specify the proxy number and port, if used, e.g 1.1.1.1:800" )
args = vars(ap.parse_args())

# # get the starting index 
start_idx = args["start"]

# the ending index, if not supplied, will be the last index of the file
if args.get("end", False):
    end_index = args["end"]
    if end_index < start_idx:
        raise Exception('the ending index need to be grearter than starting index')

# get the time interval between request
if args.get("n_in_batch", False):
    num_in_file = args["n_in_batch"]

# get the time interval between request
if args.get("time", False):
    time_interval = args["time"]

# get the time interval between request
if args.get("wait", False):
    wait_between_batch = args["wait"]

# get the filepath
if args.get("filepath", False):
    source_filepath = args["filepath"]

# get proxy
if args.get("proxy", False):
    proxy_used = args["proxy"]


display_info()

from grabber_request import *
import pandas as pd
import datetime
import time 

# get the page main url from source file
df = pd.read_csv(source_filepath)

total_bcount = len(df)
if end_index == -1 | end_index > total_bcount:
    end_index = total_bcount

all_err_files = []

for i in range(start_idx, end_index+1, num_in_file):
    url_df = df[['Business ID ', 'URL']].iloc[i:i+num_in_file]
    all_reviews_infile = []
    
    for index, row in url_df.iterrows():
        try:
            b_id = row['Business ID ']
            b_url = row['URL']
            print('grabber starts to work on business: ' , b_id)
            b_reviews = get_business_reviews(b_id, b_url, time_interval, proxy_used)
            print(b_reviews[0], ' reviews retreived for this business: ' , b_id)
            all_reviews_infile = all_reviews_infile + b_reviews[1]
        except:
            print("Unexpected error:", sys.exc_info()[0], ' ', sys.exc_info()[1], ' ', sys.exc_info()[2])
            all_err_files.append([row['Business ID '], row['URL']])
    
    if len(all_reviews_infile) > 0:
        df_output = pd.DataFrame(all_reviews_infile)
        #df_output.columns = ['business_id', 'user_name', 'rating', 'review_date', 'review']
        output_csv_path = output_folder + str(i) + '-' + str(i+num_in_file-1) + '.csv'
        df_output.to_csv(output_csv_path, encoding='utf-8', index=False)
        print('output file ' , output_csv_path, 'was generated') # should add timestamp

    time.sleep (wait_between_batch) # add a wait time

# if err, output a log file
if len(all_err_files) > 0:
    df_err = pd.DataFrame(all_err_files)
    now = datetime.datetime.now()
    err_path = output_folder + 'ErrorLog_' + now.strftime('%Y-%m-%dT%H-%M-%S') + '.csv'
    df_err.to_csv(err_path, encoding='utf-8')




