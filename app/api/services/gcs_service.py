from datetime import timedelta

from app.api.config import settings
from fastapi import Response, File, HTTPException
from google.cloud import storage
import os
import tempfile
from app.api.config import settings


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

    def upload_file(self, source_file: File, destination_blob_name):
        tmp_file_path = tempfile.NamedTemporaryFile()
        tmp_file_path.name = tmp_file_path.name + '.txt'
        with open(tmp_file_path.name, 'wb') as tmp_file:
            tmp_file.write(source_file.file.read())

        full_destination_blob_name = os.path.join(destination_blob_name, source_file.filename)
        bucket = self.get_bucket()
        blob = bucket.blob(full_destination_blob_name)
        blob.upload_from_filename(tmp_file_path.name)

    async def generate_signed_url(self, file_name):
        bucket = self.get_bucket()
        blob = bucket.blob(file_name)
        signed_url = blob.generate_signed_url(version="v4", expiration=timedelta(minutes=15), method="GET")

        return {"url": signed_url}
