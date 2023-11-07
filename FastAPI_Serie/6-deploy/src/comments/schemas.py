from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, Field

from src.schemas import CustomBase


class ContentSchema(CustomBase):
    title: str = Field(..., examples=["Titolo"])
    text: str = Field(..., examples=["Contenuto del commento"])
    raiting: int = Field(..., ge=1, le=10, examples=[5])


class CommentResponse(CustomBase):
    id: PositiveInt
    content: ContentSchema
    user_id: PositiveInt = Field(..., examples=[1])
    event_id: PositiveInt = Field(..., examples=[1])
    created_at: datetime


class CommentCreate(CustomBase):
    content: ContentSchema
    user_id: PositiveInt = Field(..., examples=[1])
    event_id: PositiveInt = Field(..., examples=[1])


class CommentUpdate(CustomBase):
    content: Optional[ContentSchema] = None
    user_id: Optional[int] = Field(None, examples=[1])
    event_id: Optional[int] = Field(None, examples=[1])
