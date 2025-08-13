import httpx
import json

from AvaiasalesAPI.clients.flights_service import generate_signature
from api.config import Config


async def initiate_search(request_data: dict) -> dict:
    """Инициализация поиска в Aviasales"""
    params = {
        "marker": Config.aviasales_marker,
        "host": Config.host,
        "user_ip": request_data["user_ip"],
        "locale": request_data["locale"],
        "trip_class": request_data["trip_class"],
        "passengers": request_data["passengers"],
        "segments": request_data["segments"]
    }

    params["signature"] = generate_signature(params, Config.aviasales_secret)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://api.travelpayouts.com/v1/flight_search",
            json=params,
            timeout=30
        )
    response.raise_for_status()
    return response.json()


async def get_search_results(search_id: str) -> dict:
    """Получение результатов поиска"""
    url = f"https://api.travelpayouts.com/v1/flight_search_results?uuid={search_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={"Accept-Encoding": "gzip,deflate,sdch"},
            timeout=60
        )
    response.raise_for_status()
    return response.json()


async def get_booking_link(search_id: str, url_code: int, user_ip: str) -> dict:
    """Получение ссылки для бронирования"""
    url = (
        f"https://api.travelpayouts.com/v1/flight_searches/{search_id}"
        f"/clicks/{url_code}.json?marker={Config.aviasales_marker}&user_ip={user_ip}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    response.raise_for_status()
    return response.json()