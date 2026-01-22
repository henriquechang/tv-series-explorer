from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.interfaces.comment_repository import CommentRepository


@dataclass
class CommentDTO:
    id: int
    show_id: int
    episode_id: Optional[int]
    text: str
    created_at: datetime


class AddCommentUseCase:

    def __init__(self, comment_repository: CommentRepository):
        self._repository = comment_repository

    async def execute(
        self, 
        show_id: int, 
        text: str, 
        episode_id: Optional[int] = None
    ) -> CommentDTO:
        if not text or not text.strip():
            raise ValueError("Comment text cannot be empty")
        
        comment = await self._repository.add(
            show_id=show_id,
            text=text.strip(),
            episode_id=episode_id
        )
        
        return CommentDTO(
            id=comment.id,
            show_id=comment.show_id,
            episode_id=comment.episode_id,
            text=comment.text,
            created_at=comment.created_at
        )


class GetCommentsUseCase:

    def __init__(self, comment_repository: CommentRepository):
        self._repository = comment_repository

    async def for_show(self, show_id: int) -> list[CommentDTO]:
        comments = await self._repository.get_for_show(show_id)
        return [self._to_dto(c) for c in comments]

    async def for_episode(self, episode_id: int) -> list[CommentDTO]:
        comments = await self._repository.get_for_episode(episode_id)
        return [self._to_dto(c) for c in comments]

    def _to_dto(self, comment) -> CommentDTO:
        return CommentDTO(
            id=comment.id,
            show_id=comment.show_id,
            episode_id=comment.episode_id,
            text=comment.text,
            created_at=comment.created_at
        )


class DeleteCommentUseCase:

    def __init__(self, comment_repository: CommentRepository):
        self._repository = comment_repository

    async def execute(self, comment_id: int) -> bool:
        return await self._repository.delete(comment_id)