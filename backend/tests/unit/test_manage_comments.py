import pytest
from datetime import datetime
from typing import Optional

from app.domain.entities.comment import Comment
from app.domain.interfaces.comment_repository import CommentRepository
from app.application.use_cases.manage_comments import (
    AddCommentUseCase, GetCommentsUseCase, DeleteCommentUseCase
)


class FakeCommentRepository(CommentRepository):
    """Fake repository for testing."""

    def __init__(self):
        self._comments: dict[int, Comment] = {}
        self._next_id = 1

    async def add(self, show_id: int, text: str, episode_id: Optional[int] = None) -> Comment:
        comment = Comment(
            id=self._next_id,
            show_id=show_id,
            episode_id=episode_id,
            text=text,
            created_at=datetime.utcnow()
        )
        self._comments[comment.id] = comment
        self._next_id += 1
        return comment

    async def get_for_show(self, show_id: int) -> list[Comment]:
        return [
            c for c in self._comments.values()
            if c.show_id == show_id and c.episode_id is None
        ]

    async def get_for_episode(self, episode_id: int) -> list[Comment]:
        return [c for c in self._comments.values() if c.episode_id == episode_id]

    async def delete(self, comment_id: int) -> bool:
        if comment_id in self._comments:
            del self._comments[comment_id]
            return True
        return False


@pytest.fixture
def fake_comment_repo():
    return FakeCommentRepository()


class TestAddCommentUseCase:
    """Tests for AddCommentUseCase."""

    @pytest.mark.asyncio
    async def test_add_show_comment(self, fake_comment_repo):
        use_case = AddCommentUseCase(fake_comment_repo)
        
        result = await use_case.execute(show_id=100, text="Great show!")
        
        assert result.id == 1
        assert result.show_id == 100
        assert result.episode_id is None
        assert result.text == "Great show!"

    @pytest.mark.asyncio
    async def test_add_episode_comment(self, fake_comment_repo):
        use_case = AddCommentUseCase(fake_comment_repo)
        
        result = await use_case.execute(show_id=100, text="Amazing episode!", episode_id=5)
        
        assert result.episode_id == 5
        assert result.text == "Amazing episode!"

    @pytest.mark.asyncio
    async def test_empty_comment_raises_error(self, fake_comment_repo):
        use_case = AddCommentUseCase(fake_comment_repo)
        
        with pytest.raises(ValueError, match="empty"):
            await use_case.execute(show_id=100, text="")

    @pytest.mark.asyncio
    async def test_whitespace_comment_raises_error(self, fake_comment_repo):
        use_case = AddCommentUseCase(fake_comment_repo)
        
        with pytest.raises(ValueError, match="empty"):
            await use_case.execute(show_id=100, text="   ")

    @pytest.mark.asyncio
    async def test_comment_text_is_trimmed(self, fake_comment_repo):
        use_case = AddCommentUseCase(fake_comment_repo)
        
        result = await use_case.execute(show_id=100, text="  Hello World  ")
        
        assert result.text == "Hello World"

    @pytest.mark.asyncio
    async def test_comment_has_created_at(self, fake_comment_repo):
        use_case = AddCommentUseCase(fake_comment_repo)
        
        result = await use_case.execute(show_id=100, text="Test")
        
        assert result.created_at is not None


class TestGetCommentsUseCase:

    @pytest.mark.asyncio
    async def test_get_show_comments(self, fake_comment_repo):
        add_use_case = AddCommentUseCase(fake_comment_repo)
        await add_use_case.execute(show_id=100, text="Comment 1")
        await add_use_case.execute(show_id=100, text="Comment 2")
        
        get_use_case = GetCommentsUseCase(fake_comment_repo)
        results = await get_use_case.for_show(100)
        
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_get_episode_comments(self, fake_comment_repo):
        add_use_case = AddCommentUseCase(fake_comment_repo)
        await add_use_case.execute(show_id=100, text="Episode comment", episode_id=5)
        await add_use_case.execute(show_id=100, text="Show comment")
        
        get_use_case = GetCommentsUseCase(fake_comment_repo)
        results = await get_use_case.for_episode(5)
        
        assert len(results) == 1
        assert results[0].text == "Episode comment"

    @pytest.mark.asyncio
    async def test_show_comments_exclude_episode_comments(self, fake_comment_repo):
        add_use_case = AddCommentUseCase(fake_comment_repo)
        await add_use_case.execute(show_id=100, text="Show comment")
        await add_use_case.execute(show_id=100, text="Episode comment", episode_id=5)
        
        get_use_case = GetCommentsUseCase(fake_comment_repo)
        results = await get_use_case.for_show(100)
        
        assert len(results) == 1
        assert results[0].text == "Show comment"

    @pytest.mark.asyncio
    async def test_get_comments_for_nonexistent_show(self, fake_comment_repo):
        get_use_case = GetCommentsUseCase(fake_comment_repo)
        results = await get_use_case.for_show(999)
        
        assert len(results) == 0


class TestDeleteCommentUseCase:
    """Tests for DeleteCommentUseCase."""

    @pytest.mark.asyncio
    async def test_delete_existing_comment(self, fake_comment_repo):
        add_use_case = AddCommentUseCase(fake_comment_repo)
        comment = await add_use_case.execute(show_id=100, text="To delete")
        
        delete_use_case = DeleteCommentUseCase(fake_comment_repo)
        result = await delete_use_case.execute(comment.id)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_nonexistent_comment(self, fake_comment_repo):
        delete_use_case = DeleteCommentUseCase(fake_comment_repo)
        result = await delete_use_case.execute(9999)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_deleted_comment_not_returned(self, fake_comment_repo):
        add_use_case = AddCommentUseCase(fake_comment_repo)
        comment = await add_use_case.execute(show_id=100, text="To delete")
        
        delete_use_case = DeleteCommentUseCase(fake_comment_repo)
        await delete_use_case.execute(comment.id)
        
        get_use_case = GetCommentsUseCase(fake_comment_repo)
        results = await get_use_case.for_show(100)
        
        assert len(results) == 0