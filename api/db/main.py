# import uvicorn
from fastapi import FastAPI, APIRouter
from api.auth.routes import auth_router
from api.bookings.routes import router
# from api.config import Config
from api.db.data import init_db
from api.hotel.routes import hotel_router
from api.reviews.routes import review_router
from api.rooms.routes import room_routes

# from redis import asyncio as aioredis
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend

app = FastAPI(title="API Project")

main_api_router = APIRouter()
main_api_router.include_router(auth_router, prefix="/user", tags=["пользователь"])
app.include_router(main_api_router)

main_api_router1 = APIRouter()
main_api_router1.include_router(hotel_router, prefix="/hotel", tags=["отель"])
app.include_router(main_api_router1)

main_api_router2 = APIRouter()
main_api_router2.include_router(review_router, prefix="/review", tags=["отзывы"])
app.include_router(main_api_router2)


main_api_router3 = APIRouter()
main_api_router3.include_router(room_routes, prefix="/room", tags=["комната"])
app.include_router(main_api_router3)

main_api_router4 = APIRouter()
main_api_router4.include_router(router, prefix="/bookings", tags=["бронирование"])
app.include_router(main_api_router4)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()

# @app.on_event('startup')
# def startup():
#     redis = aioredis.from_url(
#         f'redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}',
#         encoding='utf8',
#         decode_responses=True
#     )
#     FastAPICache.init(RedisBackend(redis), prefix="cache")

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
