from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Comment:
    id: int
    show_id: int
    episode_id: Optional[int]
    text: str
    created_at: datetime

    @property
    def is_episode_comment(self) -> bool:
        return self.episode_id is not None