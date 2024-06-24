from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.databese import get_async_session
from src.events.models import Event
from src.reservations.models import Reservation
from src.reservations.schemas import (
    ReservationCreate,
    ReservationResponse,
    ReservationUpdate,
)
from src.security import JWTBearer
from .errors import NotFoundReservationError

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
)

expNotFound = HTTPException(status_code=404, detail="Reservation not found")

docNotFound = {"model": NotFoundReservationError, "description": "Not found"}


@router.get("/", response_model=Optional[List[ReservationResponse]])
async def get_reservations(
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(JWTBearer()),
):
    query = select(Reservation).where(Reservation.user_id == user_id)
    query_result = await session.scalars(query)
    result = query_result.all()
    return result


@router.post(
    "/",
    response_model=ReservationResponse,
    status_code=201,
    responses={404: docNotFound},
)
async def create_reservation(
    payload: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(JWTBearer()),
):
    # verifico se non supera il limite di posti disponibili
    # prima recupero i posti disponibili per l'evento
    query = select(Event.capacity).where(Event.id == payload.event_id)
    query_result = await session.scalars(query)
    max_capacity = query_result.first()
    if not max_capacity:
        raise expNotFound

    # poi recupero il numero di posti già prenotati
    query = select(Reservation.num_guests).where(
        Reservation.event_id == payload.event_id
    )
    query_result = await session.scalars(query)
    num_guests_array = query_result.all()
    num_guest = sum(num_guests_array)

    # se il numero di posti disponibili è minore del numero di posti prenotati + il numero di posti richiesti
    if num_guest + payload.num_guests > max_capacity:
        raise expNotFound

    new_reservation = Reservation(
        num_guests=payload.num_guests, user_id=user_id, event_id=payload.event_id
    )

    session.add(new_reservation)
    await session.commit()
    return new_reservation


@router.get(
    "/{reservation_id}",
    response_model=ReservationResponse,
    responses={404: docNotFound},
)
async def get_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(JWTBearer()),
):
    query = select(Reservation).where(
        Reservation.id == reservation_id, Reservation.user_id == user_id
    )
    query_result = await session.scalars(query)
    result = query_result.first()

    if result is None:
        raise expNotFound

    return result


@router.patch(
    "/{reservation_id}",
    response_model=ReservationResponse,
    responses={404: docNotFound},
)
async def update_reservation(
    reservation_id: int,
    payload: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(JWTBearer()),
):
    query = select(Reservation).where(
        Reservation.id == reservation_id, Reservation.user_id == user_id
    )
    query_result = await session.scalars(query)
    result = query_result.first()

    if result is None:
        raise expNotFound

    for field, value in payload.model_dump().items():
        if value is not None:
            setattr(result, field, value)

    await session.commit()
    return result


@router.delete("/{reservation_id}", status_code=204, responses={404: docNotFound})
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(JWTBearer()),
):
    query = select(Reservation).where(
        Reservation.id == reservation_id, Reservation.user_id == user_id
    )
    query_result = await session.scalars(query)
    result = query_result.first()

    if not result:
        return expNotFound

    await session.delete(result)
    await session.commit()
    return None
