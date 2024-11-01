import os
import pytest_asyncio
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


def pytest_configure():
    os.environ['TESTING'] = 'true'


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an event loop for the session scope."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def cleanup_test_database():
    yield

    if os.getenv("TESTING") == "true":
        mongo_uri = os.getenv("DATABASE_URI", "mongodb://localhost:27017")
        client = AsyncIOMotorClient(mongo_uri)
        test_db_name = "fastapi_test_db"

        await client.drop_database(test_db_name)
        print(f"Test database '{test_db_name}' dropped successfully.")
