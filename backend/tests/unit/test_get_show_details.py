import pytest
from app.application.use_cases.get_show_details import GetShowDetailsUseCase


class TestGetShowDetailsUseCase:
    """Tests for GetShowDetailsUseCase"""

    @pytest.mark.asyncio
    async def test_returns_show_with_grouped_episodes(self, fake_repository):
        use_case = GetShowDetailsUseCase(fake_repository)
        result = await use_case.execute(1)  # Breaking Bad

        assert result is not None
        assert result.id == 1
        assert result.name == "Breaking Bad"
        assert len(result.seasons) == 2
        
        # Verify grouping and sorting
        season_numbers = [s.season_number for s in result.seasons]
        assert season_numbers == [1, 2]  # Sorted by season
        
        season_1 = result.seasons[0]
        assert len(season_1.episodes) == 2
        assert all(e.season == 1 for e in season_1.episodes)
        assert [e.number for e in season_1.episodes] == [1, 2]  # Sorted by episode
        
        season_2 = result.seasons[1]
        assert len(season_2.episodes) == 1
        assert season_2.episodes[0].season == 2

    @pytest.mark.asyncio
    async def test_returns_none_for_invalid_show(self, fake_repository):
        use_case = GetShowDetailsUseCase(fake_repository)
        result = await use_case.execute(9999)

        assert result is None

    @pytest.mark.asyncio
    async def test_show_with_no_episodes_returns_empty_seasons(self, fake_repository):
        use_case = GetShowDetailsUseCase(fake_repository)
        result = await use_case.execute(2)  # Game of Thrones (no episodes in fixture)

        assert result is not None
        assert result.name == "Game of Thrones"
        assert len(result.seasons) == 0

    @pytest.mark.asyncio
    async def test_includes_all_show_metadata(self, fake_repository):
        use_case = GetShowDetailsUseCase(fake_repository)
        result = await use_case.execute(1)

        assert result.year == 2008
        assert result.poster_url == "http://example.com/bb.jpg"
        assert "Drama" in result.genres
        assert "Crime" in result.genres
        assert result.summary is not None