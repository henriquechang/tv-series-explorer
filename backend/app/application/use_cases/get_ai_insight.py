from dataclasses import dataclass
from typing import Optional

from app.domain.interfaces.ai_repository import AIRepository
from app.domain.interfaces.show_repository import ShowRepository


@dataclass
class InsightDTO:
    insight: str
    source: str 


class GetShowInsightUseCase:

    def __init__(self, ai_repository: AIRepository, show_repository: ShowRepository):
        self._ai = ai_repository
        self._shows = show_repository

    async def execute(self, show_id: int) -> Optional[InsightDTO]:
        show = await self._shows.get_by_id(show_id)
        if not show:
            return None

        try:
            insight = await self._ai.generate_show_insight(
                name=show.name,
                summary=show.summary,
                genres=show.genres or [],
                comments=[]
            )
            return InsightDTO(insight=insight, source="ai")
        except Exception:
            return InsightDTO(
                insight=f"'{show.name}' is a captivating series that delivers compelling storytelling.",
                source="fallback"
            )


class GetEpisodeInsightUseCase:

    def __init__(self, ai_repository: AIRepository, show_repository: ShowRepository):
        self._ai = ai_repository
        self._shows = show_repository

    async def execute(self, show_id: int, episode_id: int) -> Optional[InsightDTO]:
        show = await self._shows.get_by_id(show_id)
        if not show:
            return None

        episodes = await self._shows.get_episodes(show_id)
        episode = next((e for e in episodes if e.id == episode_id), None)
        if not episode:
            return None

        try:
            insight = await self._ai.generate_episode_insight(
                show_name=show.name,
                episode_name=episode.name,
                season=episode.season,
                number=episode.number,
                summary=episode.summary,
                genres=show.genres or [],
                comments=[]
            )
            return InsightDTO(insight=insight, source="ai")
        except Exception:
            return InsightDTO(
                insight=f"This episode of '{show.name}' offers engaging storytelling and character development.",
                source="fallback"
            )