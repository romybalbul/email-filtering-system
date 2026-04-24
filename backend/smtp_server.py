import asyncio
from email import policy
from email.parser import BytesParser

from aiosmtpd.controller import Controller

from app.schemas.email import EmailInput, AttachmentInput
from app.services.filtering_engine import FilteringEngine
from app.services.email_service import save_filtered_email
from app.db.session import SessionLocal
from app.db.base import Base
from app.db.session import engine
import app.db.models  # noqa: F401


class EmailFilterHandler:
    async def handle_DATA(self, server, session, envelope):
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
            engine_filter = FilteringEngine()
            result = engine_filter.evaluate(email_input, db)
            record = save_filtered_email(db, email_input, result)

            print(
                f"SMTP email saved: id={record.id}, "
                f"sender={sender}, verdict={result.verdict}, score={result.score}"
            )
        finally:
            db.close()

        return "250 Message accepted for filtering"


async def main():
    Base.metadata.create_all(bind=engine)

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
