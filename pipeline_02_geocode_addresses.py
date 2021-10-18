"""
Extract Process #2

Use the Census Geocoding API to geocode the addresses in the file that was
extracted in step one. The documentation for the API is available at:

https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf

I encourage you to read it for details, but the gist is:
- You can geocode a batch of addresses by sending a POST request to
  https://geocoding.geo.census.gov/geocoder/geographies/addressbatch
- The request should contain the following context:
    1. A parameter named "benchmark" (set the value to "Public_AR_Current")
    2. A parameter named "vintage" (set the value to "Current_Current")
    3. A file labeled "addressFile" with the format described at
       https://www.census.gov/programs-surveys/locations/technical-documentation/complete-technical-documentation/census-geocoder.html#ti103804043
       (the file you downloaded in the previous step should conform to that
       format).

Save the geocoded data to a new file.
"""

import datetime as dt
import requests

print('Opening the addresses data...')
infile_path = f'data/addresses_{dt.date.today()}.csv'
with open(infile_path, mode='rb') as opened_file:
    print('Geocoding the addresses data...')
    response = requests.post(
        'https://geocoding.geo.census.gov/geocoder/geographies/addressbatch',
        data={
            'benchmark': 'Public_AR_Current',
            'vintage': 'Current_Current',
        },
        files={
            'addressFile': opened_file,
        })

print('Saving geocoded data to a file...')
outfile_path = f'data/geocoded_addresses_{dt.date.today()}.csv'
with open(outfile_path, mode='wb') as outfile:
    outfile.write(response.content)

print('Done.')
