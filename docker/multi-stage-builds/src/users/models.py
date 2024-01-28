from datetime import datetime
from typing import List

from passlib.context import CryptContext
from sqlalchemy import Integer, Text, Boolean, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.databese import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

    @property
    def password_setter(self):
        raise AttributeError("Password can't be read")

    @password_setter.setter
    def password_setter(self, password: str) -> None:
        self.password = pwd_context.hash(password)

    def check_password(self, plane_password: str) -> bool:
        return pwd_context.verify(plane_password, self.password)

    def __json__(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at}
