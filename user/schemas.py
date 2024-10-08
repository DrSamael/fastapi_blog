from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator


RoleType = Literal['user', 'author', 'admin']
PyObjectId = Annotated[str, BeforeValidator(str)]


class UserConfig:
    populate_by_name = True
    json_encoders = {ObjectId: str}


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: RoleType


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
    role: Optional[RoleType] = None


class UserOut(UserBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')

    class Config(UserConfig):
        pass


class UserTokens(BaseModel):
    access_token: str
    refresh_token: str
