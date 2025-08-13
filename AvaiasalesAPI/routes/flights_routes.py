from fastapi import APIRouter, HTTPException

from AvaiasalesAPI.clients.flights_clients import initiate_search, get_search_results
from AvaiasalesAPI.models.schemas_flight import SearchResponse, SearchRequest

import httpx

aviasales_api = APIRouter()

@aviasales_api.post("/initiate", response_model=SearchResponse)
async def start_search(request: SearchRequest):
    try:
        result = await initiate_search(request)
        return {"search_id": result["search_id"]}
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Aviasales API error: {e.response.text}"
        )

@aviasales_api.get("/results")
async def fetch_results(search_id: str):
    try:
        return await get_search_results(search_id)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to get results: {e.response.text}"
        )