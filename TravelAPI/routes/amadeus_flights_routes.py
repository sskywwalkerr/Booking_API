from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from TravelAPI.clients.amadeus_flights_clients import AmadeusApiClient

router_flights = APIRouter()
amadeus_client = AmadeusApiClient()


@router_flights.get("/search")
async def search_flights(
        originLocationCode: str = Query(..., description="IATA код города отправления (например, SYD)"),
        destinationLocationCode: str = Query(..., description=""),
        departureDate: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}", description="Дата вылета в формате YYYY-MM-DD"),
        returnDate: Optional[str] = Query(None, regex=r"\d{4}-\d{2}-\d{2}", description="Дата возврата в формате YYYY-MM-DD"),
        adults: int = Query(1, ge=1, le=9, description="Количество взрослых пассажиров (от 1 до 9)"),
        children: Optional[int] = Query(0, ge=0, le=9, description="Количество детей (до 12 лет, от 0 до 9)"),
        infants: Optional[int] = Query(0, ge=0, description="Количество младенцев (до 2 лет, не больше количества взрослых)"),
        travelClass: Optional[str] = Query(
            None,
            pattern=r"(ECONOMY|PREMIUM_ECONOMY|BUSINESS|FIRST)",
            description="Класс путешествия"
        ),
        includedAirlineCodes: Optional[str] = Query(None, description="Список разрешённых авиакомпаний через запятую (IATA коды)"),
        excludedAirlineCodes: Optional[str] = Query(None, description="Список исключённых авиакомпаний через запятую (IATA коды)"),
        nonStop: bool = Query(False, description="Только прямые рейсы. False or True"),
        currencyCode: Optional[str] = Query(None, regex=r"[A-Z]{3}", description="Валюта по ISO 4217 (например, EUR)"),
        maxPrice: Optional[int] = Query(None, ge=0, description="Максимальная цена за путешественника"),
        max: int = Query(250, ge=1, le=250, description="Максимум предложений для возврата (от 1 до 250)")
):
    if infants > adults:
        raise HTTPException(status_code=400, detail="Количество младенцев не может превышать количество взрослых")

    params = {
        "originLocationCode": originLocationCode,
        "destinationLocationCode": destinationLocationCode,
        "departureDate": departureDate,
        "returnDate": returnDate,
        "adults": adults,
        "children": children,
        "infants": infants,
        "travelClass": travelClass,
        "includedAirlineCodes": includedAirlineCodes,
        "excludedAirlineCodes": excludedAirlineCodes,
        "nonStop": "true" if nonStop else "false",
        "currencyCode": currencyCode,
        "maxPrice": maxPrice,
        "max": max
    }

    params = {k: v for k, v in params.items() if v is not None}

    result = await amadeus_client.get_flights_destination(params)
    return result

