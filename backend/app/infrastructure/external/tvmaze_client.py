from typing import Optional
import httpx

from app.domain.entities.show import Show
from app.domain.entities.episode import Episode
from app.domain.interfaces.show_repository import ShowRepository


class TVMazeClient(ShowRepository):

    BASE_URL = "http://api.tvmaze.com"

    def __init__(self, client: Optional[httpx.AsyncClient] = None):
        self._client = client

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=10.0)
        return self._client

    async def search(self, query: str) -> list[Show]:
        if not query or not query.strip():
            return []

        client = await self._get_client()
        response = await client.get(
            f"{self.BASE_URL}/search/shows",
            params={"q": query}
        )
        response.raise_for_status()
        
        results = response.json()
        return [Show.from_tvmaze_search(item) for item in results]

    async def get_by_id(self, show_id: int) -> Optional[Show]:
        client = await self._get_client()
        response = await client.get(f"{self.BASE_URL}/shows/{show_id}")
        
        if response.status_code == 404:
            return None
        
        response.raise_for_status()
        return Show.from_tvmaze_show(response.json())

    async def get_episodes(self, show_id: int) -> list[Episode]:
        client = await self._get_client()
        response = await client.get(f"{self.BASE_URL}/shows/{show_id}/episodes")
        
        if response.status_code == 404:
            return []
        
        response.raise_for_status()
        results = response.json()
        return [Episode.from_tvmaze(ep, show_id) for ep in results]

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None