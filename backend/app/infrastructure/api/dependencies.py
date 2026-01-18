from app.domain.interfaces.show_repository import ShowRepository
from app.infrastructure.external.tvmaze_client import TVMazeClient

# Singleton instance
_tvmaze_client: TVMazeClient | None = None


def get_show_repository() -> ShowRepository:
    """Dependency injection for ShowRepository."""
    global _tvmaze_client
    if _tvmaze_client is None:
        _tvmaze_client = TVMazeClient()
    return _tvmaze_client


async def cleanup_clients():
    """Cleanup HTTP clients on shutdown."""
    global _tvmaze_client
    if _tvmaze_client:
        await _tvmaze_client.close()
        _tvmaze_client = None