#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[21]:


prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
file_name = 'yellow_tripdata_2021-01.csv.gz'
url = prefix + file_name
df = pd.read_csv(url, nrows=100)


# In[10]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates
)


# In[15]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[17]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[18]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[22]:


df_iter = pd.read_csv(
    url, 
    dtype=dtype,
    parse_dates=parse_dates, 
    iterator=True, 
    chunksize=100000
)


# In[30]:


from tqdm.auto import tqdm


# In[31]:


first = True

for df_chunk in tqdm(df_iter):

    if first:
        # Create table schema (no data)
        df_chunk.head(0).to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="replace"
        )
        first = False
        print("Table created")

    # Insert chunk
    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )

    print("Inserted:", len(df_chunk))

