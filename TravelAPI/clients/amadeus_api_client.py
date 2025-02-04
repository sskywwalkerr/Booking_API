# Client для внешнего API
import logging
from datetime import date

import httpx
import os
from dotenv import load_dotenv
load_dotenv()


class AmadeusApiClient:
    BASE_URL = "https://test.api.amadeus.com/v1"

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

    async def search_hotels(self, city: str):
        if not self.access_token:
            await self.authenticate()

        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "cityCode": city,
            # "checkInDate": check_in,
            # "checkOutDate": check_out,
            # "adults": adults,
        }
        url = f"{self.BASE_URL}/reference-data/locations/hotels/by-city"
        logging.debug(f"Request URL: {url}")
        logging.debug(f"Requesting hotels with params: {params}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            logging.debug(f"Response status: {response.status_code}")
            logging.debug(f"Response content: {response.text}")
            response.raise_for_status()
            return response.json()
