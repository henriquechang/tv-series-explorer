from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.infrastructure.api.dependencies import get_show_repository
from app.domain.interfaces.show_repository import ShowRepository
from app.application.use_cases.get_show_details import GetShowDetailsUseCase


router = APIRouter(prefix="/shows", tags=["episodes"])


class EpisodeResponse(BaseModel):
    id: int
    season: int
    number: int
    name: str
    summary: Optional[str]
    airdate: Optional[str]


class SeasonResponse(BaseModel):
    season_number: int
    episodes: list[EpisodeResponse]


class ShowWithEpisodesResponse(BaseModel):
    id: int
    name: str
    year: Optional[int]
    poster_url: Optional[str]
    summary: Optional[str]
    genres: list[str]
    seasons: list[SeasonResponse]


@router.get("/{show_id}/details", response_model=ShowWithEpisodesResponse)
async def get_show_with_episodes(
    show_id: int,
    repository: ShowRepository = Depends(get_show_repository)
):
    use_case = GetShowDetailsUseCase(repository)
    result = await use_case.execute(show_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Show not found")
    
    return ShowWithEpisodesResponse(
        id=result.id,
        name=result.name,
        year=result.year,
        poster_url=result.poster_url,
        summary=result.summary,
        genres=result.genres,
        seasons=[
            SeasonResponse(
                season_number=s.season_number,
                episodes=[
                    EpisodeResponse(**e.__dict__)
                    for e in s.episodes
                ]
            )
            for s in result.seasons
        ]
    )