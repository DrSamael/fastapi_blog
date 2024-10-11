import pytest
from fastapi import status
from httpx import AsyncClient, ASGITransport

from main import app
from .fixtures import *


@pytest.mark.positive
@pytest.mark.asyncio
async def test_list_posts(test_posts_list):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        response = await async_client.get("/posts/")
        result_posts_ids = [post['_id'] for post in response.json()]
        test_posts_ids2 = [str(post['_id']) for post in test_posts_list]

        assert response.status_code == status.HTTP_200_OK
        assert result_posts_ids.sort() == test_posts_ids2.sort()


@pytest.mark.positive
@pytest.mark.asyncio
async def test_show_post_successful(test_post):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_id = str(test_post['_id'])
        response = await async_client.get(f"/posts/{post_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['_id'] == str(test_post['_id'])


@pytest.mark.negative
@pytest.mark.asyncio
async def test_show_post_unsuccessful():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_id = str(ObjectId())
        response = await async_client.get(f"/posts/{post_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
