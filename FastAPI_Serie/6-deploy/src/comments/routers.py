from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.comments.models import Comment
from src.comments.schemas import CommentCreate, CommentResponse, CommentUpdate
from src.databese import get_async_session

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


@router.get("/", response_model=Optional[List[CommentResponse]])
async def get_comments(session: AsyncSession = Depends(get_async_session)):
    query = select(Comment)
    query_result = await session.scalars(query)
    result = query_result.all()
    return result


@router.post("/", response_model=CommentResponse, status_code=201)
async def create_comment(payload: CommentCreate, session: AsyncSession = Depends(get_async_session)):
    new_comment = Comment(
        content=payload.content.model_dump(),
        user_id=payload.user_id,
        event_id=payload.event_id
    )

    session.add(new_comment)
    await session.commit()
    return new_comment


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Comment).where(Comment.id == comment_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return result


@router.patch("/{comment_id}", response_model=CommentResponse)
async def update_comment(comment_id: int, comment: CommentUpdate, session: AsyncSession = Depends(get_async_session)):
    query = select(Comment).where(Comment.id == comment_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    for field, value in comment.model_dump().items():
        if value is not None:
            setattr(result, field, value.model_dump() if hasattr(value, "model_dump") else value)

    await session.commit()
    return result


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(comment_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Comment).where(Comment.id == comment_id)
    query_result = await session.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    await session.delete(result)
    await session.commit()
    return None
