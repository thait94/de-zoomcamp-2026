Homework 1

# Docker 

1. Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

What's the version of pip in the image?

    docker run -it --rm --entrypoint=bash python:3.13
    pip -V 

Version is 25.3

2. Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

    Since the two containers are on the same network, they can see each other. Therefore, pgadmin should connect to the postgres database with db:5432 because the second port number is one on the container within the network. 

3. For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

    SELECT COUNT(*) 
    FROM public.green_taxi_data
    WHERE "lpep_pickup_datetime" BETWEEN '2025-11-01' AND '2025-12-01'
    AND "trip_distance" <= 1.0

Answer: 8007 

4. Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

    SELECT "lpep_pickup_datetime", "trip_distance"
    FROM public.green_taxi_data
    WHERE "trip_distance" < 100.0
    ORDER BY "trip_distance" DESC
    LIMIT 1

Answer: 2025-11-14

5. Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

    SELECT "Zone", SUM("total_amount") 
    FROM public.green_taxi_data AS gt 
    JOIN public.taxi_zone_lookup AS tz
    ON gt."PULocationID" = tz."LocationID"
    WHERE date_trunc('day', "lpep_pickup_datetime")='2025-11-18'
    GROUP BY "Zone"
    ORDER BY SUM("total_amount") DESC
    LIMIT 1

Answer: East Harlem North

6. For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

    SELECT dropoff."Zone", "tip_amount"
    FROM public.green_taxi_data AS gt 
    JOIN public.taxi_zone_lookup AS pickup
    ON gt."PULocationID" = pickup."LocationID"
    JOIN public.taxi_zone_lookup AS dropoff
    ON gt."DOLocationID" = dropoff."LocationID"
    WHERE "lpep_pickup_datetime" BETWEEN '2025-11-01' AND '2025-12-01'
    AND pickup."Zone"='East Harlem North'
    ORDER BY "tip_amount" DESC
    LIMIT 1

Answer: Yorkville West

# Terraform 

Which of the following sequences, respectively, describes the workflow for:

    1. Downloading the provider plugins and setting up backend,
    2. Generating proposed changes and auto-executing the plan
    3. Remove all resources managed by terraform`

Answer: terraform init, terraform apply -auto-approve, terraform destroy