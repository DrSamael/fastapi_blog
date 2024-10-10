import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from database import user_collection
from database import post_collection
from main import app


@pytest_asyncio.fixture(scope='function')
async def test_user():
    user = {
        "_id": "test_user_id",
        "email": "fixtureuser-user@example.com",
        "password": "123123",
        "first_name": "Fixture",
        "last_name": "User",
        "role": "user"
    }
    await user_collection.insert_one(user)
    yield user


@pytest_asyncio.fixture(scope='function')
async def test_post(test_user):
    post_data = {
        "_id": "test_post_id",
        "title": "Fixture Test Post",
        "content": "Content of the fixture post.",
        "user_id": test_user['_id']
    }
    await post_collection.insert_one(post_data)
    yield post_data


@pytest.mark.positive
@pytest.mark.asyncio
async def test_list_posts(test_user, test_post):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        response = await async_client.get("/posts/")
        posts_list = response.json()

        # import pdb
        # pdb.set_trace()

        assert response.status_code == 200
        # assert len(posts_list) == len(test_post)
