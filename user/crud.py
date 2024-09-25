from bson import ObjectId
from database import user_collection
from .models import User


async def add_user(data: dict):
    user = await user_collection.insert_one(data)
    new_user = await retrieve_user(user.inserted_id)
    return new_user

async def retrieve_user(id: str):
    return await user_collection.find_one({"_id": ObjectId(id)})

async def retrieve_users():
    users = []
    cursor = user_collection.find({})
    async for user in cursor:
        users.append(User(**user))
    return users

async def update_user(id: str, data: dict):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_user:
            return await retrieve_user(id)
    return None

async def delete_user(id: str):
    return await user_collection.delete_one({"_id": ObjectId(id)})
