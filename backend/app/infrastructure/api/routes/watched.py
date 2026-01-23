from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.infrastructure.persistence.database import get_session
from app.infrastructure.persistence.repositories.watched_episode import WatchedEpisodeRepository


router = APIRouter(prefix="/api", tags=["watched"])


class WatchedStatus(BaseModel):
    episode_id: int


@router.get("/shows/{show_id}/watched", response_model=List[WatchedStatus])
async def get_watched_episodes(show_id: int, db: AsyncSession = Depends(get_session)):
    repo = WatchedEpisodeRepository(db)
    watched_episodes = await repo.get_watched_episodes(show_id)
    return [
        WatchedStatus(episode_id=ep.episode_id)
        for ep in watched_episodes
    ]


@router.get("/shows/{show_id}/episodes/{episode_id}/watched")
async def check_watched(show_id: int, episode_id: int, db: AsyncSession = Depends(get_session)):
    repo = WatchedEpisodeRepository(db)
    watched = await repo.is_episode_watched(show_id, episode_id)
    return {"watched": watched}


@router.put("/shows/{show_id}/episodes/{episode_id}/watched")
async def mark_watched(show_id: int, episode_id: int, db: AsyncSession = Depends(get_session)):
    repo = WatchedEpisodeRepository(db)
    await repo.mark_watched(show_id, episode_id)
    return {"success": True}


@router.delete("/shows/{show_id}/episodes/{episode_id}/watched")
async def unmark_watched(show_id: int, episode_id: int, db: AsyncSession = Depends(get_session)):
    repo = WatchedEpisodeRepository(db)
    deleted = await repo.unmark_watched(show_id, episode_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Episode not found")
    return {"success": True}