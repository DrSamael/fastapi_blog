from bson import ObjectId
from typing import Optional
import json

from src.database import post_collection, redis
from .schemas import Post
from src.settings.app import AppSettings

CACHE_EXPIRATION_SECONDS = AppSettings().cache_expiration_seconds


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
    cached_posts = await _get_cached_posts()
    if cached_posts:
        return cached_posts

    filter_criteria = {"published": True}
    posts = await retrieve_posts(filter_criteria)
    await _set_cached_posts(posts)
    return posts


async def add_post(post_data: dict, user_id: str):
    post_data['user_id'] = user_id
    post = await post_collection.insert_one(post_data)
    new_post = await retrieve_post(post.inserted_id)
    await _delete_cached_posts()
    return new_post


async def delete_post(post_id: str):
    await _delete_cached_posts()
    return await post_collection.delete_one({"_id": ObjectId(post_id)})


async def update_post(post_id: str, data: dict):
    if len(data) < 1:
        return None
    post = await post_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        updated_post = await post_collection.update_one({"_id": ObjectId(post_id)}, {"$set": data})
        if updated_post:
            await _delete_cached_posts()
            return await retrieve_post(post_id)
    return None


async def _get_cached_posts():
    cached_posts = await redis.get("posts")
    if cached_posts:
        posts = [Post(**post_data) for post_data in json.loads(cached_posts)]
        return posts


async def _set_cached_posts(posts):
    serialized_posts = [post.model_dump() for post in posts]
    await redis.set("posts", json.dumps(serialized_posts), ex=CACHE_EXPIRATION_SECONDS)


async def _delete_cached_posts():
    await redis.delete("posts")
