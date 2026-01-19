from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.infrastructure.api.dependencies import get_show_repository
from app.domain.interfaces.show_repository import ShowRepository
from app.application.use_cases.search_shows import SearchShowsUseCase


router = APIRouter(prefix="/shows", tags=["shows"])


class ShowSearchResponse(BaseModel):
    id: int
    name: str
    year: Optional[int]
    poster_url: Optional[str]


class ShowDetailResponse(BaseModel):
    id: int
    name: str
    year: Optional[int]
    poster_url: Optional[str]
    summary: Optional[str]
    genres: list[str]


@router.get("/search", response_model=list[ShowSearchResponse])
async def search_shows(
    q: str = Query(..., description="Search query"),
    repository: ShowRepository = Depends(get_show_repository)
):
    use_case = SearchShowsUseCase(repository)
    results = await use_case.execute(q)
    return [
        ShowSearchResponse(
            id=r.id,
            name=r.name,
            year=r.year,
            poster_url=r.poster_url
        )
        for r in results
    ]


@router.get("/{show_id}", response_model=ShowDetailResponse)
async def get_show(
    show_id: int,
    repository: ShowRepository = Depends(get_show_repository)
):
    show = await repository.get_by_id(show_id)
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    
    return ShowDetailResponse(
        id=show.id,
        name=show.name,
        year=show.year,
        poster_url=show.poster_url,
        summary=show.summary,
        genres=show.genres or []
    )