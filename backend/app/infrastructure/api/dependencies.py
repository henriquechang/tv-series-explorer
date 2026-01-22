from app.domain.interfaces.show_repository import ShowRepository
from app.domain.interfaces.ai_repository import AIRepository
from app.domain.interfaces.comment_repository import CommentRepository
from app.infrastructure.external.tvmaze_client import TVMazeClient
from app.infrastructure.ai.huggingfaceai_service import HuggingFaceAIService
from app.infrastructure.persistence.repositories.comment import SQLAlchemyCommentRepository
from app.infrastructure.persistence.database import get_session

_tvmaze_client: TVMazeClient | None = None
_ai_service: HuggingFaceAIService | None = None


def get_show_repository() -> ShowRepository:
    global _tvmaze_client
    if _tvmaze_client is None:
        _tvmaze_client = TVMazeClient()
    return _tvmaze_client

def get_ai_service() -> AIRepository:
    global _ai_service
    if _ai_service is None:
        _ai_service = HuggingFaceAIService()
    return _ai_service

async def get_comment_repository() -> CommentRepository:
    async for session in get_session():
        yield SQLAlchemyCommentRepository(session)

async def cleanup_clients():
    global _tvmaze_client
    if _tvmaze_client:
        await _tvmaze_client.close()
        _tvmaze_client = None