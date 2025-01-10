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

from ..user.models import Base, BaseEnum


class ContentCategory(BaseEnum):
    REGULATORY_DOCUMENT = "regulatory_document"
    DOCUMENT_FOR_MILITARY_REGISTRATION = "document_for_military_registration"
    ALTERNATIVE_CIVILIAN_SERVICE_DOCUMENT = "alternative_civilian_service_document"
    CONTRACT_SERVICE_DOCUMENT = "contract_service_document"
    GALLERY = "gallery"


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True)
    filename = Column(String(256), nullable=False)
    path = Column(String(256), nullable=False, unique=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    category = Column(Enum(ContentCategory), nullable=False)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    last_updated_at = Column(DateTime, default=None)

    creator = relationship("User", back_populates="contents")

    __table_args__ = (
        UniqueConstraint("filename", "category", name="_filename_category_uc"),
    )

    async def archive(self):
        self.is_archived = True
        self.last_updated_at = datetime.now()

    async def unarchived(self):
        self.is_archived = False
        self.last_updated_at = datetime.now()

    async def to_pydantic(self):
        date_format = "%H:%M %d.%m.%Y"
        return {
            "id": self.id,
            "filename": self.filename,
            "path": self.path,
            "category": self.category,
            "creator": await self.creator.to_base_user(),
            "is_archived": self.is_archived,
            "created_at": self.created_at.strftime(date_format),
            "last_updated_at": (
                self.last_updated_at.strftime(date_format)
                if self.last_updated_at
                else None
            ),
        }
