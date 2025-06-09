from fastapi import APIRouter, Depends

from TravelAPI.clients.amadeus_flights_clients import AmadeusApiClient
from TravelAPI.models.schemas_flights import FlightSearchParams, AirlineDestinationParams, AirlineLocationParams

router_flights = APIRouter()
amadeus_client = AmadeusApiClient()


@router_flights.get("/search")
async def search_flights(params: FlightSearchParams = Depends()):
    filtered_params = params.model_dump(exclude_none=True)

    result = await amadeus_client.get_flights_destination(filtered_params)
    return result


@router_flights.get("/airline/destinations")
async def search_airline_destinations(params: AirlineDestinationParams = Depends()):
    result = await amadeus_client.get_airline_destination(params.model_dump(exclude_none=True))
    return result


@router_flights.get("/reference-data/locations")
async def search_airline_location(params: AirlineLocationParams = Depends()):
    amadeus_params = params.dict(by_alias=True, exclude_none=True)

    # переименование поля для совместимости
    if "page_limit" in amadeus_params:
        amadeus_params["page[limit]"] = amadeus_params.pop("page_limit")
    if "page_offset" in amadeus_params:
        amadeus_params["page[offset]"] = amadeus_params.pop("page_offset")

    result = await amadeus_client.get_airline_location(amadeus_params)
    return result
