import httpx
from fastapi import APIRouter, HTTPException
from TravelAPI.clients.amadeus_api_client import AmadeusApiClient
from TravelAPI.models.schemas import SearchRequest, GetSentiments, GetPrices
import logging
router_search = APIRouter()
amadeus_client = AmadeusApiClient()


@router_search.post("/search-hotels/")
async def search_hotels(search_request: SearchRequest):
    try:
        hotels = await amadeus_client.search_hotels(
            search_request.city,
        )
        return hotels
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_search.post("/get_hotel_sentiments/")
async def get_hotel_sentiments(get_sentiment: GetSentiments):
    try:
        sentiments = await amadeus_client.get_hotel_sentiments(
            get_sentiment.hotel_ids
        )
        return sentiments
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_search.post("/get_hotel_prices/")
async def get_hotel_prices(get_prices: GetPrices):
    try:
        # Проверяем, что у нас есть доступ к amadeus_client
        if not hasattr(amadeus_client, 'get_hotel_prices'):
            raise HTTPException(status_code=500, detail="Amadeus client not initialized")

        # Получаем цены на отели
        prices = await amadeus_client.get_hotel_prices(
            get_prices.hotel_ids,
            get_prices.adults,
            get_prices.checkInDate,
            get_prices.roomQuantity,
        )
        return prices
    except httpx.HTTPStatusError as e:
        # Обработка ошибок HTTP
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except ValueError as e:
        # Обработка ошибок значения
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Обработка всех других исключений
        raise HTTPException(status_code=500, detail=str(e))

logging.basicConfig(level=logging.DEBUG)
