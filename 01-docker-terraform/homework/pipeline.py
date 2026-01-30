# grab read from the data files (parquet and csv)
# take that data and load it into postgresql db 
# use pgadmin to run queries 

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

greentrip_dtype = {
    "VendorID": "Int64",
    "store_and_fwd_flag": "string",
    "RatecodeID": "float64",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "ehail_fee": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "payment_type": "Int64",
    "trip_type": "float64",
    "congestion_surcharge": "float64",
    "cbd_congestion_fee": "float64"
}

parse_greentrip_dates = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]

taxizone_lookup_dtypes = {
    "LocationID": "Int64", 
    "Borough": "string", 
    "Zone": "string", 
    "service_zone": "string"
}

url = './data/green_tripdata_2025-11.parquet'
taxizone_lookup_df = pd.read_csv('./data/taxi_zone_lookup.csv')

def ingest_data():
    pg_user = 'root'
    pg_pass = 'root'
    pg_host = 'localhost'
    pg_port = 5432
    pg_db = 'ny_taxi'
    table_name = 'green_taxi_data'
    chunksize = 100000

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    greentrip_df_iter = pd.read_parquet(
        url, 
        dtype=greentrip_dtype,
        parse_dates=parse_greentrip_dates, 
        iterator=True, 
        chunksize=chunksize
    )

    first = True

    for df_chunk in tqdm(greentrip_df_iter):

        if first:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name=table_name,
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        df_chunk.to_sql(
            name=table_name,
            con=engine,
            if_exists="append"
        )





