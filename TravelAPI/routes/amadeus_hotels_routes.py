import httpx
from fastapi import APIRouter, HTTPException
from TravelAPI.clients.amadeus_hotels_client import AmadeusApiClient
from TravelAPI.models.schemas_hotels import (
    HotelSearchRequest, HotelOfferRequest, HotelOfferRequestParams, HotelBookingRequest
)

router_search = APIRouter()
amadeus_client = AmadeusApiClient()


@router_search.post("/hotels/by-city")
async def search_hotels(request: HotelSearchRequest):
    try:
        return await amadeus_client.search_hotels(
            city_code=request.city_code,
            radius=request.radius,
            radius_unit=request.radius_unit,
            chain_codes=request.chain_codes,
            amenities=[a.value for a in request.amenities] if request.amenities else None,
            ratings=[r.value for r in request.ratings] if request.ratings else None,
            hotel_source=request.hotel_source,
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_search.post("/hotel/offers/")
async def hotel_offers(request: HotelOfferRequest):
    try:
        return await amadeus_client.get_hotel_offers(
            hotel_ids=request.hotel_ids,
            check_in_date=request.check_in_date,
            check_out_date=request.check_out_date,
            adults=request.adults,
            room_quantity=request.room_quantity,
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_search.post("/hotel/offers/params/")
async def hotel_offers_params(request: HotelOfferRequestParams):
    try:
        return await amadeus_client.get_hotel_offer_params(
            hotel_ids=request.hotel_ids,
            adults=request.adults,
            check_in_date=request.check_in_date,
            check_out_date=request.check_out_date,
            country_of_residence=request.country_of_residence,
            room_quantity=request.room_quantity,
            price_range=request.price_range,
            currency=request.currency,
            payment_policy=request.payment_policy,
            board_type=request.board_type,
            include_closed=request.include_closed,
            best_rate_only=request.best_rate_only,
            lang=request.lang,
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_search.post("/hotel/bookings/")
async def book_hotel(request: HotelBookingRequest):
    try:
        payload = request.dict(by_alias=True, exclude_unset=True)
        return await amadeus_client.book_hotel(payload=payload)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Amadeus API Error: {e.response.text}"
        )
