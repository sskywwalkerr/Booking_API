import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from utilities import settings
from api.handlers import user_router
from api.login_handler import login_router
from utilities.parsers.handlers_parser import router as api_router

from redis_om import get_redis_connection
#######################
# BLOCK WITH API ROUTES #
#######################

app = FastAPI(title="API Project")
app.include_router(api_router, prefix="/api", tags=["parsers"])
# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(main_api_router)


if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)