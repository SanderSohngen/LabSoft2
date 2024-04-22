import os

from dotenv import load_dotenv
from boto3 import client
from typing import AsyncGenerator

from .clients.external_api_client import ExternalAPIClient

load_dotenv()


async def get_client() -> AsyncGenerator[ExternalAPIClient, None]:
    async with ExternalAPIClient() as external_client:
        yield external_client


def get_s3_client() -> client:
    return client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION_NAME")
    )
