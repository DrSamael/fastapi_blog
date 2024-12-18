from motor.motor_asyncio import AsyncIOMotorClient
import os

DATABASE_NAME = "fastapi_test_db" if os.getenv("TESTING") == "true" else os.getenv("DATABASE_NAME")
DATABASE_URI = os.getenv("DATABASE_URI", "mongodb://mongo:27017")

client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
post_collection = db.posts
user_collection = db.users
author_collection = db.authors
