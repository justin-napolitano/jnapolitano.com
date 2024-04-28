from google.cloud import storage
import os

class GCSClient:
    def __init__(self, project_id, credentials_path=None):
        """
        Initializes the Google Cloud Storage client.

        Args:
            project_id (str): The Google Cloud project ID.
            credentials_path (str, optional): Path to the JSON file containing service account credentials.
                                              If not provided, it will use the default credentials from the environment.
        """
        self.project_id = project_id
        self.credentials_path = credentials_path
        self.client = self._create_client()

    def _create_client(self):
        """
        Creates and returns the Google Cloud Storage client.

        Returns:
            google.cloud.storage.Client: The initialized Google Cloud Storage client.
        """
        if self.credentials_path:
            client = storage.Client.from_service_account_json(self.credentials_path)
        else:
            client = storage.Client(project=self.project_id)
        return client

    def list_buckets(self):
        """
        Lists all buckets in the Google Cloud Storage project.

        Returns:
            list: A list of bucket names.
        
        Source: 
            https://cloud.google.com/storage/docs/listing-buckets
        """
        buckets = [bucket.name for bucket in self.client.list_buckets()]
        return buckets
    
    def create_bucket(self, bucket_name):
        """
        Creates a new bucket in the Google Cloud Storage project if it does not already exist.

        Args:
            bucket_name (str): The name of the bucket to create.

        Returns:
            str: The name of the created bucket.

        Source: 
            https://cloud.google.com/storage/docs/creating-buckets
        """
        bucket = self.client.bucket(bucket_name)
        if not bucket.exists():
            bucket.create()
            return f"Bucket '{bucket_name}' created successfully."
        else:
            return f"Bucket '{bucket_name}' already exists."
        
    def upload_to_bucket_from_memory(self, bucket, source_string, destination_blob_name):
        """
        Uploads an object to a blob in a Google Cloud Storage bucket.

        Args:
            bucket (str or google.cloud.storage.Bucket): The name of the bucket or an already instantiated bucket object.
            source_object (str, bytes, file-like object): The object to be uploaded.
            destination_blob_name (str): The name to give to the uploaded file in the bucket.

        Returns:
            str: The URL of the uploaded object.

        Source: https://cloud.google.com/storage/docs/uploading-objects-from-memory
        """
        if isinstance(bucket, str):
            bucket = self.client.bucket(bucket)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(source_string)
        return f"Object uploaded to {destination_blob_name} in bucket {bucket.name}"

# Example usage:

def test():

    project_id = os.environ.get("GCPPROJECTID")
    # credentials_path = "path/to/your/credentials.json"  # Optional if using default credentials
    gcs = GCSClient(project_id, credentials_path=None)

    # List buckets
    buckets = gcs.list_buckets()
    print("Buckets:", buckets)



if __name__ == "__main__":
    test()

