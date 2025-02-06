# Client для внешнего API
import logging
from typing import Dict, Any, Optional
import httpx
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()


class AmadeusApiClient:
    BASE_URL_V1 = "https://test.api.amadeus.com/v1"
    BASE_URL_V2 = "https://test.api.amadeus.com/v2"
    TOKEN_URL = f"{BASE_URL_V1}/security/oauth2/token"
    HOTELS_BY_CITY_URL = f"{BASE_URL_V1}/reference-data/locations/hotels/by-city"
    HOTEL_SENTIMENTS_URL = f"{BASE_URL_V2}/e-reputation/hotel-sentiments"

    def __init__(self):
        self.client_id = os.getenv('TRAVEL_API_KEY')
        self.client_secret = os.getenv('TRAVEL_API_SECRET')
        self.access_token: Optional[str] = None

    async def authenticate(self) -> None:
        """Аутентификация в API Amadeus и получение токена доступа."""
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

    async def _make_request(
            self, method: str, url: str, headers: Dict[str, str], params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Выполнение HTTP-запроса с логированием."""
        logging.debug(f"Request URL: {url}")
        logging.debug(f"Requesting hotels with params: {params}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            logging.debug(f"Response status: {response.status_code}")
            logging.debug(f"Response content: {response.text}")
            response.raise_for_status()
            return response.json()

    async def search_hotels(self, city: str) -> Dict[str, Any]:
        """Поиск отелей по коду города."""
        if not self.access_token:
            await self.authenticate()

        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"cityCode": city}

        return await self._make_request("GET", self.HOTELS_BY_CITY_URL, headers, params)

    async def get_hotel_sentiments(self, hotel_ids: str) -> Dict[str, Any]:
        """Получение отзывов об отелях по их идентификаторам."""
        if not self.access_token:
            await self.authenticate()
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"hotelIds": hotel_ids}

        return await self._make_request("GET", self.HOTEL_SENTIMENTS_URL, headers, params)
