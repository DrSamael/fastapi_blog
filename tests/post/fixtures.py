import pytest_asyncio
from bson import ObjectId
from faker import Faker

from database import user_collection
from database import post_collection

faker = Faker()


@pytest_asyncio.fixture
def current_user():
    return {
        "_id": ObjectId(),
        "email": "current_user@example.com",
        "role": "author"
    }


@pytest_asyncio.fixture(scope='function')
async def test_user():
    user = {
        "_id": ObjectId(),
        "email": "fixtureuser-user@example.com",
        "password": "123123",
        "first_name": "Fixture",
        "last_name": "User",
        "role": "author"
    }
    await user_collection.insert_one(user)
    yield user


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
