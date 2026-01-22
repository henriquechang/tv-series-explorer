from datetime import datetime
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.comment import Comment
from app.domain.interfaces.comment_repository import CommentRepository
from app.infrastructure.persistence.models import CommentModel


class SQLAlchemyCommentRepository(CommentRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, show_id: int, text: str, episode_id: Optional[int] = None) -> Comment:
        model = CommentModel(
            show_id=show_id,
            episode_id=episode_id,
            text=text,
            created_at=datetime.utcnow()
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        
        return Comment(
            id=model.id,
            show_id=model.show_id,
            episode_id=model.episode_id,
            text=model.text,
            created_at=model.created_at
        )

    async def get_for_show(self, show_id: int) -> list[Comment]:
        result = await self._session.execute(
            select(CommentModel)
            .where(CommentModel.show_id == show_id)
            .where(CommentModel.episode_id.is_(None))
            .order_by(CommentModel.created_at.desc())
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def get_for_episode(self, episode_id: int) -> list[Comment]:
        result = await self._session.execute(
            select(CommentModel)
            .where(CommentModel.episode_id == episode_id)
            .order_by(CommentModel.created_at.desc())
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def delete(self, comment_id: int) -> bool:
        result = await self._session.execute(
            delete(CommentModel).where(CommentModel.id == comment_id)
        )
        await self._session.commit()
        return result.rowcount > 0

    def _to_entity(self, model: CommentModel) -> Comment:
        return Comment(
            id=model.id,
            show_id=model.show_id,
            episode_id=model.episode_id,
            text=model.text,
            created_at=model.created_at
        )