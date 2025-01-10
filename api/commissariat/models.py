from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from ..content.models import Base
from .schemes import CommissariatUrlType, CommissariatPhoneType


class Commissioner(Base):
    __tablename__ = "commissioners"
    __table_args__ = (
        UniqueConstraint(
            "name", "surname", "patronymic", name="_name_surname_patronymic_uc"
        ),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    surname = Column(String(256), nullable=False)
    patronymic = Column(String(256), nullable=False)

    commissariat = relationship("Commissariat", back_populates="commissioner")

    async def to_pydantic(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "patronymic": self.patronymic,
        }


class CommissariatUrl(Base):
    __tablename__ = "commissariat_urls"
    __table_args__ = (UniqueConstraint("url", "type", name="_url_type_uc"),)

    id = Column(Integer, primary_key=True)
    url = Column(String(256), nullable=False)
    type = Column(Enum(CommissariatUrlType), nullable=False)
    commissariat_id = Column(Integer, ForeignKey("commissariats.id"), nullable=False)

    commissariat = relationship("Commissariat", back_populates="urls")

    async def to_pydantic(self):
        return {
            "id": self.id,
            "url": self.url,
            "type": self.type,
        }


class CommissariatPhone(Base):
    __tablename__ = "commissariat_phones"
    __table_args__ = (UniqueConstraint("phone", name="_phone_uc"),)

    id = Column(Integer, primary_key=True)
    phone = Column(String(256), nullable=False)
    type = Column(Enum(CommissariatPhoneType), nullable=False)
    commissariat_id = Column(Integer, ForeignKey("commissariats.id"), nullable=False)

    commissariat = relationship("Commissariat", back_populates="phones")

    async def to_pydantic(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "type": self.type,
        }


class Commissariat(Base):
    __tablename__ = "commissariats"
    __table_args__ = (UniqueConstraint("name", "address", name="_name_address_uc"),)

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    address = Column(String(256), nullable=False)
    commissioner_id = Column(Integer, ForeignKey("commissioners.id"))

    commissioner = relationship("Commissioner", back_populates="commissariat")
    urls = relationship("CommissariatUrl", back_populates="commissariat")
    phones = relationship("CommissariatPhone", back_populates="commissariat")

    async def to_pydantic(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "commissioner": await self.commissioner.to_pydantic(),
            "phones": [await phone.to_pydantic() for phone in self.phones],
            "urls": [await url.to_pydantic() for url in self.urls],
        }
