import pytest
from typing import Optional

from app.domain.entities.show import Show
from app.domain.entities.episode import Episode
from app.domain.interfaces.show_repository import ShowRepository


class FakeShowRepository(ShowRepository):
    """Fake repository for testing."""

    def __init__(self, shows: list[Show] = None, episodes: list[Episode] = None):
        self._shows = shows or []
        self._episodes = episodes or []

    async def search(self, query: str) -> list[Show]:
        query_lower = query.lower()
        return [s for s in self._shows if query_lower in s.name.lower()]

    async def get_by_id(self, show_id: int) -> Optional[Show]:
        for show in self._shows:
            if show.id == show_id:
                return show
        return None

    async def get_episodes(self, show_id: int) -> list[Episode]:
        return [e for e in self._episodes if e.show_id == show_id]


@pytest.fixture
def sample_shows():
    return [
        Show(id=1, name="Breaking Bad", year=2008, poster_url="http://example.com/bb.jpg",
             summary="Chemistry", genres=["Drama", "Crime"]),
        Show(id=2, name="Game of Thrones", year=2011, poster_url="http://example.com/got.jpg",
             summary="Fantasy epic", genres=["Drama", "Fantasy"]),
        Show(id=3, name="The Office", year=2005, poster_url="http://example.com/office.jpg",
             summary="Mock", genres=["Comedy"]),
    ]


@pytest.fixture
def sample_episodes():
    return [
        Episode(id=1, show_id=1, season=1, number=1, name="Hello", summary="Walter"),
        Episode(id=2, show_id=1, season=1, number=2, name="Hello 2", summary="White"),
        Episode(id=3, show_id=1, season=2, number=1, name="Hello 3", summary="Hi"),
    ]


@pytest.fixture
def fake_repository(sample_shows, sample_episodes):
    return FakeShowRepository(shows=sample_shows, episodes=sample_episodes)