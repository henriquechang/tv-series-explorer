from abc import ABC, abstractmethod
from typing import Optional


class AIRepository(ABC):

    @abstractmethod
    async def generate_show_insight(
        self,
        name: str,
        summary: Optional[str],
        genres: list[str],
        comments: list[str] = None
    ) -> str:
        pass

    @abstractmethod
    async def generate_episode_insight(
        self,
        show_name: str,
        episode_name: str,
        season: int,
        number: int,
        summary: Optional[str],
        genres: list[str],
        comments: list[str] = None
    ) -> str:
        pass