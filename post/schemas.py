from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class PostBase(BaseModel):
    title: str = Field(max_length=200, min_length=5)
    content: str = Field(max_length=10000, min_length=10)
    published: bool = Field(default=False)


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: Optional[str] = Field(None, max_length=300, min_length=5)
    content: Optional[str] = Field(None, max_length=10000, min_length=10)
    published: Optional[bool] = None


class Post(PostBase):
    model_config = ConfigDict(populate_by_name=True, json_encoders={ObjectId: str}, json_schema_extra={
        "example": {"title": "A Sample Post",
                    "content": "This is the content of the post."}
    })

    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: Optional[PyObjectId] = None
