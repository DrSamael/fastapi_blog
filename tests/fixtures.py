import pytest_asyncio
from bson import ObjectId
from faker import Faker
from httpx import AsyncClient, ASGITransport

from main import app
from database import user_collection
from database import post_collection
from auth.deps import get_current_user

faker = Faker()


@pytest_asyncio.fixture(scope='function')
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope='function')
async def override_get_current_user(test_user):
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
        "user_id": test_user['_id']
    }
    await post_collection.insert_one(post_data)
    yield post_data


@pytest_asyncio.fixture(scope='function')
async def test_post2():
    post_data = {
        "_id": ObjectId(),
        "title": "Fixture Test Post",
        "content": "Content of the fixture post.",
        "user_id": ObjectId()
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
            "user_id": test_user['_id']
        }
        posts_data.append(post_data)

    await post_collection.insert_many(posts_data)
    yield posts_data
