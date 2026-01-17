import pytest
from app.domain.entities.show import Show
from app.domain.entities.episode import Episode


class TestShowEntity:
    """Tests for Show entity."""

    def test_create_show_with_all_fields(self):
        show = Show(
            id=1,
            name="Breaking Bad",
            year=2008,
            poster_url="http://example.com/poster.jpg",
            summary="Hello",
            genres=["Drama", "Crime"]
        )
        assert show.id == 1
        assert show.name == "Breaking Bad"
        assert show.year == 2008
        assert show.genres == ["Drama", "Crime"]

    def test_create_show_with_minimal_fields(self):
        show = Show(id=1, name="Test Show")
        assert show.id == 1
        assert show.name == "Test Show"
        assert show.year is None
        assert show.poster_url is None

    def test_from_tvmaze_search_response(self):
        api_response = {
            "score": 0.9,
            "show": {
                "id": 169,
                "name": "Breaking Bad",
                "premiered": "2008-01-20",
                "image": {"medium": "http://example.com/medium.jpg"},
                "summary": "<p>Hello</p>",
                "genres": ["Drama", "Crime", "Thriller"]
            }
        }
        show = Show.from_tvmaze_search(api_response)
        assert show.id == 169
        assert show.name == "Breaking Bad"
        assert show.year == 2008
        assert show.poster_url == "http://example.com/medium.jpg"

    def test_from_tvmaze_search_with_missing_image(self):
        api_response = {
            "show": {
                "id": 1,
                "name": "Test",
                "premiered": "2020-01-01",
                "image": None,
                "genres": []
            }
        }
        show = Show.from_tvmaze_search(api_response)
        assert show.poster_url is None

    def test_from_tvmaze_search_with_missing_premiered(self):
        api_response = {
            "show": {
                "id": 1,
                "name": "Test",
                "premiered": None,
                "image": None,
                "genres": []
            }
        }
        show = Show.from_tvmaze_search(api_response)
        assert show.year is None


class TestEpisodeEntity:
    """Tests for Episode entity."""

    def test_create_episode(self):
        episode = Episode(
            id=1,
            show_id=100,
            season=1,
            number=1,
            name="Hi",
            summary="First"
        )
        assert episode.id == 1
        assert episode.show_id == 100
        assert episode.season == 1
        assert episode.number == 1

    def test_from_tvmaze_response(self):
        api_response = {
            "id": 1,
            "season": 2,
            "number": 5,
            "name": "Episode Title",
            "summary": "<p>Episode Summary</p>",
            "airdate": "2020-05-15",
            "runtime": 60
        }
        episode = Episode.from_tvmaze(api_response, show_id=100)
        assert episode.id == 1
        assert episode.show_id == 100
        assert episode.season == 2
        assert episode.number == 5
        assert episode.name == "Episode Title"
        assert episode.runtime == 60