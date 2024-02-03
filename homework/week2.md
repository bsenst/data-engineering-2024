# Module 2: ETL Pipeline

The Mage project is located in the `taxi` folder. Run the `green_taxi_etl` pipeline with the following command:

`mage run taxi green_taxi_etl`

```
@bsenst ➜ /workspaces/data-engineering-2024 (main) $ mage run taxi green_taxi_etl
...
(266855, 20)
...
(139370, 20)
df['lpep_pickup_date'] = df['lpep_pickup_datetime'].dt.date
...
{'PULocationID', 'RatecodeID', 'DOLocationID', 'VendorID'}
[2. 1.]
...
Postgres initialized
├─ Opening connection to PostgreSQL database...DONE
└─ Exporting data to 'mage.green_taxi'...
DataFrame successfully uploaded to S3 bucket: my-example-bucket/your-data.csv
95
Data has been written to Parquet files in S3 bucket: my-example-bucket/your-folder/
DONE

Pipeline run completed.
```
