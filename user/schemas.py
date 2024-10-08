from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

from .enums import UserRoles


PyObjectId = Annotated[str, BeforeValidator(str)]


class UserConfig:
    populate_by_name = True
    json_encoders = {ObjectId: str}


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRoles


class User(UserBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    password: str

    class Config(UserConfig):
        pass


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRoles] = None


class UserOut(UserBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')

    class Config(UserConfig):
        pass


class UserTokens(BaseModel):
    access_token: str
    refresh_token: str
