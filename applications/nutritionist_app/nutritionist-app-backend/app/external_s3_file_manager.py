import boto3

from typing import List
from fastapi import UploadFile, File

from .models import User
from .external_schemas import Document


def upload_doc_to_s3(
    patient_id: int,
    user: User,
    s3_client: boto3.client,
    bucket_name: str = "vitalink",
    file: UploadFile = File(...),
) -> Document:
    key = f"{1}/nutritionist/{3}/{file.filename}"
    s3_client.put_object(
        Body=file.file.read(),
        Bucket=bucket_name,
        Key=key
    )
    return Document(key=key)


def download_doc_from_s3(
    patient_id: int,
    user_id: int,
    filename: str,
    s3_client: boto3.client,
    bucket_name: str = "vitalink",
    profession: str = "nutritionist"
):
    key = f"{patient_id}/{profession}/{user_id}/{filename}"
    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=key
    )
    for chunk in response['Body'].iter_chunks(chunk_size=1024*1024):
        yield chunk


def list_docs_from_s3(
    s3_client: boto3.client,
    bucket_name: str = "vitalink",
) -> List[Document]:
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    documents = []
    if 'Contents' in response:
        for item in response['Contents']:
            document = Document(key=item['Key'])
            documents.append(document)
    return documents
