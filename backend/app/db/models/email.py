from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EmailRecord(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sender: Mapped[str] = mapped_column(String(255), index=True)
    recipient: Mapped[str] = mapped_column(String(255), index=True)
    subject: Mapped[str] = mapped_column(String(500), default="")
    body: Mapped[str] = mapped_column(Text, default="")
    score: Mapped[int] = mapped_column(Integer, index=True)
    verdict: Mapped[str] = mapped_column(String(50), index=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    rule_hits = relationship(
        "RuleHitRecord",
        back_populates="email",
        cascade="all, delete-orphan",
    )
