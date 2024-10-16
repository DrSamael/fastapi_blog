import pytest
from fastapi import status
from httpx import AsyncClient, ASGITransport

from auth.deps import get_current_user
from main import app
from tests.fixtures import *


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
async def test_show_post_invalid_data():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_id = str(ObjectId())
        response = await async_client.get(f"/posts/{post_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.positive
@pytest.mark.asyncio
async def test_create_post_successful(test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_data = {"title": "Test title", "content": "Test content"}
        response = await async_client.post(f"/posts/", json=post_data)
        result_post = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result_post['title'] == post_data['title']

    app.dependency_overrides.clear()


@pytest.mark.negative
@pytest.mark.asyncio
async def test_create_post_unauthorized():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_data = {"title": "Test title", "content": "Test content"}
        response = await async_client.post(f"/posts/", json=post_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.negative
@pytest.mark.asyncio
async def test_create_post_invalid_data(test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_data = {"title": "Test title"}
        response = await async_client.post(f"/posts/", json=post_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    app.dependency_overrides.clear()


@pytest.mark.negative
@pytest.mark.asyncio
async def test_create_post_author_required(test_user):
    test_user['role'] = 'user'
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_data = {"title": "Test title", "content": "Test content"}
        response = await async_client.post(f"/posts/", json=post_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    app.dependency_overrides.clear()


@pytest.mark.positive
@pytest.mark.asyncio
async def test_edit_post_successful(test_user, test_post):
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_data = {"title": "Updated title", "content": "Updated content"}
        response = await async_client.patch(f"/posts/{test_post['_id']}", json=post_data)
        result_post = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result_post['title'] == post_data['title']
        assert result_post['content'] == post_data['content']

    app.dependency_overrides.clear()


@pytest.mark.negative
@pytest.mark.asyncio
async def test_edit_post_unauthorized(test_post):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_data = {"title": "Updated title", "content": "Updated content"}
        response = await async_client.patch(f"/posts/{test_post['_id']}", json=post_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.negative
@pytest.mark.asyncio
async def test_edit_post_invalid_post_id(test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_data = {"title": "Updated title", "content": "Updated content"}
        response = await async_client.patch(f"/posts/{str(ObjectId())}", json=post_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    app.dependency_overrides.clear()


@pytest.mark.negative
@pytest.mark.asyncio
async def test_edit_post_invalid_data(test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        response = await async_client.patch(f"/posts/{str(ObjectId())}", json={})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    app.dependency_overrides.clear()


@pytest.mark.negative
@pytest.mark.asyncio
async def test_edit_post_author_required(test_user, test_post):
    test_user['role'] = 'user'
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_data = {"title": "Updated title", "content": "Updated content"}
        response = await async_client.patch(f"/posts/{test_post['_id']}", json=post_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    app.dependency_overrides.clear()


@pytest.mark.negative
@pytest.mark.asyncio
async def test_edit_post_wrong_owner(test_user, test_post2):
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        post_data = {"title": "Updated title", "content": "Updated content"}
        response = await async_client.patch(f"/posts/{test_post2['_id']}", json=post_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    app.dependency_overrides.clear()


@pytest.mark.positive
@pytest.mark.asyncio
async def test_destroy_post_successful(test_user, test_post):
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        response = await async_client.delete(f"/posts/{test_post['_id']}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['detail'] == 'Post deleted successfully'

    app.dependency_overrides.clear()


@pytest.mark.negative
@pytest.mark.asyncio
async def test_destroy_post_unauthorized(test_post):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        response = await async_client.delete(f"/posts/{test_post['_id']}")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.negative
@pytest.mark.asyncio
async def test_delete_post_invalid_post_id(test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        response = await async_client.delete(f"/posts/{str(ObjectId())}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    app.dependency_overrides.clear()


@pytest.mark.negative
@pytest.mark.asyncio
async def test_delete_post_author_required(test_user, test_post):
    test_user['role'] = 'user'
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        response = await async_client.delete(f"/posts/{test_post['_id']}")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    app.dependency_overrides.clear()


@pytest.mark.negative
@pytest.mark.asyncio
async def test_delete_post_wrong_owner(test_user, test_post2):
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        response = await async_client.delete(f"/posts/{test_post2['_id']}")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    app.dependency_overrides.clear()
