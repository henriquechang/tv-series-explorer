from dataclasses import dataclass
from typing import Optional


@dataclass
class Show:
    id: int
    name: str
    year: Optional[int] = None
    poster_url: Optional[str] = None
    summary: Optional[str] = None
    genres: Optional[list[str]] = None

    @classmethod
    def from_tvmaze_search(cls, data: dict) -> "Show":
        show_data = data.get("show", data)
        premiered = show_data.get("premiered", "")
        year = int(premiered[:4]) if premiered else None
        image = show_data.get("image") or {}
        
        return cls(
            id=show_data["id"],
            name=show_data["name"],
            year=year,
            poster_url=image.get("medium"),
            summary=show_data.get("summary"),
            genres=show_data.get("genres", [])
        )

    @classmethod
    def from_tvmaze_show(cls, data: dict) -> "Show":
        premiered = data.get("premiered", "")
        year = int(premiered[:4]) if premiered else None
        image = data.get("image") or {}
        
        return cls(
            id=data["id"],
            name=data["name"],
            year=year,
            poster_url=image.get("original") or image.get("medium"),
            summary=data.get("summary"),
            genres=data.get("genres", [])
        )