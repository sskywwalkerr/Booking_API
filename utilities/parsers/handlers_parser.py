import requests
from logging import getLogger
from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel


from utilities.parsers.product_parser import get_data, get_result
# from utilities.redis_tools.tools import RedisTools

logger = getLogger(__name__)

app = FastAPI()
router = APIRouter()


class URLRequest(BaseModel):
    url: str


@router.post("/parse/data")
async def parse_data(request: URLRequest):
    try:
        get_data(request.url)
        return {"message": "Страница успешно загружена и сохранена.", "url": request.url}
    except requests.HTTPError as http_err:
        raise HTTPException(status_code=http_err.response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


# @router.post("/parse/result")
# async def parse_result(request: URLRequest, current_user: User = Depends(get_current_user)):
#     if not current_user.is_authenticated:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#
#     try:
#         result = get_result(request.url)  # Assuming get_result handles file I/O
#         return {"message": "Parsing successful.", "result": result, "url": request.url}
#     except requests.HTTPError as http_err:
#         raise HTTPException(status_code=http_err.response.status_code, detail=str(http_err))
#     except Exception as err:
#         raise HTTPException(status_code=500, detail=str(err))

# @router.post("/parse/result")
# async def parse_result(request: URLRequest):
#     try:
#         get_result(request.url)
#         return {"message": "Страница успешно загружена и сохранена.", "url": request.url}
#     except requests.HTTPError as http_err:
#         raise HTTPException(status_code=http_err.response.status_code, detail=str(http_err))
#     except Exception as err:
#         raise HTTPException(status_code=500, detail=str(err))


@router.post("/parse/result")
async def parse_result(request: URLRequest):
    # if name not in [s.encode('utf-8') for s in RedisTools.get_keys()]:
    #     return {
    #         'error': 'the name does not exist'
    #     }
    # return {
    #     'name': name,
    #     'item_basePrice': RedisTools.get_pair(name)
    # }
    try:
        get_result(request.url)
        return {"message": "Страница успешно загружена и сохранена.", "url": request.url}
    except requests.HTTPError as http_err:
        raise HTTPException(status_code=http_err.response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)