# 1. Read from the data files (parquet and csv)
# 2. Take that data and load it into postgresql db 
# 3. Use pgadmin to run queries 

# Note: Make sure to run docker-compose file to create volumes and then run the Dockerfile to reference this pipeline
# The docker-compose file will create a network by default named as [folder_name]_default 
# Make sure to run these commands below with that network name 
# Then docker build -t docker-hw:1.0 .
# Then docker run -it --rm --network=homework_default docker-hw:1.0

import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from tqdm.auto import tqdm

pg_user = 'root'
pg_pass = 'root'
pg_host = 'pgdatabase'
pg_port = 5432
pg_db = 'ny_taxi'
engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

def ingest_csv():

    table_name = 'taxi_zone_lookup'
    
    taxizone_lookup_dtype = {
        "LocationID": "Int64", 
        "Borough": "string", 
        "Zone": "string", 
        "service_zone": "string"
    }

    # Create a dataframe for taxi zone lookup data
    taxizone_lookup_df = pd.read_csv(
        './data/taxi_zone_lookup.csv', 
        header=0, 
        dtype=taxizone_lookup_dtype
    )

    # Load the header to the db 
    taxizone_lookup_df.head(0).to_sql(
        name=table_name, 
        con=engine, 
        if_exists="replace"
    )

    # Load the rest of the data to the db 
    taxizone_lookup_df.to_sql(
        name=table_name, 
        con=engine, 
        if_exists="append"
    )


def ingest_parquet(): 
    table_name = 'green_taxi_data'
    location = './data/green_tripdata_2025-11.parquet'

    first = True
    greentrip_pq = pq.ParquetFile(location)

    for batch in greentrip_pq.iter_batches(10000):
        batch_df = batch.to_pandas()

        if first:
            batch_df.head(0).to_sql(
                name=table_name,
                con=engine,
                if_exists='replace'
            )
            first = False

        batch_df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append'
        )


        

if __name__ == '__main__':
    ingest_csv()
    ingest_parquet()




