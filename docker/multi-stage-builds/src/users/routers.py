from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.databese import get_async_session
from src.events.schemas import EventResponse
from src.security import sign_jwt, JWTBearer
from src.users.models import User
from src.users.schemas import UserCreate, UserResponse, UserUpdate, UserLogin

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me")
async def me(session: AsyncSession = Depends(get_async_session), user_id: int = Depends(JWTBearer())):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.get("/", response_model=Optional[List[UserResponse]])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    query = select(User)
    query_result = await session.scalars(query)
    result = query_result.unique().all()
    return result


@router.post("/login")
async def login(
        payload: UserLogin,
        session: AsyncSession = Depends(get_async_session)
):
    query = select(User).where(User.username == payload.username)
    query_result = await session.scalars(query)
    result = query_result.first()
    error_exception = HTTPException(status_code=401, detail="Wrong user or password")
    if not result:
        raise error_exception
    if not result.check_password(payload.password):
        raise error_exception
    return sign_jwt(result.id)


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = User(
        username=user.username,
        email=user.email,
        password_setter=user.password,
        is_admin=False
    )

    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already in use")
    return new_user

@router.post("/image_upload")
async def image_upload(image: UploadFile, user_id: int = Depends(JWTBearer())):
    if image.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Deve essere un jpeg/jpg")
    with open(f"static/images/{user_id}.jpg", "wb") as buffer:
        buffer.write(image.file.read())
    return {"message": "immagine scritta"}

@router.get("/image_download")
async def image_download(user_id: int):
    return FileResponse(f"static/images/{user_id}.jpg")




@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.patch("/", response_model=UserResponse)
async def update_user(payload: UserUpdate,
                      session: AsyncSession = Depends(get_async_session),
                      user_id: int = Depends(JWTBearer())):
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


@router.delete("/", status_code=204)
async def delete_user(session: AsyncSession = Depends(get_async_session),
                      user_id: int = Depends(JWTBearer())):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(result)
    await session.commit()
    return None


@router.get("/get/events", response_model=Optional[List[EventResponse]])
async def get_user_events(session: AsyncSession = Depends(get_async_session),
                          user_id=Depends(JWTBearer())):
    query = select(User).where(User.id == user_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result.events
