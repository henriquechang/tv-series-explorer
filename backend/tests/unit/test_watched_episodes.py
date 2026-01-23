import pytest
from datetime import datetime
from typing import List, Optional

from app.infrastructure.persistence.models import WatchedEpisodeModel
from app.infrastructure.persistence.repositories.watched_episode import WatchedEpisodeRepository


class FakeWatchedEpisodeRepository:
    """Fake repository for testing."""

    def __init__(self):
        self._watched_episodes: dict[tuple[int, int], WatchedEpisodeModel] = {}
        self._next_id = 1

    async def get_watched_episodes(self, show_id: Optional[int] = None) -> List[WatchedEpisodeModel]:
        episodes = list(self._watched_episodes.values())
        if show_id:
            episodes = [ep for ep in episodes if ep.show_id == show_id]
        return episodes

    async def is_episode_watched(self, show_id: int, episode_id: int) -> bool:
        return (show_id, episode_id) in self._watched_episodes

    async def mark_watched(self, show_id: int, episode_id: int) -> WatchedEpisodeModel:
        key = (show_id, episode_id)
        if key in self._watched_episodes:
            return self._watched_episodes[key]
        
        watched = WatchedEpisodeModel(
            id=self._next_id,
            show_id=show_id,
            episode_id=episode_id,
            watched=True,
            watched_at=datetime.utcnow()
        )
        self._watched_episodes[key] = watched
        self._next_id += 1
        return watched

    async def unmark_watched(self, show_id: int, episode_id: int) -> bool:
        key = (show_id, episode_id)
        if key in self._watched_episodes:
            del self._watched_episodes[key]
            return True
        return False


@pytest.fixture
def fake_watched_repo():
    return FakeWatchedEpisodeRepository()


class TestMarkWatched:
    """Tests for marking episodes as watched."""

    @pytest.mark.asyncio
    async def test_mark_new_episode_watched(self, fake_watched_repo):
        result = await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        
        assert result.id == 1
        assert result.show_id == 100
        assert result.episode_id == 1
        assert result.watched is True
        assert result.watched_at is not None

    @pytest.mark.asyncio
    async def test_mark_already_watched_episode_returns_existing(self, fake_watched_repo):
        first = await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        second = await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        
        assert first.id == second.id
        assert first.show_id == second.show_id
        assert first.episode_id == second.episode_id

    @pytest.mark.asyncio
    async def test_mark_different_episodes_creates_separate_entries(self, fake_watched_repo):
        first = await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        second = await fake_watched_repo.mark_watched(show_id=100, episode_id=2)
        
        assert first.id != second.id
        assert first.episode_id == 1
        assert second.episode_id == 2

    @pytest.mark.asyncio
    async def test_mark_same_episode_different_shows(self, fake_watched_repo):
        show1 = await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        show2 = await fake_watched_repo.mark_watched(show_id=200, episode_id=1)
        
        assert show1.id != show2.id
        assert show1.show_id == 100
        assert show2.show_id == 200


class TestUnmarkWatched:
    """Tests for unmarking watched episodes."""

    @pytest.mark.asyncio
    async def test_unmark_existing_watched_episode(self, fake_watched_repo):
        await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        result = await fake_watched_repo.unmark_watched(show_id=100, episode_id=1)
        
        assert result is True
        is_watched = await fake_watched_repo.is_episode_watched(100, 1)
        assert is_watched is False

    @pytest.mark.asyncio
    async def test_unmark_nonexistent_episode_returns_false(self, fake_watched_repo):
        result = await fake_watched_repo.unmark_watched(show_id=999, episode_id=999)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_unmark_only_affects_specific_episode(self, fake_watched_repo):
        await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        await fake_watched_repo.mark_watched(show_id=100, episode_id=2)
        
        await fake_watched_repo.unmark_watched(show_id=100, episode_id=1)
        
        assert await fake_watched_repo.is_episode_watched(100, 1) is False
        assert await fake_watched_repo.is_episode_watched(100, 2) is True


class TestIsEpisodeWatched:
    """Tests for checking if episodes are watched."""

    @pytest.mark.asyncio
    async def test_new_episode_is_not_watched(self, fake_watched_repo):
        result = await fake_watched_repo.is_episode_watched(100, 1)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_marked_episode_is_watched(self, fake_watched_repo):
        await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        result = await fake_watched_repo.is_episode_watched(100, 1)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_unmarked_episode_is_not_watched(self, fake_watched_repo):
        await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        await fake_watched_repo.unmark_watched(show_id=100, episode_id=1)
        
        result = await fake_watched_repo.is_episode_watched(100, 1)
        
        assert result is False


class TestGetWatchedEpisodes:
    """Tests for retrieving watched episodes."""

    @pytest.mark.asyncio
    async def test_get_all_watched_episodes(self, fake_watched_repo):
        await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        await fake_watched_repo.mark_watched(show_id=200, episode_id=1)
        await fake_watched_repo.mark_watched(show_id=100, episode_id=2)
        
        result = await fake_watched_repo.get_watched_episodes()
        
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_get_watched_episodes_for_specific_show(self, fake_watched_repo):
        await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        await fake_watched_repo.mark_watched(show_id=100, episode_id=2)
        await fake_watched_repo.mark_watched(show_id=200, episode_id=1)
        
        result = await fake_watched_repo.get_watched_episodes(show_id=100)
        
        assert len(result) == 2
        assert all(ep.show_id == 100 for ep in result)

    @pytest.mark.asyncio
    async def test_get_empty_list_for_show_with_no_watched_episodes(self, fake_watched_repo):
        await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        
        result = await fake_watched_repo.get_watched_episodes(show_id=200)
        
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_empty_list_when_no_episodes_watched(self, fake_watched_repo):
        result = await fake_watched_repo.get_watched_episodes()
        
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_unmarked_episodes_not_in_watched_list(self, fake_watched_repo):
        await fake_watched_repo.mark_watched(show_id=100, episode_id=1)
        await fake_watched_repo.mark_watched(show_id=100, episode_id=2)
        await fake_watched_repo.unmark_watched(show_id=100, episode_id=1)
        
        result = await fake_watched_repo.get_watched_episodes(show_id=100)
        
        assert len(result) == 1
        assert result[0].episode_id == 2