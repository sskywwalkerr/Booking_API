import logging
from typing import Dict, Any, Optional, List
import httpx
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()


class AmadeusApiClient:
    BASE_URL_V1 = "https://test.api.amadeus.com/v1"
    BASE_URL_V2 = "https://test.api.amadeus.com/v2"
    BASE_URL_V3 = "https://test.api.amadeus.com/v3"
    TOKEN_URL = f"{BASE_URL_V1}/security/oauth2/token"
    HOTELS_BY_CITY_URL = f"{BASE_URL_V1}/reference-data/locations/hotels/by-city"
    HOTEL_OFFERS_URL = f"{BASE_URL_V2}/shopping/hotel-offers"

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

    async def search_hotels(
            self,
            city_code: str,
            radius: Optional[int] = 5,
            radius_unit: Optional[str] = 'KM',
            chain_codes: Optional[List[str]] = None,
            amenities: Optional[List[str]] = None,
            ratings: Optional[List[str]] = None,
            hotel_source: Optional[str] = 'ALL',
    ) -> Dict[str, Any]:
        if not self.access_token:
            await self.authenticate()

        headers = {"Authorization": f"Bearer {self.access_token}"}

        params = {
            "cityCode": city_code,
            "radius": radius,
            "radiusUnit": radius_unit,
            "hotelSource": hotel_source,
        }
        if chain_codes:
            params["chainCodes"] = chain_codes  # как множественные параметры
        if amenities:
            params["amenities"] = ','.join(amenities)  # как строка с запятыми
        if ratings:
            params["ratings"] = ','.join(ratings)  # как строка с запятыми

            # Удаляем пустые параметры
        params = {k: v for k, v in params.items() if v is not None}

        return await self.make_request("GET", self.HOTELS_BY_CITY_URL, headers, params)

    # async def get_hotel_offers(
    #         self,
    #         hotel_ids: str,
    #         check_in_date: str,
    #         check_out_date: str,
    #         adults: int = 1,
    #         room_quantity: int = 1,
    #         currency: str = "USD",
    #         language: str = "en-US"
    # ) -> Dict[str, Any]:
    #     if not self.access_token:
    #         await self.authenticate()
    #
    #     headers = {
    #         "Authorization": f"Bearer {self.access_token}",
    #         "Content-Type": "application/json"
    #     }
    #     payload = {
    #         "hotelIds": hotel_ids,
    #         "checkInDate": check_in_date,
    #         "checkOutDate": check_out_date,
    #         "adults": adults,
    #         "roomQuantity": room_quantity,
    #         "currency": currency,
    #         "language": language
    #     }
    #
    #     return await self.make_request("POST", self.HOTEL_OFFERS_URL, headers, json=payload)
