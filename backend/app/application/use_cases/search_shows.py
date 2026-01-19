from dataclasses import dataclass
from typing import Optional

from app.domain.interfaces.show_repository import ShowRepository


@dataclass
class ShowSearchResult:
    id: int
    name: str
    year: Optional[int]
    poster_url: Optional[str]


class SearchShowsUseCase:

    def __init__(self, show_repository: ShowRepository):
        self._repository = show_repository

    async def execute(self, query: str) -> list[ShowSearchResult]:
        if not query:
            return []

        shows = await self._repository.search(query.strip())
        
        return [
            ShowSearchResult(
                id=show.id,
                name=show.name,
                year=show.year,
                poster_url=show.poster_url
            )
            for show in shows
        ]