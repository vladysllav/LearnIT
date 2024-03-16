from fastapi import APIRouter, UploadFile
from app.services.s3 import s3_service

router = APIRouter()


@router.post('/upload_file/')
def upload_file(file: UploadFile):
    file_url = s3_service.upload_file(file=file)
    return {'url': file_url}
