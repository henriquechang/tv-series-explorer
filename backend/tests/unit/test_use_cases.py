import pytest
from app.application.use_cases.search_shows import SearchShowsUseCase


class TestSearchShowsUseCase:

    @pytest.mark.asyncio
    async def test_finds_matching_shows(self, fake_repository):
        use_case = SearchShowsUseCase(fake_repository)
        results = await use_case.execute("Breaking")
        
        assert len(results) == 1
        assert results[0].name == "Breaking Bad"
        assert results[0].id == 1

    @pytest.mark.asyncio
    async def test_case_insensitive_search(self, fake_repository):
        use_case = SearchShowsUseCase(fake_repository)
        results = await use_case.execute("breaking")
        
        assert len(results) == 1
        assert results[0].name == "Breaking Bad"

    @pytest.mark.asyncio
    async def test_multiple_results(self, fake_repository):
        use_case = SearchShowsUseCase(fake_repository)
        # "Of" appears in "The Office" and "Game of Thrones"
        results = await use_case.execute("Of")
        
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_no_results_when_nothing_found(self, fake_repository):
        use_case = SearchShowsUseCase(fake_repository)
        results = await use_case.execute("NonexistentShow")
        
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_empty_query(self, fake_repository):
        use_case = SearchShowsUseCase(fake_repository)
        results = await use_case.execute("")
        
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_whitespace_handling(self, fake_repository):
        use_case = SearchShowsUseCase(fake_repository)
        results = await use_case.execute("  Breaking  ")
        
        assert len(results) == 1
        assert results[0].name == "Breaking Bad"

    @pytest.mark.asyncio
    async def test_result_fields(self, fake_repository):
        use_case = SearchShowsUseCase(fake_repository)
        results = await use_case.execute("Breaking Bad")
        
        result = results[0]
        assert result.id == 1
        assert result.name == "Breaking Bad"
        assert result.year == 2008
        assert result.poster_url == "http://example.com/bb.jpg"