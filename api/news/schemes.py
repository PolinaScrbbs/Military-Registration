from typing import Optional, List

from ..user.schemes import ID, BaseModel, BaseUser


class NewNews(BaseModel):
    title: str
    content: str


class NewsResponse(NewNews, ID):
    creator: BaseUser
    created_at: str
    last_updated: Optional[str]
