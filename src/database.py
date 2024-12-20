from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
import os

DATABASE_NAME = "fastapi_test_db" if os.getenv("TESTING") == "true" else os.getenv("DATABASE_NAME")
DATABASE_URI = os.getenv("DATABASE_URI", "mongodb://mongo:27017")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/")

redis = Redis.from_url(REDIS_URL, decode_responses=True)
client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
post_collection = db.posts
user_collection = db.users
author_collection = db.authors
