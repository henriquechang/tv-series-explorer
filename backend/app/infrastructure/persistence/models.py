from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.database import Base


class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    show_id: Mapped[int] = mapped_column(Integer, index=True)
    episode_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WatchedEpisodeModel(Base):
    __tablename__ = "watched_episodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    show_id: Mapped[int] = mapped_column(Integer, index=True)
    episode_id: Mapped[int] = mapped_column(Integer, index=True)
    watched: Mapped[bool] = mapped_column(Boolean, default=True)
    watched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)