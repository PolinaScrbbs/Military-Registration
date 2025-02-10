from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from ..content.models import Base, BaseEnum
from .schemes import NewsResponse


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String(32), unique=True, nullable=False)
    content = Column(String(128), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    last_updated_at = Column(DateTime, default=None)

    creator = relationship("User", back_populates="news")

    __table_args__ = (UniqueConstraint("title", "content", name="_title_content_uc"),)

    async def to_pydantic(self) -> NewsResponse:
        date_format = "%H:%M %d.%m.%Y"
        return NewsResponse(
            id=self.id,
            title=self.title,
            content=self.content,
            creator=await self.creator.to_base_user(),
            created_at=self.created_at.strftime(date_format),
            last_updated=(
                self.last_updated_at.strftime(date_format)
                if self.last_updated_at
                else None
            ),
        )
