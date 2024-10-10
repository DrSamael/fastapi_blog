from bson import ObjectId

from database import post_collection
from .schemas import Post


async def retrieve_post(post_id: str):
    return await post_collection.find_one({"_id": ObjectId(post_id)})


async def retrieve_posts():
    posts = []
    cursor = post_collection.find({})
    async for post in cursor:
        posts.append(Post(**post))
    return posts


async def add_post(post_data: dict, user_id: str):
    post_data['user_id'] = user_id
    post = await post_collection.insert_one(post_data)
    new_post = await retrieve_post(post.inserted_id)
    return new_post


async def delete_post(post_id: str):
    return await post_collection.delete_one({"_id": ObjectId(post_id)})


async def update_post(post_id: str, data: dict):
    if len(data) < 1:
        return False
    post = await post_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        updated_post = await post_collection.update_one({"_id": ObjectId(post_id)}, {"$set": data})
        if updated_post:
            return await retrieve_post(post_id)
    return None
