import os
import pandas as pd
import argparse
import json
import logging
from google.cloud import bigquery
from gcputils.gcpclient import GCSClient
from gcputils.GoogleCloudLogging import GoogleCloudLogging
from gcputils.BigQueryClient import BigQueryClient

def initialize_gcs_client(project_id, credentials_path=None):
    return GCSClient(project_id, credentials_path=credentials_path)

def initialize_google_cloud_logging_client(project_id, credentials_path=None):
    return GoogleCloudLogging(project_id, credentials_path=credentials_path)

def initialize_bq_client(project_id, credentials_path=None):
    return BigQueryClient(project_id, credentials_path=credentials_path)

def list_gcs_buckets(client):
    try:
        buckets = client.list_buckets()
        print("Buckets:", buckets)
        logging.info(f"Buckets: {buckets}")
    except Exception as e:
        logging.error(f"Error listing buckets: {e}")

def create_gcs_bucket(client, bucket_name):
    try:
        bucket = client.create_bucket(bucket_name=bucket_name)
        logging.info(bucket)
        print(bucket)
    except Exception as e:
        logging.error(f"Error creating bucket: {e}")

def normalize_main(result):
    df_main = pd.json_normalize(result)
    return df_main

def normalize_item(result):
    item_data = result['item']
    df_item = pd.json_normalize(item_data)
    df_item['id'] = result['id']  # Add 'id' for joining
    return df_item

def normalize_resources(result):
    resources_data = result['resources']
    df_resources = pd.json_normalize(resources_data)
    df_resources['id'] = result['id']  # Add 'id' for joining
    return df_resources

def normalize_call_numbers(result):
    item_data = result['item']
    call_numbers = item_data.get('call_number', [])
    df_call_number = pd.DataFrame(call_numbers, columns=['call_number'])
    df_call_number['id'] = result['id']  # Add 'id' for joining
    return df_call_number

def normalize_contributors(result):
    item_data = result['item']
    contributors = item_data.get('contributors', [])
    df_contributors = pd.DataFrame(contributors, columns=['contributors'])
    df_contributors['id'] = result['id']  # Add 'id' for joining
    return df_contributors

def normalize_subjects(result):
    item_data = result['item']
    subjects = item_data.get('subjects', [])
    df_subjects = pd.DataFrame(subjects, columns=['subjects'])
    df_subjects['id'] = result['id']  # Add 'id' for joining
    return df_subjects

def normalize_notes(result):
    item_data = result['item']
    notes = item_data.get('notes', [])
    df_notes = pd.DataFrame(notes, columns=['notes'])
    df_notes['id'] = result['id']  # Add 'id' for joining
    return df_notes

def create_tables_and_schemas(bq_client, bucket_name, patterns_file, gcs_client, dataset_id):
    # Define the BigQuery table schema
    main_table_id = "results_staging"
    item_table_id = "items_staging"
    resources_table_id = "resources_staging"
    call_number_table_id = "call_numbers_staging"
    contributors_table_id = "contributors_staging"
    subjects_table_id = "subjects_staging"
    notes_table_id = "notes_staging"

    # Assuming the first blob provides a sample structure
    sample_blob = gcs_client.pop_blob(bucket_name, patterns_file)
    blob_data = gcs_client.download_blob_to_memory(bucket_name, sample_blob.name)
    json_data = json.loads(blob_data)
    result = json_data["results"][0]  # Use the first result as a sample

    df_main = normalize_main(result)
    df_item = normalize_item(result)
    df_resources = normalize_resources(result)
    df_call_number = normalize_call_numbers(result)
    df_contributors = normalize_contributors(result)
    df_subjects = normalize_subjects(result)
    df_notes = normalize_notes(result)

    main_schema = [bigquery.SchemaField(name, bigquery.enums.SqlTypeNames.STRING) for name in df_main.columns]
    item_schema = [bigquery.SchemaField(name, bigquery.enums.SqlTypeNames.STRING) for name in df_item.columns]
    resources_schema = [bigquery.SchemaField(name, bigquery.enums.SqlTypeNames.STRING) for name in df_resources.columns]
    call_number_schema = [bigquery.SchemaField(name, bigquery.enums.SqlTypeNames.STRING) for name in df_call_number.columns]
    contributors_schema = [bigquery.SchemaField(name, bigquery.enums.SqlTypeNames.STRING) for name in df_contributors.columns]
    subjects_schema = [bigquery.SchemaField(name, bigquery.enums.SqlTypeNames.STRING) for name in df_subjects.columns]
    notes_schema = [bigquery.SchemaField(name, bigquery.enums.SqlTypeNames.STRING) for name in df_notes.columns]

    # Create BigQuery tables
    # bq_client.create_table(dataset_id, main_table_id, main_schema)
    bq_client.create_table(dataset_id, item_table_id, item_schema)
    bq_client.create_table(dataset_id, resources_table_id, resources_schema)
    bq_client.create_table(dataset_id, call_number_table_id, call_number_schema)
    bq_client.create_table(dataset_id, contributors_table_id, contributors_schema)
    bq_client.create_table(dataset_id, subjects_table_id, subjects_schema)
    bq_client.create_table(dataset_id, notes_table_id, notes_schema)

def process_blob(gcs_client, bq_client, bucket_name, processed_bucket_name, patterns_file, dataset_id):
    main_table_id = "results_staging"
    item_table_id = "items_staging"
    resources_table_id = "resources_staging"
    call_number_table_id = "call_numbers_staging"
    contributors_table_id = "contributors_staging"
    subjects_table_id = "subjects_staging"
    notes_table_id = "notes_staging"

    # Grab a blob from the heap
    first_blob = gcs_client.pop_blob(bucket_name, patterns_file)
    if not first_blob:
        return False

    print(f"Processing blob: {first_blob.name}")

    # Download to memory
    blob_data = gcs_client.download_blob_to_memory(bucket_name, first_blob.name)
    json_data = json.loads(blob_data)

    results = json_data["results"]

    # Initialize lists to hold DataFrames
    df_main_list = []
    df_item_list = []
    df_resources_list = []
    df_call_number_list = []
    df_contributors_list = []
    df_subjects_list = []
    df_notes_list = []

    for result in results:
        df_main_list.append(normalize_main(result))
        df_item_list.append(normalize_item(result))
        df_resources_list.append(normalize_resources(result))
        df_call_number_list.append(normalize_call_numbers(result))
        df_contributors_list.append(normalize_contributors(result))
        df_subjects_list.append(normalize_subjects(result))
        df_notes_list.append(normalize_notes(result))

    # Concatenate all DataFrames
    df_main = pd.concat(df_main_list, ignore_index=True)
    df_item = pd.concat(df_item_list, ignore_index=True)
    df_resources = pd.concat(df_resources_list, ignore_index=True)
    df_call_number = pd.concat(df_call_number_list, ignore_index=True)
    df_contributors = pd.concat(df_contributors_list, ignore_index=True)
    df_subjects = pd.concat(df_subjects_list, ignore_index=True)
    df_notes = pd.concat(df_notes_list, ignore_index=True)

    # Load DataFrames into BigQuery tables
    # bq_client.load_dataframe_to_table(dataset_id, main_table_id, df_main)
    bq_client.load_dataframe_to_table(dataset_id, item_table_id, df_item)
    bq_client.load_dataframe_to_table(dataset_id, resources_table_id, df_resources)
    bq_client.load_dataframe_to_table(dataset_id, call_number_table_id, df_call_number)
    bq_client.load_dataframe_to_table(dataset_id, contributors_table_id, df_contributors)
    bq_client.load_dataframe_to_table(dataset_id, subjects_table_id, df_subjects)
    bq_client.load_dataframe_to_table(dataset_id, notes_table_id, df_notes)

    # Move the blob to the processed_results bucket
    gcs_client.copy_blob(bucket_name, first_blob.name, processed_bucket_name, first_blob.name)
    gcs_client.delete_blob(bucket_name, first_blob.name)
    print(f"Blob {first_blob.name} moved to {processed_bucket_name} and deleted from {bucket_name}")

    return True

def main():
    parser = argparse.ArgumentParser(description='Run the script locally or in the cloud.')
    parser.add_argument('--local', action='store_true', help='Run the script locally with credentials path')
    args = parser.parse_args()

    dataset_id = "supreme_court"
    patterns_file = os.getenv('PATTERNS_FILE', 'exclude.txt')
    project_id = os.getenv('GCP_PROJECT_ID', 'smart-axis-421517')
    bucket_name = os.getenv('BUCKET_NAME', 'loc-scraper')
    processed_bucket_name = "processed_results"

    credentials_path = None
    if args.local:
        credentials_path = os.getenv('GCP_CREDENTIALS_PATH', 'secret.json')

    # Initialize logging
    logging_client = initialize_google_cloud_logging_client(project_id, credentials_path)
    logging_client.setup_logging()

    # List Buckets for testing
    gcs_client = initialize_gcs_client(project_id, credentials_path)
    list_gcs_buckets(gcs_client)

    # Create the processed_results bucket if not exists
    # gcs_client.create_bucket(processed_bucket_name)

    bq_client = initialize_bq_client(project_id, credentials_path)

    # Create the dataset if not exists
    bq_client.create_dataset(dataset_id)

    # Create tables and schemas
    create_tables_and_schemas(bq_client, bucket_name, patterns_file, gcs_client, dataset_id)
    # def create_tables_and_schemas(bq_client, bucket_name, patterns_file, gcs_client, dataset_id):

    # Process blobs in a loop
    while process_blob(gcs_client, bq_client, bucket_name, processed_bucket_name, patterns_file, dataset_id):
        print("Processed a blob, checking for more...")
        

if __name__ == "__main__":
    main()
