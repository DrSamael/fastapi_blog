from bson import ObjectId
from typing import Optional

from src.database import post_collection
from .schemas import Post


async def retrieve_post(post_id: str):
    return await post_collection.find_one({"_id": ObjectId(post_id)})


async def retrieve_posts(filter_criteria=None):
    posts = []
    cursor = post_collection.find(filter_criteria)
    async for post in cursor:
        posts.append(Post(**post))
    return posts


async def retrieve_current_user_posts(user_id: Optional[str]):
    filter_criteria = {"user_id": ObjectId(user_id)} if user_id else {}
    return await retrieve_posts(filter_criteria)


async def retrieve_published_posts():
    filter_criteria = {"published": True}
    return await retrieve_posts(filter_criteria)


async def add_post(post_data: dict, user_id: str):
    post_data['user_id'] = user_id
    post = await post_collection.insert_one(post_data)
    new_post = await retrieve_post(post.inserted_id)
    return new_post


async def delete_post(post_id: str):
    return await post_collection.delete_one({"_id": ObjectId(post_id)})


async def update_post(post_id: str, data: dict):
    if len(data) < 1:
        return None
    post = await post_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        updated_post = await post_collection.update_one({"_id": ObjectId(post_id)}, {"$set": data})
        if updated_post:
            return await retrieve_post(post_id)
    return None
