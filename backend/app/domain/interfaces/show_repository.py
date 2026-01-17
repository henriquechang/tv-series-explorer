from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.show import Show
from app.domain.entities.episode import Episode


class ShowRepository(ABC):
    """Interface for fetching TV show data."""

    @abstractmethod
    async def search(self, query: str) -> list[Show]:
        """Search for TV shows by name."""
        pass

    @abstractmethod
    async def get_by_id(self, show_id: int) -> Optional[Show]:
        """Get a specific show by ID."""
        pass

    @abstractmethod
    async def get_episodes(self, show_id: int) -> list[Episode]:
        """Get all episodes for a show."""
        pass