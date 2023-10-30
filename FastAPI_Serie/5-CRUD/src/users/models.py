from datetime import datetime
from typing import List

from sqlalchemy import Integer, Text, Boolean, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.databese import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, unique=True)
    email: Mapped[str] = mapped_column(Text, unique=True)
    password: Mapped[str] = mapped_column(Text)
    is_admin: Mapped[bool] = mapped_column(Boolean, deferred=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    events: Mapped[List["Event"]] = relationship(back_populates="user", cascade="all, delete-orphan", lazy="joined")
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user", cascade="all, delete-orphan")
