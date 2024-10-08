from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator


RoleType = Literal['user', 'author', 'admin']
PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: RoleType = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: RoleType


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[RoleType] = None


class UserOut(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    email: EmailStr
    first_name: str
    last_name: str
    role: Optional[RoleType] = None

    class Config:
        populate_by_name = True


class UserTokens(BaseModel):
    access_token: str
    refresh_token: str
