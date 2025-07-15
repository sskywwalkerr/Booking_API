import httpx
from fastapi import HTTPException


class HotelsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "booking-com15.p.rapidapi.com"
        }
        self.base_url = "https://booking-com15.p.rapidapi.com/api/v1 "

    async def search_flight_destinations(self, query: str):
        url = f"{self.base_url}/flights/searchDestination"
        params = {"query": query}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=e.response.text)