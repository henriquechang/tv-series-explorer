from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.show import Show
from app.domain.entities.episode import Episode


class ShowRepository(ABC):

    @abstractmethod
    async def search(self, query: str) -> list[Show]:
        pass

    @abstractmethod
    async def get_by_id(self, show_id: int) -> Optional[Show]:
        pass

    @abstractmethod
    async def get_episodes(self, show_id: int) -> list[Episode]:
        pass