from bson import ObjectId

from src.database import user_collection
from .schemas import User

from src.auth.utils import get_hashed_password


async def add_user(data: dict):
    data['password'] = await get_hashed_password(data['password'])
    user = await user_collection.insert_one(data)
    new_user = await retrieve_user(user.inserted_id)
    return new_user


async def retrieve_user(user_id: str):
    return await user_collection.find_one({"_id": ObjectId(user_id)})


async def retrieve_user_by_email(email: str):
    return await user_collection.find_one({"email": email})


async def retrieve_users():
    users = []
    cursor = user_collection.find({})
    async for user in cursor:
        users.append(User(**user))
    return users


async def update_user(user_id: str, data: dict):
    if len(data) < 1:
        return None
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        updated_user = await user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
        if updated_user:
            return await retrieve_user(user_id)
    return None


async def delete_user(user_id: str):
    return await user_collection.delete_one({"_id": ObjectId(user_id)})
