from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.infrastructure.api.dependencies import get_show_repository, get_ai_service, get_comment_repository
from app.application.use_cases.get_ai_insight import GetShowInsightUseCase, GetEpisodeInsightUseCase


router = APIRouter(tags=["ai"])


class InsightResponse(BaseModel):
    insight: str
    source: str


@router.get("/shows/{show_id}/insight", response_model=InsightResponse)
async def get_show_insight(
    show_id: int,
    show_repository=Depends(get_show_repository),
    ai_service=Depends(get_ai_service),
    comment_repository=Depends(get_comment_repository)
):
    use_case = GetShowInsightUseCase(ai_service, show_repository, comment_repository)
    
    result = await use_case.execute(show_id)
    if not result:
        raise HTTPException(status_code=404, detail="Show not found")
    
    return InsightResponse(insight=result.insight, source=result.source)


@router.get("/shows/{show_id}/episodes/{episode_id}/insight", response_model=InsightResponse)
async def get_episode_insight(
    show_id: int,
    episode_id: int,
    show_repository=Depends(get_show_repository),
    ai_service=Depends(get_ai_service),
    comment_repository=Depends(get_comment_repository)
):
    use_case = GetEpisodeInsightUseCase(ai_service, show_repository, comment_repository)
    
    result = await use_case.execute(show_id, episode_id)
    if not result:
        raise HTTPException(status_code=404, detail="Show or episode not found")
    
    return InsightResponse(insight=result.insight, source=result.source)