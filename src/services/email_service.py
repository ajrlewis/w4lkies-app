import asyncio
import datetime
import traceback as tb
from typing import Optional

from flask import render_template, request
from flask_mail import Message
import html2text
from loguru import logger

from app import mail
from models import User


def send_user_sign_in_notification(user: User):
    html = render_template(
        "emails/user_sign_in_notification.html",
        user=user,
        now=datetime.datetime.now().strftime("%H:%M %Y-%m-%d"),
        user_agent=request.user_agent.string,
        ip_address=request.remote_addr,
    )
    send(
        sender=mail.username,
        recipient=user.email,
        subject="⚠️🔒 Sign-in Notification ⚠️🔒",
        html=html,
    )
    logger.debug("Sent sign-in notification to user")


def send(
    sender: str,
    recipient: str,
    subject: str,
    html: str,
    bcc: list = [],
    attachments: Optional[list] = None,
):
    try:
        recipients = [recipient]
        logger.debug(f"{recipients = }")
        body = html2text.html2text(html)
        # logger.debug(f"{body = }")
        message = Message(
            subject,
            sender=sender,
            bcc=bcc,
            recipients=recipients,
            html=html,
            body=body,
        )
        # logger.debug(f"{message = }")
        if attachments:
            for attachment in attachments:
                logger.debug(f"{attachment = }")
                message.attach(**attachment)
        mail.send(message)
    except Exception as e:
        logger.error(f"{tb.format_exc() = }")
        logger.error(f"{e = }")
        return


async def send_async(
    sender: str,
    recipient: str,
    subject: str,
    html: str,
    attachments: Optional[list] = None,
):
    try:
        recipients = [recipient]
        logger.debug(f"{recipients = }")
        bcc = [mail.username]
        logger.debug(f"{bcc = }")
        body = html2text.html2text(html)
        logger.debug(f"{body = }")
        message = Message(
            subject,
            sender=sender,
            bcc=bcc,
            recipients=recipients,
            html=html,
            body=body,
        )
        logger.debug(f"{message = }")

        # Check if mail.send is an asynchronous method
        # If not, you may need to use run_in_executor or create a thread pool
        if hasattr(mail, "send_async"):
            await mail.send_async(message)
        else:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, mail.send, message)

        if attachments:
            for attachment in attachments:
                logger.debug(f"{attachment = }")
                message.attach(**attachment)

    except Exception as e:
        logger.error(f"{tb.format_exc() = }")
        logger.error(f"{e = }")
