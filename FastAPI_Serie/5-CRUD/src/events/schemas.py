from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, Field

from src.schemas import CustomBase


class EventResponse(CustomBase):
    id: PositiveInt
    name: str = Field(..., min_length=3, max_length=50, examples=["Sagra della patata"])
    date: datetime
    location: str = Field(..., min_length=3, max_length=50, examples=["Piazza del paese"])
    capacity: PositiveInt = Field(..., examples=[100])
    user_id: PositiveInt = Field(..., examples=[1])
    content: dict
    created_at: datetime


class EventCreate(CustomBase):
    name: str = Field(..., min_length=3, max_length=50, examples=["Sagra della patata"])
    date: datetime
    location: str = Field(..., min_length=3, max_length=50, examples=["Piazza del paese"])
    capacity: PositiveInt = Field(..., examples=[100])
    user_id: PositiveInt = Field(..., examples=[1])
    content: dict


class EventUpdate(CustomBase):
    name: Optional[str] = Field(None, min_length=3, max_length=50, examples=["Sagra della patata"])
    date: Optional[datetime] = Field(None)
    location: Optional[str] = Field(None, min_length=3, max_length=50, examples=["Piazza del paese"])
    capacity: Optional[PositiveInt] = Field(None, examples=[100])
    user_id: Optional[PositiveInt] = Field(None, examples=[1])
    content: Optional[dict] = None
