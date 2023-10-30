from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.databese import get_async_session
from src.events.models import Event
from src.events.schemas import EventResponse, EventCreate, EventUpdate

router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.get("/", response_model=List[EventResponse])
async def get_events(session: AsyncSession = Depends(get_async_session)):
    query = select(Event)
    query_result = await session.scalars(query)
    result = query_result.all()
    return result


@router.post("/", response_model=EventResponse)
async def create_event(payload: EventCreate, session: AsyncSession = Depends(get_async_session)):
    new_event = Event(
        name=payload.name,
        date=payload.date,
        location=payload.location,
        capacity=payload.capacity,
        user_id=payload.user_id,
        content=payload.content
    )
    session.add(new_event)
    await session.commit()
    return new_event


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Event).where(Event.id == event_id)
    query_result = await session.scalars(query)
    result = query_result.first()

    if not result:
        return HTTPException(status_code=404, detail="Event not found")

    return result


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(event_id: int, payload: EventUpdate, session: AsyncSession = Depends(get_async_session)):
    query = select(Event).where(Event.id == event_id)
    query_result = await session.scalars(query)
    result = query_result.first()

    if not result:
        return HTTPException(status_code=404, detail="Event not found")

    for key, value in payload.model_dump().items():
        if value:
            setattr(result, key, value)

    await session.commit()
    return result


@router.delete("/{event_id}", status_code=204)
async def delete_event(event_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Event).where(Event.id == event_id)
    query_result = await session.scalars(query)
    result = query_result.first()

    if not result:
        return HTTPException(status_code=404, detail="Event not found")

    await session.delete(result)
    await session.commit()
    return None
