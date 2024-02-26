import boto3
from botocore.exceptions import ClientError
import logging
from urllib.parse import quote as urlencode
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings


class S3Service:
    def __init__(self):
        self.access_key = settings.AWS_ACCESS_KEY
        self.secret_key = settings.AWS_SECRET_KEY
        self.region_name = settings.AWS_REGION
        self.bucket = settings.S3_BUCKET
        self.s3_url = settings.S3_BASE_URL

    @property
    def client(self):
        client = boto3.client('s3', region_name=self.region_name, aws_access_key_id=self.access_key,
                            aws_secret_access_key=self.secret_key)
        return client

    def upload_file(self, *, file: UploadFile) -> str:
        try:
            self.client.upload_fileobj(file.file, self.bucket, file.filename)
            url = self._format_url(filename=file.filename)
            return url
        except ClientError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"File could not be uploaded: {e}")

    def _format_url(self, filename):
        encoded_filename = urlencode(filename.encode('utf-8'))
        formatted_url = self.s3_url + encoded_filename
        return formatted_url


s3_service = S3Service()
