from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import pandas as pd
from io import BytesIO
import boto3
from minio import Minio
from minio.error import S3Error

import pyarrow as pa
import pyarrow.parquet as pq

# Assuming you have a DataFrame named 'df' with the data you want to save
# Replace these values with your LocalStack S3 configuration
localstack_host = 'localhost:4566'
localstack_port = 4566
s3_bucket_name = 'my-example-bucket'
access_key = 'dummy-access-key'
secret_key = 'dummy-secret-key'

@data_exporter
def export_data_to_s3(df: DataFrame, **kwargs) -> None:

    # Convert DataFrame to CSV format in memory
    csv_data = df.to_csv(index=False).encode('utf-8')
    csv_buffer = BytesIO(csv_data)

    # Initialize Minio client
    minio_client = Minio(
        localstack_host,
        access_key=access_key,
        secret_key=secret_key,
        secure=False  # Use False for non-HTTPS connection
    )

    # Create S3 bucket if it doesn't exist
    if not minio_client.bucket_exists(s3_bucket_name):
        minio_client.make_bucket(s3_bucket_name)

    # Upload DataFrame CSV to the S3 bucket
    object_name = 'your-data.csv'  # Specify the desired object key
    try:
        minio_client.put_object(
            bucket_name=s3_bucket_name,
            object_name=object_name,
            data=csv_buffer,
            length=len(csv_data),
            content_type='application/csv'
        )
        print(f"DataFrame successfully uploaded to S3 bucket: {s3_bucket_name}/{object_name}")
    except S3Error as e:
        print(f"Error uploading DataFrame to S3: {e}")
    
    # Convert DataFrame to PyArrow Table
    table = pa.Table.from_pandas(df)

    # Write Parquet files partitioned by 'lpep_pickup_date' to S3 bucket
    pq.write_to_dataset(
        table,
        root_path='dataset_name_3',
        partition_cols=['lpep_pickup_date'],
        # filesystem='s3',
        use_legacy_dataset=False,
        compression='SNAPPY',  # Optional: specify compression type
    )

    print(len(pq.ParquetDataset('dataset_name_3').files))

    print(f'Data has been written to Parquet files in S3 bucket: {s3_bucket_name}/your-folder/')

    import subprocess

    # Replace the command with the one you want to run
    command = "aws --endpoint-url=http://localhost:4566 s3 cp dataset_name_3 s3://my-example-bucket --recursive"

    # Run the command
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True)

    # Replace the command with the one you want to run
    command = "rm dataset_name_3 -r"

    # Run the command
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True)