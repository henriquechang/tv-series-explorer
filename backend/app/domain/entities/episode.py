from dataclasses import dataclass
from typing import Optional


@dataclass
class Episode:
    """Episode info"""
    id: int
    show_id: int
    season: int
    number: int
    name: str
    summary: Optional[str] = None
    airdate: Optional[str] = None
    runtime: Optional[int] = None

    @classmethod
    def from_tvmaze(cls, data: dict, show_id: int) -> "Episode":
        """Build episode from API data"""
        return cls(
            id=data["id"],
            show_id=show_id,
            season=data["season"],
            number=data["number"],
            name=data["name"],
            summary=data.get("summary"),
            airdate=data.get("airdate"),
            runtime=data.get("runtime")
        )