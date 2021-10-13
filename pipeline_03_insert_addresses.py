"""
Load Process

Take the files that we've created and load them both into the database. You
should end up with two tables: addresses and geocoded_address_results.
"""

import pandas as pd
import sqlalchemy as sqa

db = sqa.create_engine(...)

addresses_column_names = [
    'address_id',
    'street_address',
    'city',
    'state',
    'zip',
]
addresses_df = pd.read_csv(..., names=addresses_column_names)
addresses_df.to_sql('addresses', db, index=False, if_exists='replace')

geocoded_column_names = [
    'address_id',
    'input_address',
    'match_status',
    'match_type',
    'matched_address',
    'lon_lat',
    'tiger_line_id',
    'tiger_line_side',
]
geocoded_df = pd.read_csv(..., names=geocoded_column_names)
geocoded_df.to_sql('geocoded_address_results', db, index=False, if_exists='replace')
