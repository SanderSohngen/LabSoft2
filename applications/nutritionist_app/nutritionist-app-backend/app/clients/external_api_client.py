import os

from httpx import AsyncClient
from dotenv import load_dotenv

load_dotenv()

EXTERNAL_BASE_URL = os.getenv("EXTERNAL_BASE_URL")


class ExternalAPIClient:
    def __init__(self):
        self.client = AsyncClient(base_url=EXTERNAL_BASE_URL)

    async def __aenter__(self):
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
