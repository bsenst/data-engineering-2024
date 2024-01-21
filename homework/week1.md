
# Module 1 Homework: Docker & SQL

## Question 1. Knowing docker tags

`docker run --help`

```
...
  -q, --quiet                          Suppress the pull output
      --read-only                      Mount the container's root filesystem as read only
      --restart string                 Restart policy to apply when a container exits (default "no")
      --rm                             Automatically remove the container when it exits
      --runtime string                 Runtime to use for this container
      --security-opt list              Security Options
...
```

## Question 2. Understanding docker first run

`docker run -it --entrypoint /bin/bash python:3.9`

```
pip list
Package    Version
---------- -------
pip        23.0.1
setuptools 58.1.0
wheel      0.42.0
```

`# exit`

## Prepare Postgres

```
docker run -d \
  --name postgres-container \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_DB=mydatabase \
  -v ./data:/docker-entrypoint-initdb.d \
  -p 5432:5432 \
  postgres:latest
```

```
cd data
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz
wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
gunzip green_tripdata_2019-09.csv.gz
cd ..
```

`docker run -it --rm --link postgres-container:postgres postgres psql -h postgres -U myuser -d mydatabase`

```
Password for user myuser: 
psql (16.1 (Debian 16.1-1.pgdg120+1))
Type "help" for help.
mydatabase=# 
```

```
-- Create table for taxi zone lookup
CREATE TABLE taxi_zone_lookup (
    LocationID INT,
    Borough TEXT,
    Zone TEXT,
    service_zone TEXT
);
```

```
-- Create table for green taxi trips
CREATE TABLE green_taxi_trips (
    VendorID INT,
    lpep_pickup_datetime TIMESTAMP,
    lpep_dropoff_datetime TIMESTAMP,
    store_and_fwd_flag CHAR(1),
    RatecodeID INT,
    PULocationID INT,
    DOLocationID INT,
    passenger_count INT,
    trip_distance DOUBLE PRECISION,
    fare_amount DOUBLE PRECISION,
    extra DOUBLE PRECISION,
    mta_tax DOUBLE PRECISION,
    tip_amount DOUBLE PRECISION,
    tolls_amount DOUBLE PRECISION,
    ehail_fee DOUBLE PRECISION,
    improvement_surcharge DOUBLE PRECISION,
    total_amount DOUBLE PRECISION,
    payment_type INT,
    trip_type INT,
    congestion_surcharge DOUBLE PRECISION
);
```

Once connected, you can use the \dt command to list all tables:
`\dt`

Alternatively, you can also use a SQL query:
```
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

```
COPY green_taxi_trips FROM '/docker-entrypoint-initdb.d/green_tripdata_2019-09.csv' WITH CSV HEADER;
COPY taxi_zone_lookup FROM '/docker-entrypoint-initdb.d/taxi+_zone_lookup.csv' WITH CSV HEADER;
```

## Question 3. Count records

```
SELECT COUNT(*)
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) = '2019-09-18' AND DATE(lpep_dropoff_datetime) = '2019-09-18';
```

## Question 4. Largest trip for each day

```
SELECT DATE(lpep_pickup_datetime) AS pickup_day, MAX(trip_distance) AS max_trip_distance
FROM green_taxi_trips
GROUP BY pickup_day
ORDER BY max_trip_distance DESC
LIMIT 1;
```

## Question 5. Three biggest pick up Boroughs

```
SELECT
    tzl.borough,
    SUM(gt.total_amount) AS total_amount_sum
FROM
    green_taxi_trips gt
JOIN
    taxi_zone_lookup tzl ON gt.PULocationID = tzl.LocationID
WHERE
    DATE(gt.lpep_pickup_datetime) = '2019-09-18'
    AND tzl.borough <> 'Unknown'
GROUP BY
    tzl.borough
HAVING
    SUM(gt.total_amount) > 50000
ORDER BY
    total_amount_sum DESC
LIMIT 3;
```

## Question 6. Largest tip

```
WITH AstoriaPickups AS (
    SELECT
        tzl_pickup.zone AS pickup_zone,
        tzl_dropoff.zone AS dropoff_zone,
        SUM(gt.tip_amount) AS total_tip_amount
    FROM
        green_taxi_trips gt
    JOIN
        taxi_zone_lookup tzl_pickup ON gt.PULocationID = tzl_pickup.LocationID
    JOIN
        taxi_zone_lookup tzl_dropoff ON gt.DOLocationID = tzl_dropoff.LocationID
    WHERE
        DATE(gt.lpep_pickup_datetime) >= '2019-09-01'
        AND DATE(gt.lpep_pickup_datetime) <= '2019-09-30'
        AND tzl_pickup.zone = 'Astoria'
    GROUP BY
        tzl_pickup.zone, tzl_dropoff.zone
)
SELECT
    pickup_zone AS astoria_pickup_zone,
    dropoff_zone,
    total_tip_amount
FROM
    AstoriaPickups
ORDER BY
    total_tip_amount DESC;
```

## Question 7. Creating Resources

https://docs.localstack.cloud/getting-started/installation/

```
$ localstack --version
3.0.2
```

`localstack start`

https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

`pip install terraform-local`

```
cd terraform
tflocal init
tflocal apply
```