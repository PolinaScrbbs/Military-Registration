from pydantic import BaseModel


class ID(BaseModel):
    id: int


class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str
    full_name: str


class BaseUser(ID):
    username: str
    role: str
    full_name: str


class UserResponse(BaseModel):
    message: str
    user: BaseUser