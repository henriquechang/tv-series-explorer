from dataclasses import dataclass
from typing import Optional
from collections import defaultdict

from app.domain.interfaces.show_repository import ShowRepository
from app.domain.entities.episode import Episode


@dataclass
class EpisodeDTO:
    id: int
    season: int
    number: int
    name: str
    summary: Optional[str]
    airdate: Optional[str]


@dataclass
class SeasonDTO:
    season_number: int
    episodes: list[EpisodeDTO]


@dataclass
class ShowDetailsDTO:
    id: int
    name: str
    year: Optional[int]
    poster_url: Optional[str]
    summary: Optional[str]
    genres: list[str]
    seasons: list[SeasonDTO]


class GetShowDetailsUseCase:

    def __init__(self, show_repository: ShowRepository):
        self._repository = show_repository

    async def execute(self, show_id: int) -> Optional[ShowDetailsDTO]:
        show = await self._repository.get_by_id(show_id)
        if not show:
            return None

        episodes = await self._repository.get_episodes(show_id)
        seasons = self._group_episodes_by_season(episodes)

        return ShowDetailsDTO(
            id=show.id,
            name=show.name,
            year=show.year,
            poster_url=show.poster_url,
            summary=show.summary,
            genres=show.genres or [],
            seasons=seasons
        )

    def _group_episodes_by_season(self, episodes: list[Episode]) -> list[SeasonDTO]:
        seasons_dict = defaultdict(list)
        
        for ep in episodes:
            episode_dto = EpisodeDTO(
                id=ep.id,
                season=ep.season,
                number=ep.number,
                name=ep.name,
                summary=ep.summary,
                airdate=ep.airdate
            )
            seasons_dict[ep.season].append(episode_dto)

        return [
            SeasonDTO(
                season_number=num, 
                episodes=sorted(eps, key=lambda e: e.number)
            )
            for num, eps in sorted(seasons_dict.items())
        ]