from fastapi import APIRouter, Depends, HTTPException, Body

from TravelAPI.clients.amadeus_flights_clients import AmadeusApiClient
from TravelAPI.models.schemas_flights import FlightSearchParams, AirlineDestinationParams, AirlineLocationParams, \
    FlightOffersPriceParams, FlightOfferPricingRequest

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


@router_flights.post("shopping/flight-offers/pricing")
async def price_flight_offers(
        request: FlightOfferPricingRequest = Body(..., description="Предложения перелетов для подтверждения цены"),
        params: FlightOffersPriceParams = Depends(),
):
    """
    Подтверждение цены для предложений перелетов

    Требуемые заголовки:
    - X-HTTP-Method-Override: GET
    - Content-Type: application/vnd.amadeus+json

    Параметры запроса:
    - include: Дополнительные ресурсы (credit-card-fees, bags, other-services, detailed-fare-rules)
    - forceClass: Принудительное использование класса бронирования (true/false)
    """
    try:
        # Извлекаем список предложений из тела запроса
        flight_offers = request.data["flightOffers"]

        result = await amadeus_client.price_flight_offers(
            flight_offers=flight_offers,
            params=params
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при подтверждении цены: {str(e)}"
        )
