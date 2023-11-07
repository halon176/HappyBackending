from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.databese import get_async_session
from src.events.schemas import EventResponse
from src.users.models import User
from src.users.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=Optional[List[UserResponse]])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    query = select(User)
    query_result = await session.scalars(query)
    result = query_result.unique().all()
    return result


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        is_admin=False
    )

    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already in use")
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, payload: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in payload.model_dump().items():
        if value is not None:
            setattr(result, field, value)

    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already in use")
    return result


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(result)
    await session.commit()
    return None


@router.get("/{user_id}/events", response_model=Optional[List[EventResponse]])
async def get_user_events(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result.events
