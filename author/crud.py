from bson import ObjectId
from typing import Optional

from database import author_collection
from .schemas import Author


async def add_autor(data: dict):
    data['user_id'] = ObjectId(data['user_id'])
    autor = await author_collection.insert_one(data)
    new_author = await retrieve_author(autor.inserted_id)
    return new_author


async def retrieve_author(author_id: str):
    return await author_collection.find_one({"_id": ObjectId(author_id)})


async def retrieve_author_by_user_id(user_id: str):
    return await author_collection.find_one({"user_id": ObjectId(user_id)})


async def retrieve_authors(user_id: Optional[str] = None):
    authors = []
    filter_criteria = {"user_id": ObjectId(user_id)} if user_id else {}
    cursor = author_collection.find(filter_criteria)
    async for author in cursor:
        authors.append(Author(**author))
    return authors


async def update_author(author_id: str, data: dict):
    if len(data) < 1:
        return None
    author = await author_collection.find_one({"_id": ObjectId(author_id)})
    if author:
        updated_author = await author_collection.update_one({"_id": ObjectId(author_id)}, {"$set": data})
        if updated_author:
            return await retrieve_author(author_id)
    return None


async def delete_author(author_id: str):
    return await author_collection.delete_one({"_id": ObjectId(author_id)})
