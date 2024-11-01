from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Literal
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]
Genres = List[Literal['social', 'culture', 'sport', 'fiction', 'medicine']]


class AuthorBase(BaseModel):
    company: str = Field(max_length=100, min_length=5)
    biography: str = Field(max_length=5000, min_length=10)
    genre: Genres = Field(default_factory=list)


class AuthorCreate(AuthorBase):
    user_id: PyObjectId


class AuthorUpdate(AuthorBase):
    company: Optional[str] = Field(None, max_length=300, min_length=5)
    biography: Optional[str] = Field(None, max_length=5000, min_length=10)
    genre: Optional[Genres] = None
    user_id: Optional[PyObjectId] = None


class Author(AuthorBase):
    model_config = ConfigDict(populate_by_name=True, json_encoders={ObjectId: str})

    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: Optional[PyObjectId] = None
