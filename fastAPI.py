from fastapi import FastAPI, UploadFile, File, HTTPException
from google.cloud import storage
from google.cloud import bigquery
import pandas as pd
import os

# Initialize FastAPI
app = FastAPI()

# Set up Google Cloud Storage and BigQuery Clients
storage_client = storage.Client.from_service_account_json('path_to_your_service_account_file.json')
bigquery_client = bigquery.Client.from_service_account_json('path_to_your_service_account_file.json')

# Google Cloud Storage Bucket Name
bucket_name = "your_bucket_name"

def save_file_to_gcs(file: UploadFile, filename: str):
    """Saves the file to Google Cloud Storage"""
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_string(file.file.read(), content_type=file.content_type)

def read_file_from_gcs(filename: str):
    """Reads the file from Google Cloud Storage"""
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    data = blob.download_as_text()
    return data

def read_csv_and_run_query(csv_data: str, table_name: str):
    """Reads the CSV data and runs the BigQuery"""
    df = pd.read_csv(pd.compat.StringIO(csv_data))
    query = build_query(df, table_name)
    result = bigquery_client.query(query)
    return result.to_dataframe()
