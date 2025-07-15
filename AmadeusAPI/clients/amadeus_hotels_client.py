import logging
from typing import Dict, Any, Optional, List
import httpx
import os
from dotenv import load_dotenv
from pydantic import Field

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()


class AmadeusApiClient:
    BASE_URL_V1 = "https://test.api.amadeus.com/v1"
    BASE_URL_V2 = "https://test.api.amadeus.com/v2"
    BASE_URL_V3 = "https://test.api.amadeus.com/v3"
    HOTEL_BOOKINGS_URL = f"{BASE_URL_V2}/booking/hotel-orders"
    TOKEN_URL = f"{BASE_URL_V1}/security/oauth2/token"
    HOTELS_BY_CITY_URL = f"{BASE_URL_V1}/reference-data/locations/hotels/by-city"
    HOTEL_OFFERS_URL = f"{BASE_URL_V3}/shopping/hotel-offers"

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
    """Поиск отеля"""
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
            "radiusUnit": radius_unit.upper() if radius_unit else None,
            "hotelSource": hotel_source.upper() if hotel_source else None,
        }
        if chain_codes:
            params["chainCodes"] = ",".join(chain_codes)  # лучше передать пустой список, что бы показать все отели
        if amenities:
            params["amenities"] = ",".join([a.upper() for a in amenities])
        if ratings:
            params["ratings"] = ",".join(ratings) # передать через запятую

        params = {k: v for k, v in params.items() if v is not None and v != ""}

        return await self.make_request("GET", self.HOTELS_BY_CITY_URL, headers, params)

    """Предложения отелей"""
    async def get_hotel_offers(
            self,
            hotel_ids: str,
            check_in_date: str,
            check_out_date: str,
            adults: int = 1,
            room_quantity: int = 1,

    ) -> Dict[str, Any]:
        if not self.access_token:
            await self.authenticate()

        headers = {"Authorization": f"Bearer {self.access_token}"}

        params = {
            "hotelIds": hotel_ids.strip(),
            "checkInDate": check_in_date.strip(),
            "checkOutDate": check_out_date.strip(),
            "adults": adults,
            "roomQuantity": room_quantity,
        }

        params = {k: v for k, v in params.items() if v is not None}

        return await self.make_request("GET", self.HOTEL_OFFERS_URL, headers, params)

    """Предложений отелей по параметрам"""
    async def get_hotel_offer_params(
            self,
            hotel_ids: List[str],
            adults: int = 1,
            check_in_date: str = None,
            check_out_date: str = None,
            country_of_residence: str = None,
            room_quantity: int = Field(1, ge=1, le=9),
            price_range: Optional[str] = Field(None, example="200-300"),
            currency: str = None,
            payment_policy: str = "NONE",
            board_type: str = None,
            include_closed: bool = False,
            best_rate_only: bool = True,
            lang: str = "EN",
    ) -> Dict[str, Any]:
        if not self.access_token:
            await self.authenticate()

        headers = {"Authorization": f"Bearer {self.access_token}"}

        params = {
            "hotelIds": ",".join(hotel_ids),  # Передаем как строку через запятую
            "adults": adults,
            "checkInDate": check_in_date,
            "checkOutDate": check_out_date,
            "countryOfResidence": country_of_residence,
            "roomQuantity": room_quantity,
            "priceRange": price_range,
            "currency": currency,
            "paymentPolicy": payment_policy,
            "boardType": board_type,
            "includeClosed": include_closed,
            "bestRateOnly": best_rate_only,
            "lang": lang,
        }

        params = {k: v for k, v in params.items() if v is not None}

        return await self.make_request("GET", self.HOTEL_OFFERS_URL, headers, params)

    """Бронирование отеля"""
    async def book_hotel(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.access_token:
            await self.authenticate()

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        request_payload = payload.get("data", payload)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.HOTEL_BOOKINGS_URL,
                    json={"data": request_payload},
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = f"Amadeus API Error [{e.response.status_code}]: {e.response.text}"
            raise ValueError(error_detail)
