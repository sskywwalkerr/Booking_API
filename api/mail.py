from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from api.config import Config
from pathlib import Path


# from ssl import create_default_context
# from email.mime.text import MIMEText
# from smtplib import SMTP


BASE_DIR = Path(__file__).resolve().parent


mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


mail = FastMail(config=mail_config)


def create_message(recipients: list[str], subject: str, body: str):

    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )

    return message

# def send_mail(data: dict | None = None):
#     msg = MailBody(**data)
#     message = MIMEText(msg.body, "html")
#     message["From"] = Config.MAIL_USERNAME
#     message["To"] = ",".join(msg.to)
#     message["Subject"] = msg.subject
#
#     ctx = create_default_context()
#
#     try:
#         with SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
#             server.ehlo()
#             server.starttls(context=ctx)
#             server.ehlo()
#             server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
#             server.send_message(message)
#             server.quit()
#         return {"status": 200, "errors": None}
#     except Exception as e:
#         return {"status": 500, "errors": e}
