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
    STUDENTS = "students"
    GALLERY = "gallery"
    PATRIOTIC_EDUCATION = "patriotic_education"
    EVENTS = "events"
    MILITARY_TRAINING_CAMPS = "military_training_camps"
    ADDRESS_AND_LINKS = "addresses_and_links"
    CONTACTS = "contacts"

    @staticmethod
    async def get_category_names() -> dict:
        category_names = {
            ContentCategory.REGULATORY_DOCUMENT: "Нормативный документ",
            ContentCategory.DOCUMENT_FOR_MILITARY_REGISTRATION: "Документ для воинского учета",
            ContentCategory.ALTERNATIVE_CIVILIAN_SERVICE_DOCUMENT: "Документ альтернативной гражданской службы",
            ContentCategory.CONTRACT_SERVICE_DOCUMENT: "Документ контрактной службы",
            ContentCategory.STUDENTS: "Студенты",
            ContentCategory.GALLERY: "Галерея",
            ContentCategory.PATRIOTIC_EDUCATION: "Патриотическое воспитание",
            ContentCategory.EVENTS: "События",
            ContentCategory.MILITARY_TRAINING_CAMPS: "Военные сборы",
            ContentCategory.ADDRESS_AND_LINKS: "Адреса и ссылки",
            ContentCategory.CONTACTS: "Контакты",
        }
        return category_names

    @staticmethod
    async def get_category_name(category: "ContentCategory") -> str:
        category_names = await ContentCategory.get_category_names()
        return category_names.get(category, category.value)


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True)
    filename = Column(String(256), nullable=False)
    path = Column(String(256), nullable=False, unique=True)
    extension = Column(String(7), nullable=False)
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
            "extension": self.extension,
            "path": self.path,
            "category": await ContentCategory.get_category_name(self.category),
            "creator": await self.creator.to_base_user(),
            "is_archived": self.is_archived,
            "created_at": self.created_at.strftime(date_format),
            "last_updated_at": (
                self.last_updated_at.strftime(date_format)
                if self.last_updated_at
                else None
            ),
        }
