from sqlalchemy import DateTime, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ListEntryRecord(Base):
    __tablename__ = "list_entries"
    __table_args__ = (
        UniqueConstraint("list_type", "value", name="uq_list_type_value"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    list_type: Mapped[str] = mapped_column(String(100), index=True)
    value: Mapped[str] = mapped_column(String(255), index=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
