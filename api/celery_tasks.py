import smtplib

from celery import Celery
from api.celery import celery
from pydantic import EmailStr

from api.config import Config
from api.mail import mail, create_message
from asgiref.sync import async_to_sync

from email_templates import create_booking_confirmation_template

c_app = Celery()

c_app.config_from_object("api.config")


@c_app.task()
def send_email(recipients: list[str], subject: str, body: str):
    print(f"Sending email to: {recipients}, subject: {subject}")
    try:
        message = create_message(recipients=recipients, subject=subject, body=body)
        async_to_sync(mail.send_message)(message)
        print("Email sent")
    except Exception as e:
        print(f"Error sending email: {e}")


@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr
):
    email_to_user = email_to  # Используйте email_to, переданный в задачу
    email_content = create_booking_confirmation_template(
        booking=booking, email_to=email_to_user
    )
    try:
        with smtplib.SMTP_SSL(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.send_message(email_content)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

