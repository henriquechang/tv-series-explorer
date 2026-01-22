import os
import re
from typing import Optional

from huggingface_hub import InferenceClient

from app.domain.interfaces.ai_repository import AIRepository


class HuggingFaceAIService(AIRepository):
    """AI service using HuggingFace Inference API."""
    
    MODEL = "deepseek-ai/DeepSeek-R1-0528:fastest"
    MAX_TOKENS = 500
    TEMPERATURE = 0.7

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the HuggingFace AI service.
        
        Args:
            api_key: Optional API key. If not provided, uses HUGGINGFACE_API_KEY env var.
        """
        self._api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self._client = (
            InferenceClient(provider="auto", api_key=self._api_key)
            if self._api_key
            else None
        )

    async def generate_show_insight(
        self,
        name: str,
        summary: Optional[str],
        genres: list[str],
        comments: list[str] = None
    ) -> str:
        prompt = self._build_show_prompt(name, summary, genres, comments)
        return await self._generate(prompt)

    async def generate_episode_insight(
        self,
        show_name: str,
        episode_name: str,
        season: int,
        number: int,
        summary: Optional[str],
        genres: list[str],
        comments: list[str] = None
    ) -> str:
        prompt = self._build_episode_prompt(
            show_name, episode_name, season, number, summary, genres, comments
        )
        return await self._generate(prompt)

    def _format_comments(self, comments: Optional[list[str]]) -> Optional[str]:
        if not comments:
            return None
        # Include up to 3 most recent comments for context
        recent_comments = comments[:3]
        comments_text = " | ".join([c[:100] for c in recent_comments])
        return f"Recent viewer comments: {comments_text}"

    def _clean_summary(self, summary: Optional[str]) -> Optional[str]:
        if not summary:
            return None
        return summary.replace('<p>', '').replace('</p>', '').strip()[:500]

    def _build_show_prompt(
        self,
        name: str,
        summary: Optional[str],
        genres: list[str],
        comments: list[str] = None
    ) -> str:
        parts = [f"Write a single compelling insight about the TV show '{name}'."]
        
        if genres:
            parts.append(f"Genres: {', '.join(genres)}.")
        
        clean_summary = self._clean_summary(summary)
        if clean_summary:
            parts.append(f"Summary: {clean_summary}")
        
        formatted_comments = self._format_comments(comments)
        if formatted_comments:
            parts.append(formatted_comments)
        
        parts.append("Provide exactly 2-3 sentences that capture what makes this show unique and appealing. Do not list multiple options, just give one cohesive insight.")
        return " ".join(parts)

    def _build_episode_prompt(
        self,
        show_name: str,
        episode_name: str,
        season: int,
        number: int,
        summary: Optional[str],
        genres: list[str],
        comments: list[str] = None
    ) -> str:
        parts = [
            f"Write a single insight for episode '{episode_name}' (S{season}E{number}) from '{show_name}'."
        ]
        
        if genres:
            parts.append(f"Show genres: {', '.join(genres)}.")
        
        clean_summary = self._clean_summary(summary)
        if clean_summary:
            parts.append(f"Episode summary: {clean_summary}")
        
        formatted_comments = self._format_comments(comments)
        if formatted_comments:
            parts.append(formatted_comments)
        
        parts.append("Provide exactly 2-3 sentences about this episode's themes and significance. Do not list options, just give one cohesive insight.")
        return " ".join(parts)

    def _clean_response(self, response: str) -> str:
        """Clean common AI response patterns from the text."""
        if not response:
            return response
        
        # If "insight" appears before a colon, remove everything up to and including the colon
        if re.search(r'\binsight\b.*?:', response, flags=re.IGNORECASE):
            cleaned = re.sub(r"^.*?\binsight\b(?:.*?'[^']*')?:\s*", '', response, count=1, flags=re.IGNORECASE)
            return cleaned.strip()
        
        return response.strip()

    async def _generate(self, prompt: str) -> str:
        if not self._client:
            return self._fallback_insight(prompt)
            
        try:
            response = await self._call_deepseek_api(prompt)
            result = response.choices[0].message.content
            
            if not result:
                return self._fallback_insight(prompt)
            
            # Extract the actual insight response from DeepSeek's <think> tags."""
            if '</think>' in result:
                parts = result.split('</think>')
                if len(parts) > 1:
                    result = parts[-1].strip()
            
            result = self._clean_response(result)
            
            return result if result else self._fallback_insight(prompt)
            
        except Exception as e:
            print(f"Error calling DeepSeek API: {e}")
            return self._fallback_insight(prompt)
    
    async def _call_deepseek_api(self, prompt: str):
        return self._client.chat.completions.create(
            model=self.MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.MAX_TOKENS,
            temperature=self.TEMPERATURE
        )

    def _fallback_insight(self, prompt: str) -> str:
        """Generate a simple fallback insight when API is unavailable."""
        if "episode" in prompt.lower():
            return "This episode has a good story and interesting characters that fans will enjoy."
        return "This is a great show with good stories and characters that many people love to watch."


class FallbackAIService(AIRepository):
    """Fallback AI service that provides static insights when the API is unavailable."""

    async def generate_show_insight(
        self,
        name: str,
        summary: Optional[str],
        genres: list[str],
        comments: list[str] = None
    ) -> str:
        genre_text = f"As a {'/'.join(genres[:2])} series, " if genres else ""
        return (
            f"{genre_text}'{name}' is a fun show to watch "
            f"with good stories and nice characters."
        )

    async def generate_episode_insight(
        self,
        show_name: str,
        episode_name: str,
        season: int,
        number: int,
        summary: Optional[str],
        genres: list[str],
        comments: list[str] = None
    ) -> str:
        return (
            f"This episode of '{show_name}' continues the story "
            f"with interesting events and good character moments "
            f"that fans will like."
        )