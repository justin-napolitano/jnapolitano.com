from gcputils.gcpclient import GCSClient




if __name__ =="__main__":
     project_id = 'smart-axis-421517'
     gcs = GCSClient(project_id, credentials_path=None)
     bucket_name = "loc-scraper"
     blob_name = 'last_page.txt'
     blob_data = "1"

     blob = gcs.put_blob_from_string(bucket_name, blob_data, blob_name, overwrite = False)

