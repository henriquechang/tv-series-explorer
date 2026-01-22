from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.database import get_session
from app.infrastructure.persistence.repositories.comment import SQLAlchemyCommentRepository
from app.application.use_cases.manage_comments import (
    AddCommentUseCase, GetCommentsUseCase, DeleteCommentUseCase
)


router = APIRouter(tags=["comments"])


class AddCommentRequest(BaseModel):
    text: str


class CommentResponse(BaseModel):
    id: int
    show_id: int
    episode_id: Optional[int]
    text: str
    created_at: datetime


@router.get("/shows/{show_id}/comments", response_model=list[CommentResponse])
async def get_show_comments(
    show_id: int,
    session: AsyncSession = Depends(get_session)
):
    repository = SQLAlchemyCommentRepository(session)
    use_case = GetCommentsUseCase(repository)
    comments = await use_case.for_show(show_id)
    return [CommentResponse(**c.__dict__) for c in comments]


@router.post("/shows/{show_id}/comments", response_model=CommentResponse)
async def add_show_comment(
    show_id: int,
    request: AddCommentRequest,
    session: AsyncSession = Depends(get_session)
):
    repository = SQLAlchemyCommentRepository(session)
    use_case = AddCommentUseCase(repository)
    try:
        comment = await use_case.execute(show_id=show_id, text=request.text)
        return CommentResponse(**comment.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/episodes/{episode_id}/comments", response_model=list[CommentResponse])
async def get_episode_comments(
    episode_id: int,
    session: AsyncSession = Depends(get_session)
):
    repository = SQLAlchemyCommentRepository(session)
    use_case = GetCommentsUseCase(repository)
    comments = await use_case.for_episode(episode_id)
    return [CommentResponse(**c.__dict__) for c in comments]


@router.post("/shows/{show_id}/episodes/{episode_id}/comments", response_model=CommentResponse)
async def add_episode_comment(
    show_id: int,
    episode_id: int,
    request: AddCommentRequest,
    session: AsyncSession = Depends(get_session)
):
    repository = SQLAlchemyCommentRepository(session)
    use_case = AddCommentUseCase(repository)
    try:
        comment = await use_case.execute(
            show_id=show_id, 
            text=request.text, 
            episode_id=episode_id
        )
        return CommentResponse(**comment.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_session)
):
    repository = SQLAlchemyCommentRepository(session)
    use_case = DeleteCommentUseCase(repository)
    deleted = await use_case.execute(comment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"deleted": True}