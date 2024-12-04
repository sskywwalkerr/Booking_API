import uvicorn
from fastapi import FastAPI, APIRouter
from api.auth.routes import auth_router
from api.db.data import init_db


app = FastAPI(title="API Project")

main_api_router = APIRouter()
main_api_router.include_router(auth_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
