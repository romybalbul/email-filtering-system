import asyncio
from email import policy
from email.parser import BytesParser

from aiosmtpd.controller import Controller

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.schemas.email import AttachmentInput, EmailInput
from app.services.queue_service import enqueue_email
from app.services.list_service import seed_default_lists
from app.services.network_list_service import (
    is_blocked_ip,
    is_local_recipient_domain,
    is_relay_allowed_ip,
)
import app.db.models  # noqa: F401


def get_peer_ip(session) -> str:
    peer = getattr(session, "peer", None)
    if not peer:
        return ""
    return peer[0]


class EmailFilterHandler:
    async def handle_MAIL(self, server, session, envelope, address, mail_options):
        peer_ip = get_peer_ip(session)

        db = SessionLocal()
        try:
            if is_blocked_ip(db, peer_ip):
                print(f"SMTP rejected blocked IP at MAIL FROM: {peer_ip}")
                return "550 5.7.1 Sender IP is blocked"

            envelope.mail_from = address
            return "250 OK"
        finally:
            db.close()

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        peer_ip = get_peer_ip(session)

        db = SessionLocal()
        try:
            recipient_is_local = is_local_recipient_domain(db, address)
            relay_allowed = is_relay_allowed_ip(db, peer_ip)

            if not recipient_is_local and not relay_allowed:
                print(
                    f"SMTP relay denied: ip={peer_ip}, recipient={address}"
                )
                return "554 5.7.1 Relay access denied"

            envelope.rcpt_tos.append(address)
            return "250 OK"
        finally:
            db.close()

    async def handle_DATA(self, server, session, envelope):
        peer_ip = get_peer_ip(session)

        db = SessionLocal()
        try:
            if is_blocked_ip(db, peer_ip):
                print(f"SMTP rejected blocked IP at DATA: {peer_ip}")
                return "550 5.7.1 Sender IP is blocked"
        finally:
            db.close()

        raw_message = envelope.content
        parsed = BytesParser(policy=policy.default).parsebytes(raw_message)

        sender = envelope.mail_from or ""
        recipients = envelope.rcpt_tos or []
        recipient = recipients[0] if recipients else ""
        subject = parsed.get("subject", "")

        body = ""
        attachments = []

        if parsed.is_multipart():
            for part in parsed.walk():
                content_disposition = part.get_content_disposition()
                filename = part.get_filename()

                if content_disposition == "attachment" and filename:
                    payload = part.get_payload(decode=True) or b""
                    attachments.append(
                        AttachmentInput(
                            filename=filename,
                            content_type=part.get_content_type(),
                            size=len(payload),
                        )
                    )
                elif part.get_content_type() == "text/plain":
                    try:
                        body += part.get_content()
                    except Exception:
                        pass
        else:
            try:
                body = parsed.get_content()
            except Exception:
                body = ""

        email_input = EmailInput(
            sender=sender,
            recipient=recipient,
            subject=subject,
            body=body,
            attachments=attachments,
        )

        db = SessionLocal()
        try:
            record = enqueue_email(db, email_input)

            print(
                f"SMTP email queued: id={record.id}, "
                f"peer_ip={peer_ip}, sender={sender}, recipient={recipient}"
            )
        finally:
            db.close()

        return "250 Message accepted for filtering"


async def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_default_lists(db)
    finally:
        db.close()

    controller = Controller(
        EmailFilterHandler(),
        hostname="0.0.0.0",
        port=2525,
    )

    controller.start()
    print("SMTP server running on 0.0.0.0:2525")

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        controller.stop()


if __name__ == "__main__":
    asyncio.run(main())
