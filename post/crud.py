from bson import ObjectId
from database import post_collection
from .models import Post, PostCreate


async def retrieve_post(id: str):
    return await post_collection.find_one({"_id": ObjectId(id)})

async def retrieve_posts():
    posts = []
    cursor = post_collection.find({})
    async for post in cursor:
        posts.append(Post(**post))
    return posts

async def add_post(post_data: dict):
    post = await post_collection.insert_one(post_data)
    new_post = await retrieve_post(post.inserted_id)
    return new_post

async def delete_post(id: str):
    return await post_collection.delete_one({"_id": ObjectId(id)})

async def update_post(id: str, data: dict):
    if len(data) < 1:
        return False
    post = await post_collection.find_one({"_id": ObjectId(id)})
    if post:
        updated_post = await post_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_post:
            return await retrieve_post(id)
    return None
