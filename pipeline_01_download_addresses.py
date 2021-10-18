"""
Extract Process #1

Download addresses data from the given web location. Save to a local file in a
folder named "data/". You will have to create the folder before you can add
files to it (you don't have to create the folder in Python ... but you can if
you want to: https://docs.python.org/3/library/os.html#os.mkdir)
"""

import datetime as dt
import requests

print('Downloading the addresses data...')
response = requests.get('https://storage.googleapis.com/mjumbewu_musa_509/lab04_pipelines_and_web_services/get_latest_addresses')

print('Saving addresses data to a file...')
outfile_path = f'data/addresses_{dt.date.today()}.csv'
with open(outfile_path, mode='wb') as outfile:
    outfile.write(response.content)

print('Done.')
