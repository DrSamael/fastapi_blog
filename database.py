from motor.motor_asyncio import AsyncIOMotorClient
import os

DATABASE_NAME = "fastapi_test_db" if os.getenv("TESTING") == "true" else "fastapi_db"

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client[DATABASE_NAME]
post_collection = db.posts
user_collection = db.users
author_collection = db.authors
