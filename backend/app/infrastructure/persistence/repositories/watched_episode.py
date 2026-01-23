from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infrastructure.persistence.models import WatchedEpisodeModel


class WatchedEpisodeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_watched_episodes(self, show_id: Optional[int] = None) -> List[WatchedEpisodeModel]:
        query = select(WatchedEpisodeModel)
        if show_id:
            query = query.filter(WatchedEpisodeModel.show_id == show_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def is_episode_watched(self, show_id: int, episode_id: int) -> bool:
        query = select(WatchedEpisodeModel).filter(
            WatchedEpisodeModel.show_id == show_id,
            WatchedEpisodeModel.episode_id == episode_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def mark_watched(self, show_id: int, episode_id: int) -> WatchedEpisodeModel:
        query = select(WatchedEpisodeModel).filter(
            WatchedEpisodeModel.show_id == show_id,
            WatchedEpisodeModel.episode_id == episode_id
        )
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()
        
        if existing:
            return existing
        
        watched = WatchedEpisodeModel(show_id=show_id, episode_id=episode_id)
        self.db.add(watched)
        await self.db.commit()
        await self.db.refresh(watched)
        return watched

    async def unmark_watched(self, show_id: int, episode_id: int) -> bool:
        query = select(WatchedEpisodeModel).filter(
            WatchedEpisodeModel.show_id == show_id,
            WatchedEpisodeModel.episode_id == episode_id
        )
        result = await self.db.execute(query)
        watched = result.scalar_one_or_none()
        
        if watched:
            await self.db.delete(watched)
            await self.db.commit()
            return True
        return False