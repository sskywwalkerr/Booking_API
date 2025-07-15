import logging
from typing import Dict, Any, Optional, List
import httpx
import os
from dotenv import load_dotenv
from fastapi import HTTPException

from AmadeusAPI.models.schemas_flights import FlightOffersPriceParams

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
    FLIGHTS_SEARCH_DESTINATIONS = f"{BASE_URL_V1}/shopping/flight-destinations"
    FLIGHTS_SEARCH_AIRLINE = f"{BASE_URL_V1}/airline/destinations"
    FLIGHTS_SEARCH_LOCATIONS = f"{BASE_URL_V1}/reference-data/locations"
    FLIGHTS_OFFER = f"{BASE_URL_V1}/shopping/flight-offers/pricing"

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

    async def get_airline_destination(self, params: dict) -> Dict[str, Any]:
        if not self.access_token:
            await self.authenticate()

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.FLIGHTS_SEARCH_AIRLINE}",
                params=params,
                headers=headers,
                timeout=30.0)

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)

            return response.json()

    async def get_airline_location(self, params: dict) -> Dict[str, Any]:
        if not self.access_token:
            await self.authenticate()

        headers = {"Authorization": f"Bearer {self.access_token}"}

        encoded_params = []
        for key, value in params.items():
            if '[' in key and ']' in key:
                # кодирую только значение, ключ оставляю как есть
                encoded_params.append((key, str(value)))
            else:
                encoded_params.append((key, str(value)))

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.FLIGHTS_SEARCH_LOCATIONS}",
                params=encoded_params,  # преобразованные параметры
                headers=headers,
                timeout=30.0
            )

            if response.status_code != 200:
                print(f"Amadeus API error: {response.status_code}, {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)

            return response.json()

    async def price_flight_offers(
            self,
            flight_offers: List[Dict[str, Any]],
            params: FlightOffersPriceParams
    ) -> Dict[str, Any]:
        if not self.access_token:
            await self.authenticate()

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-HTTP-Method-Override": "GET",
            "Content-Type": "application/vnd.amadeus+json"
        }

        request_body = {
            "data": {
                "type": "flight-offers-pricing",
                "flightOffers": flight_offers
            }
        }

        query_params = params.dict(exclude_none=True)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.FLIGHTS_OFFER}",
                json=request_body,
                headers=headers,
                params=query_params,
                timeout=30.0
            )

            if response.status_code != 200:
                error_detail = f"Amadeus API error: {response.status_code} - {response.text}"
                raise ValueError(error_detail)

            return response.json()

