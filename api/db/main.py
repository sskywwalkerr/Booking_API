# import uvicorn
from fastapi import FastAPI, APIRouter
from sqladmin import Admin

from api.admin.auth import authentication_backend

from api.admin.main import UserAdmin, BookingAdmin, RoomAdmin, HotelAdmin
# from api.admin.views import UsersAdmin, HotelsAdmin, RoomsAdmin, BookingsAdmin

from api.auth.routes import auth_router
from api.bookings.routes import router

from api.db.data import init_db, async_engine
from api.hotel.routes import hotel_router
from api.reviews.routes import review_router
from api.rooms.routes import room_routes
from prometheus.routes import router_prom


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

main_api_router5 = APIRouter()
main_api_router5.include_router(router_prom, prefix="/Prometheus", tags=["Prometheus"])
app.include_router(main_api_router5)

# подключение админки
admin = Admin(app, async_engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(HotelAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)

# admin.add_view(UsersAdmin)
# admin.add_view(HotelsAdmin)
# admin.add_view(RoomsAdmin)
# admin.add_view(BookingsAdmin)


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
