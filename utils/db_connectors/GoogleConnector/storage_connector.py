from datetime import datetime

from google.oauth2 import service_account
from google.cloud import storage

class StorageConnector:

    def __init__(self, key_path,scopes):
        credentials = service_account.Credentials.from_service_account_file(key_path,scopes=scopes)

        self.storage_client = storage.Client(credentials=credentials)

    def upload_to_storage(self,project_id,bucket, blob_name, upload_data):
        bucket_name = bucket
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        if blob.exists():
            blob.delete()
        blob.upload_from_string(upload_data)

    @staticmethod
    def add_creation_log_to_df(df):
        now = datetime.now()
        df['created_at'] = now
        df['updated_at'] = now
        return df
