import httpx
from fastapi import APIRouter, HTTPException
from TravelAPI.clients.amadeus_api_client import AmadeusApiClient
from TravelAPI.models.schemas import (
    HotelSearchRequest
)

router_search = APIRouter()
amadeus_client = AmadeusApiClient()


@router_search.post("/search-hotels/")
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

