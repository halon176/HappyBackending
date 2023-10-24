from typing import List

from sqlalchemy import Integer, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.databese import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(Text)
    is_admin: Mapped[bool] = mapped_column(Boolean, deferred=False)

    events: Mapped[List["Event"]] = relationship(back_populates="user")
