from typing import Optional, List
from fastapi import UploadFile, Form

from ..user.schemes import BaseModel, ID, BaseUser
from .models import ContentCategory


class NewContent(BaseModel):
    filename: str = (Form(...),)
    category: ContentCategory = (Form(...),)
    file: UploadFile = (Form(...),)


class ContentResponse(ID):
    filename: str
    extension: str
    path: str
    category: str
    creator: BaseUser
    is_archived: bool
    created_at: str
    last_updated_at: Optional[str]


class GetContentFilters(BaseModel):
    category: Optional[ContentCategory] = None
    creator: Optional[str] = None
    archived: bool = False


class ContentUpdateRequest(BaseModel):
    filename: Optional[str] = None
    category: Optional[ContentCategory] = None
    is_archived: Optional[bool] = None
