from fastapi import APIRouter, Depends

from TravelAPI.clients.amadeus_flights_clients import AmadeusApiClient
from TravelAPI.models.schemas_flights import FlightSearchParams, AirlineDestinationParams

router_flights = APIRouter()
amadeus_client = AmadeusApiClient()


@router_flights.get("/search")
async def search_flights(params: FlightSearchParams = Depends()):
    filtered_params = params.model_dump(exclude_none=True)

    result = await amadeus_client.get_flights_destination(filtered_params)
    return result


# @router_flights.get("/destinations")
# async def get_flight_destinations(params: FlightDestinationParams = Depends()):
#     result = await amadeus_client.get_flights_destination(params.model_dump(exclude_none=True))
#     return result

@router_flights.get("/airline/destinations")
async def search_airline_destinations(params: AirlineDestinationParams = Depends()):
    result = await amadeus_client.get_airline_destination(params.model_dump(exclude_none=True))
    return result
