import pytest_asyncio
from bson import ObjectId
from faker import Faker
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.database import user_collection
from src.database import post_collection
from src.auth.deps import get_current_user
from src.auth.utils import get_hashed_password
from src.database import db

faker = Faker()

UserData = {"email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "role": "user",
            "password": "string"}

UpdatedUserData = {"first_name": "Updated first_name",
                   "last_name": "Updated last_name"}


@pytest_asyncio.fixture(scope='function', autouse=True)
async def clear_test_db():
    for collection_name in await db.list_collection_names():
        await db[collection_name].delete_many({})


@pytest_asyncio.fixture(scope='function')
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope='function')
async def test_current_user(test_user, request):
    app.dependency_overrides[get_current_user] = lambda: test_user
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope='function')
async def test_user():
    user = {
        "_id": ObjectId(),
        "email": "fixture-user@example.com",
        "password": "123123",
        "first_name": "Fixture",
        "last_name": "User",
        "role": "author"
    }
    await user_collection.insert_one(user)
    yield user


@pytest_asyncio.fixture(scope='function')
async def test_user_with_encrypted_password(test_user):
    test_user['password'] = await get_hashed_password("123123")
    data = {"password": test_user['password']}

    await user_collection.update_one({"_id": test_user["_id"]}, {"$set": data})
    yield test_user


@pytest_asyncio.fixture(scope='function')
async def test_users_list():
    users_data = []

    for _ in range(3):
        user_data = {
            "_id": ObjectId(),
            "email": "fixture-user@example.com",
            "password": "123123",
            "first_name": "Fixture",
            "last_name": "User",
            "role": "user"
        }
        users_data.append(user_data)

    await user_collection.insert_many(users_data)
    yield users_data


@pytest_asyncio.fixture(scope='function')
async def test_post(test_user):
    post_data = {
        "_id": ObjectId(),
        "title": "Fixture Test Post",
        "content": "Content of the fixture post.",
        "user_id": test_user['_id'],
        "published": False
    }
    await post_collection.insert_one(post_data)
    yield post_data


@pytest_asyncio.fixture(scope='function')
async def test_post2():
    post_data = {
        "_id": ObjectId(),
        "title": "Fixture Test Post",
        "content": "Content of the fixture post.",
        "user_id": ObjectId(),
        "published": False
    }
    await post_collection.insert_one(post_data)
    yield post_data


@pytest_asyncio.fixture(scope='function')
async def test_posts_list(test_user):
    posts_data = []

    for _ in range(3):
        post_data = {
            "_id": ObjectId(),
            "title": faker.sentence(nb_words=5),
            "content": faker.text(max_nb_chars=50),
            "user_id": test_user['_id'],
            "published": True
        }
        posts_data.append(post_data)

    await post_collection.insert_many(posts_data)
    yield posts_data
