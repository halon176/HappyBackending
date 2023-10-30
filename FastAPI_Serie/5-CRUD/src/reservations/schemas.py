from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, Field

from src.schemas import CustomBase


class ReservationResponse(CustomBase):
    id: PositiveInt = Field(..., examples=[1])
    num_guests: PositiveInt = Field(..., examples=[10])
    user_id: PositiveInt = Field(..., examples=[1])
    event_id: PositiveInt = Field(..., examples=[1])
    created_at: datetime


class ReservationCreate(CustomBase):
    num_guests: PositiveInt = Field(..., examples=[10])
    user_id: PositiveInt = Field(..., examples=[1])
    event_id: PositiveInt = Field(..., examples=[1])


class ReservationUpdate(CustomBase):
    user_id: Optional[PositiveInt] = Field(None, examples=[1])
    event_id: Optional[PositiveInt] = Field(None, examples=[1])
    num_guests: Optional[PositiveInt] = Field(None, examples=[10])
