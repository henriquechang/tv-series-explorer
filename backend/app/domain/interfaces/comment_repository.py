from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.comment import Comment


class CommentRepository(ABC):

    @abstractmethod
    async def add(self, show_id: int, text: str, episode_id: Optional[int] = None) -> Comment:
        pass

    @abstractmethod
    async def get_for_show(self, show_id: int) -> list[Comment]:
        pass

    @abstractmethod
    async def get_for_episode(self, episode_id: int) -> list[Comment]:
        pass

    @abstractmethod
    async def delete(self, comment_id: int) -> bool:
        pass