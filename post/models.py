from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object ID")
        return ObjectId(v)

# Schema for the Post collection
class Post(BaseModel):
    id: ObjectId = Field( alias="_id")
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

# For POST/PUT requests: Input validation model (without 'id')
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
