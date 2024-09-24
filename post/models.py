from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator


PyObjectId = Annotated[str, BeforeValidator(str)]


class Post(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "A Sample Post",
                "content": "This is the content of the post."
            }
        }


class PostCreate(BaseModel):
    title: str
    content: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My First Post",
                "content": "Content of the post goes here."
            }
        }
