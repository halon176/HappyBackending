from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, Field, EmailStr

from src.schemas import CustomBase


class UserResponse(CustomBase):
    id: PositiveInt
    username: str = Field(..., min_length=5, max_length=50, examples=["ciccio"])
    email: EmailStr
    is_admin: bool
    created_at: datetime


class UserCreate(CustomBase):
    username: str = Field(..., min_length=5, max_length=50, examples=["ciccio"])
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=30, examples=["ciccio123"])
    is_admin: bool = Field(False)


class UserUpdate(CustomBase):
    username: Optional[str] = Field(
        None, min_length=5, max_length=50, examples=["ciccio"]
    )
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(
        None, min_length=8, max_length=30, examples=["ciccio123"]
    )
    is_admin: Optional[bool] = Field(None)


class UserLogin(CustomBase):
    username: Optional[str] = Field(
        None, min_length=5, max_length=50, examples=["ciccio"]
    )
    password: Optional[str] = Field(
        None, min_length=8, max_length=30, examples=["ciccio123"]
    )
