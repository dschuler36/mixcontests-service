from app.api.config import settings
from google.cloud import storage


class GCSService:
    def __init__(self):
        self.gcs_bucket_name = settings.GCS_BUCKET_NAME
        self.storage_client = storage.Client()

    def get_bucket(self):
        return self.storage_client.bucket(self.gcs_bucket_name)

    def create_folder(self, folder_name):
        bucket = self.get_bucket()
        blob_prefix = bucket.blob(folder_name)
        blob_prefix.upload_from_string(b'', content_type="application/x-directory")
