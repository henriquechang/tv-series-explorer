import pytest
from unittest.mock import patch, MagicMock
from app.infrastructure.ai.huggingfaceai_service import HuggingFaceAIService, FallbackAIService


class TestHuggingFaceAIService:
    """Tests for the HuggingFaceAIService class."""
    
    @pytest.fixture
    def service_with_key(self):
        with patch.dict('os.environ', {'HUGGINGFACE_API_KEY': 'test_key'}):
            service = HuggingFaceAIService()
            return service
    
    @pytest.fixture
    def service_without_key(self):
        with patch.dict('os.environ', {}, clear=True):
            service = HuggingFaceAIService()
            return service
    
    @pytest.mark.asyncio
    async def test_generate_show_insight_without_api_key(self, service_without_key):
        result = await service_without_key.generate_show_insight(
            name="Test Show",
            summary="A test summary",
            genres=["Drama", "Crime"],
            comments=[]
        )
        
        assert result is not None
        assert "great show" in result
    
    @pytest.mark.asyncio
    async def test_generate_episode_insight_without_api_key(self, service_without_key):
        result = await service_without_key.generate_episode_insight(
            show_name="Test Show",
            episode_name="Pilot",
            season=1,
            number=1,
            summary="Episode summary",
            genres=["Drama"],
            comments=[]
        )
        
        assert result is not None
        assert "episode" in result.lower()
    
    def test_build_show_prompt(self, service_with_key):
        prompt = service_with_key._build_show_prompt(
            name="Breaking Bad",
            summary="<p>A chemistry teacher turns to crime</p>",
            genres=["Drama", "Crime"],
            comments=None
        )
        
        assert "Breaking Bad" in prompt
        assert "Drama, Crime" in prompt
        assert "chemistry teacher" in prompt
        assert "<p>" not in prompt 
        assert "2-3 sentences" in prompt
    
    def test_build_episode_prompt(self, service_with_key):
        prompt = service_with_key._build_episode_prompt(
            show_name="Breaking Bad",
            episode_name="Pilot",
            season=1,
            number=1,
            summary="Walt starts cooking",
            genres=["Drama", "Crime"],
            comments=None
        )
        
        assert "Breaking Bad" in prompt
        assert "Pilot" in prompt
        assert "S1E1" in prompt
        assert "Walt starts cooking" in prompt
    
    @pytest.mark.asyncio
    async def test_generate_with_api_success(self, service_with_key):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "<think>Thinking</think>Great insight about the show."
        
        with patch.object(service_with_key, '_call_deepseek_api', return_value=mock_response):
            result = await service_with_key._generate("Test prompt")
            assert result == "Great insight about the show."
    
    @pytest.mark.asyncio
    async def test_generate_with_api_failure(self, service_with_key):
        with patch.object(service_with_key, '_call_deepseek_api', side_effect=Exception("API Error")):
            result = await service_with_key._generate("Test prompt")
            assert result is not None
            assert "great show" in result  # Should use fallback
    
    def test_clean_response_removes_insight_prefix(self, service_with_key):
        result = service_with_key._clean_response("Here's a single compelling insight: The show is amazing")
        assert result == "The show is amazing"
        
        result = service_with_key._clean_response("INSIGHT: Great story")
        assert result == "Great story"
        
        result = service_with_key._clean_response("Here's a compelling insight about 'Parasyte: The Grey': This show brilliantly explores themes of identity")
        assert result == "This show brilliantly explores themes of identity"
        
        result = service_with_key._clean_response("An interesting insight: The show explores: complex themes and ideas")
        assert result == "The show explores: complex themes and ideas"
        
        result = service_with_key._clean_response("This show explores complex themes")
        assert result == "This show explores complex themes"

        assert service_with_key._clean_response("") == ""
        assert service_with_key._clean_response(None) == None


class TestFallbackAIService:
    """Tests for the FallbackAIService class."""
    
    @pytest.fixture
    def service(self):
        return FallbackAIService()
    
    @pytest.mark.asyncio
    async def test_generate_show_insight(self, service):
        result = await service.generate_show_insight(
            name="Test Show",
            summary="Summary",
            genres=["Drama", "Action"],
            comments=[]
        )
        
        assert "Test Show" in result
        assert "Drama/Action" in result
        assert "fun show" in result
    
    @pytest.mark.asyncio
    async def test_generate_episode_insight(self, service):
        result = await service.generate_episode_insight(
            show_name="Test Show",
            episode_name="Episode 1",
            season=1,
            number=1,
            summary="Summary",
            genres=["Drama"],
            comments=[]
        )
        
        assert "Test Show" in result
        assert "continues the story" in result