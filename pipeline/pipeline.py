import sys
import pandas as pd

print("These are the arguments", sys.argv)

month = int(sys.argv[1])
print(f"Running pipeline for month {month}")

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
print(df.head())

df.to_parquet(f"output_month_{sys.argv[1]}.parquet")