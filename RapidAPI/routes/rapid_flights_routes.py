from fastapi import FastAPI, Depends, APIRouter
from dotenv import load_dotenv
import os

from RapidAPI.clients.rapid_flights_clients import HotelsClient
from RapidAPI.models.schemas_flights import FlightDestinationResponse

load_dotenv()

rapid_booking_flights = APIRouter()


def get_hotels_client():
    api_key = os.getenv("RAPIDAPI_KEY")
    return HotelsClient(api_key)


@rapid_booking_flights.get("/destinations", response_model=FlightDestinationResponse)
async def search_flight_destinations(
    query: str,
    client: HotelsClient = Depends(get_hotels_client)
):
    results = await client.search_flight_destinations(query)
    return {"results": results}
