import boto3
from botocore.exceptions import ClientError
import logging
import os
from dotenv import load_dotenv
from urllib.parse import quote as urlencode
from fastapi import UploadFile



class S3Service:
    @property
    def client(self):
        access_key = os.getenv('AWS_ACCESS_KEY')
        secret_key = os.getenv('AWS_SECRET_KEY')
        region_name = os.getenv('AWS_REGION')
        client =  boto3.client('s3', region_name=region_name, aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key)
        print(client)
        return client

    def upload_file(self, *, file: UploadFile) -> str:
        bucket = os.getenv('S3_BUCKET')
        region = os.getenv('AWS_REGION')
        try:
            self.client.upload_fileobj(file.file, bucket, file.filename)
            url = f"https://{bucket}.s3.{region}.amazonaws.com/{urlencode(file.filename.encode('utf8'))}"
            print(f'{file.filename} uploaded successfully')
            return url
        except ClientError as e:
            print(f'Failed to upload file: {e}')


s3_service = S3Service()