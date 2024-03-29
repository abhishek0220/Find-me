import os
from google.cloud import storage

if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.getcwd(), 'googleStorage.json')

BUCKET_NAME = 'bvhacks'


class _CloudStorage:
    def __init__(self) -> None:
        self.storage_client = storage.Client()
        self.bucket: storage.Bucket = self.storage_client.bucket(BUCKET_NAME)

    def upload(self, source_file_name: str, destination_blob_name: str) -> str:
        blob: storage.Blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        return blob.public_url

    def delete(self, blob_name: str) -> None:
        blob = self.bucket.blob(blob_name)
        blob.delete()


cloud_storage = _CloudStorage()
