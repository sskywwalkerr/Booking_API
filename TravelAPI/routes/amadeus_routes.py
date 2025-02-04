import httpx
from fastapi import APIRouter, HTTPException
from TravelAPI.clients.amadeus_api_client import AmadeusApiClient
from TravelAPI.models.schemas import SearchRequest, BookingRequest
import logging
router_search = APIRouter()
amadeus_client = AmadeusApiClient()


@router_search.post("/search-hotels/")
async def search_hotels(search_request: SearchRequest):
    try:
        hotels = await amadeus_client.search_hotels(
            search_request.city,
            # search_request.check_in,
            # search_request.check_out,
            # search_request.adults,
        )
        return hotels
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router_search.post("/book/")
# async def book_hotel(booking_request: BookingRequest):
#     # Логика для создания бронирования
#     pass
logging.basicConfig(level=logging.DEBUG)
