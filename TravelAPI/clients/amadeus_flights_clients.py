import logging
from typing import Dict, Any, Optional
import httpx
import os
from dotenv import load_dotenv
from fastapi import HTTPException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()


class AmadeusApiClient:
    BASE_URL_V1 = "https://test.api.amadeus.com/v1"
    BASE_URL_V2 = "https://test.api.amadeus.com/v2"
    BASE_URL_V3 = "https://test.api.amadeus.com/v3"
    HOTEL_BOOKINGS_URL = f"{BASE_URL_V2}/booking/hotel-orders"
    TOKEN_URL = f"{BASE_URL_V1}/security/oauth2/token"
    FLIGHTS_SEARCH_URL = f"{BASE_URL_V2}/shopping/flight-offers"

    def __init__(self):
        self.client_id = os.getenv('TRAVEL_API_KEY')
        self.client_secret = os.getenv('TRAVEL_API_SECRET')
        self.access_token: Optional[str] = None

    async def authenticate(self) -> None:
        """Аутентификация в API Amadeus"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                data={"grant_type": "client_credentials"},
                auth=(self.client_id, self.client_secret),
            )
            response.raise_for_status()
            self.access_token = response.json().get("access_token")
            if not self.access_token:
                raise ValueError("Failed to obtain access token")

    async def make_request(
            self,
            method: str,
            url: str,
            headers: dict,
            params: Optional[dict] = None,
            json: Optional[dict] = None
    ) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json
            )
            response.raise_for_status()
            return response.json()

    async def get_flights_destination(self, params: dict):
        if not self.access_token:
            await self.authenticate()

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.FLIGHTS_SEARCH_URL}",
                params=params,
                headers=headers,
                timeout=30.0
            )

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)

            return response.json()



