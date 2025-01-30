# Client для внешнего API
import logging

import httpx
import os
from dotenv import load_dotenv
load_dotenv()


class AmadeusApiClient:
    BASE_URL = "https://test.api.amadeus.com/v2" # Тестовый юрл для api

    def __init__(self):
        self.client_id = os.getenv('TRAVEL_API_KEY')
        self.client_secret = os.getenv('TRAVEL_API_SECRET')
        self.access_token = None

    async def authenticate(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://test.api.amadeus.com/v1/security/oauth2/token",
                data={"grant_type": "client_credentials"},
                auth=(self.client_id, self.client_secret),
            )
            response.raise_for_status()
            self.access_token = response.json().get("access_token")
            if not self.access_token:
                raise ValueError("Failed to obtain access token")

    async def search_hotels(self, city: str, check_in: str, check_out: str, adults: int):
        if not self.access_token:
            await self.authenticate()

        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "cityCode": city,
            "checkInDate": check_in,
            "checkOutDate": check_out,
            "adults": adults,
        }
        logging.debug(f"Requesting hotels with params: {params}")

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/shopping/hotel-offers", headers=headers, params=params)
            response.raise_for_status()
            return response.json()
