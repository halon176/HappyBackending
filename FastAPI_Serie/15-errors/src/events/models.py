from datetime import datetime
from typing import List

from sqlalchemy import Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.databese import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    location: Mapped[str] = mapped_column(Text)
    capacity: Mapped[int] = mapped_column(Integer, default=10)
    content: Mapped[JSONB] = mapped_column(JSONB)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="events")
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )
    reservations: Mapped[List["Reservation"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )
