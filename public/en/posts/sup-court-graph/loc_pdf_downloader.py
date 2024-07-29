import os
import argparse
import json
import logging
import requests
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
        logging.info(f"Buckets: {buckets}")
    except Exception as e:
        logging.error(f"Error listing buckets: {e}")

def create_gcs_bucket(client, bucket_name):
    try:
        bucket = client.create_bucket(bucket_name=bucket_name)
        logging.info(bucket)
    except Exception as e:
        logging.error(f"Error creating bucket: {e}")

def download_json_from_gcs(gcs_client, bucket_name, blob_name):
    try:
        blob_data = gcs_client.download_blob_to_memory(bucket_name, blob_name)
        json_data = json.loads(blob_data)
        logging.info(f"Downloaded JSON from {bucket_name}/{blob_name}")
        return json_data
    except Exception as e:
        logging.error(f"Error downloading JSON from {bucket_name}/{blob_name}: {e}")
        return None

def extract_pdf_urls(json_data):
    pdf_urls = []
    try:
        results = json_data["results"]
        for result in results:
            resources = result.get("resources", [])
            for resource in resources:
                if resource.get("pdf"):
                    pdf_urls.append(resource.get("pdf"))
        logging.info(f"Extracted {len(pdf_urls)} PDF URLs")
    except Exception as e:
        logging.error(f"Error extracting PDF URLs: {e}")
    return pdf_urls

def download_pdf(url, local_path):
    if os.path.exists(local_path):
        logging.info(f"File {local_path} already exists. Skipping download.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            f.write(response.content)
        logging.info(f"Downloaded PDF from {url} to {local_path}")
    except Exception as e:
        logging.error(f"Error downloading PDF from {url}: {e}")

def upload_pdf_to_gcs(gcs_client, bucket_name, local_path, destination_blob_name):
    # if gcs_client.blob_exists(bucket_name, destination_blob_name):
    #     logging.info(f"Blob {destination_blob_name} already exists in bucket {bucket_name}. Skipping upload.")
    #     return

    try:
        gcs_client.upload_blob(bucket_name, local_path, destination_blob_name)
        logging.info(f"Uploaded PDF to {bucket_name}/{destination_blob_name}")
    except Exception as e:
        logging.error(f"Error uploading PDF to {bucket_name}/{destination_blob_name}: {e}")

def process_blob(gcs_client, source_bucket, destination_bucket, blob_name):
    json_data = download_json_from_gcs(gcs_client, source_bucket, blob_name)
    if not json_data:
        return False

    pdf_urls = extract_pdf_urls(json_data)
    for url in pdf_urls:
        pdf_filename = os.path.basename(url)
        local_path = f"/tmp/{pdf_filename}"
        if os.path.exists(local_path):
            print(f"{local_path} exists")
            continue
        download_pdf(url, local_path)
        upload_pdf_to_gcs(gcs_client, destination_bucket, local_path, pdf_filename)
        # if os.path.exists(local_path):
        #     os.remove(local_path)  # Clean up the local file

    return True

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description='Run the script locally or in the cloud.')
    parser.add_argument('--local', action='store_true', help='Run the script locally with credentials path')
    args = parser.parse_args()

    source_bucket = os.getenv('SOURCE_BUCKET_NAME', 'processed_results')
    destination_bucket = os.getenv('DESTINATION_BUCKET_NAME', 'loc_pdfs')
    project_id = os.getenv('GCP_PROJECT_ID', 'smart-axis-421517')

    credentials_path = None
    if args.local:
        credentials_path = os.getenv('GCP_CREDENTIALS_PATH', 'secret.json')

    gcs_client = initialize_gcs_client(project_id, credentials_path)
    list_gcs_buckets(gcs_client)

    blobs = gcs_client.list_blobs(source_bucket)
    for blob in blobs:
        process_blob(gcs_client, source_bucket, destination_bucket, blob)

if __name__ == "__main__":
    main()
