import uvicorn
from fastapi import FastAPI, APIRouter, BackgroundTasks
from api.auth.routes import auth_router
from api.db.data import init_db

# from api.config import MailBody
# from api.mail import send_mail

app = FastAPI(title="API Project")

main_api_router = APIRouter()
main_api_router.include_router(auth_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()

# @app.post("/send-email")
# def schedule_mail(req: MailBody, tasks: BackgroundTasks):
#     data = req.dict()
#     tasks.add_task(send_mail, data)
#     return {"status": 200, "message": "email has been scheduled"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
