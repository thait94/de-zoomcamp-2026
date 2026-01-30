# 1. Read from the data files (parquet and csv)
# 2. Take that data and load it into postgresql db 
# 3. Use pgadmin to run queries 

# Note: Make sure to run docker-compose file to create volumes and then run the Dockerfile to reference this pipeline

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

taxizone_lookup_dtype = {
    "LocationID": "Int64", 
    "Borough": "string", 
    "Zone": "string", 
    "service_zone": "string"
}

def ingest_data():
    location = './data/green_tripdata_2025-11.parquet'
    pg_user = 'root'
    pg_pass = 'root'
    pg_host = 'localhost'
    pg_port = 5432
    pg_db = 'ny_taxi'
    taxi_table = 'green_taxi_data'
    lookup_table = 'taxi_zone_lookup'
    chunksize = 100000

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Create a dataframe for taxi zone lookup data
    taxizone_lookup_df = pd.read_csv('./data/taxi_zone_lookup.csv', header=0, dtype=taxizone_lookup_dtype, engine=engine)

    # Load the header to the db 
    taxizone_lookup_df.head(0).to_sql(
        name=lookup_table, 
        con=engine, 
        if_exists="replace"
    )

    # Load the rest of the data to the db 
    taxizone_lookup_df.to_sql(
        name=lookup_table, 
        con=engine, 
        if_exists="append"
    )

    # Create an iterator for green trip data
    greentrip_df_iter = pd.read_parquet(
        location, 
        dtype=greentrip_dtype,
        parse_dates=parse_greentrip_dates, 
        iterator=True, 
        chunksize=chunksize
    )

    first = True

    # Loop through iterator and add data to db 
    for greentrip_chunk in tqdm(greentrip_df_iter):

        if first:
            # Create table schema (no data)
            greentrip_chunk.head(0).to_sql(
                name=taxi_table,
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        greentrip_chunk.to_sql(
            name=taxi_table,
            con=engine,
            if_exists="append"
        )

if __name__ == '__main__':
    ingest_data()





