from typing import List, Optional

from ..user.models import BaseEnum
from ..user.schemes import BaseModel, ID


class NewCommissariat(BaseModel):
    name: str
    address: str
    commissioner_id: int


class Commissioner(ID):
    name: str
    surname: str
    patronymic: str


class CommissariatUrlType(BaseEnum):
    MAIN = "main"
    VK = "vk"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"
    VIBER = "viber"
    TIKTOK = "tiktok"


class CommissionerUrl(ID):
    url: str
    type: CommissariatUrlType


class CommissariatPhoneType(BaseEnum):
    DUTY = "duty"
    MC = "mc"


class CommissionerPhone(ID):
    phone: str
    type: CommissariatPhoneType


class CommissariatResponse(ID):
    name: str
    address: str
    commissioner: Optional[Commissioner]
    phones: List[CommissionerPhone]
    urls: List[CommissionerUrl]
