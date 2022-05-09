import asyncio
from typing import Dict
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema
from decouple import config
from pathlib import Path

conf = ConnectionConfig(
    MAIL_USERNAME=config("MAIL_USERNAME"),
    MAIL_PASSWORD=config("MAIL_PASSWORD"),
    MAIL_FROM="hello@reminderse.com",
    MAIL_PORT=587,
    MAIL_SERVER=config("MAIL_SERVER"),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

fm = FastMail(conf)


async def send(to: str, body: dict):
    message = MessageSchema(
        subject="Welcome to Reminderse! Please confirm your email address",
        recipients=[to],
        template_body=body
    )
    await fm.send_message(message, template_name="confirmation_email.html")
    return
