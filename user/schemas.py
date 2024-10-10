from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

from .enums import UserRoles

PyObjectId = Annotated[str, BeforeValidator(str)]
UserConfig = {'populate_by_name': True, 'json_encoders': {ObjectId: str}}


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRoles


class User(UserBase):
    model_config = ConfigDict(**UserConfig)

    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    password: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRoles] = None


class UserOut(UserBase):
    model_config = ConfigDict(**UserConfig)

    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')


class UserTokens(BaseModel):
    access_token: str
    refresh_token: str
