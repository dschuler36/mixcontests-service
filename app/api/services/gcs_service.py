from app.api.config import settings
from fastapi import Response
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

    def download_file(self, stem_location):
        bucket = self.get_bucket()
        blob = bucket.blob(stem_location)

        try:
            file_contents = blob.download_as_bytes()
            headers = {
                "Content-Disposition": f"attachment; filename={blob.name}"
            }
            return Response(file_contents, headers=headers)
        except Exception as e:
            return {"error": str(e)}
