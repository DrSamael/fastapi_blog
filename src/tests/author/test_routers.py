import pytest
from fastapi import status

from src.tests.fixtures import *
from src.user.enums import UserRoles


@pytest.mark.asyncio
async def test_list_authors(async_client, test_user, test_authors_list, test_current_user):
    test_user['role'] = UserRoles.admin
    response = await async_client.get("/authors/")
    result_authors_ids = [author['_id'] for author in response.json()]
    test_authors_ids = [str(author['_id']) for author in test_authors_list]

    assert response.status_code == status.HTTP_200_OK
    assert result_authors_ids == test_authors_ids


@pytest.mark.asyncio
async def test_current_user_author_successful(async_client, test_users_author, test_author, test_current_user):
    response = await async_client.get("/authors/user-author")
    result_authors_ids = [author['_id'] for author in response.json()]

    assert response.status_code == status.HTTP_200_OK
    assert str(test_users_author['_id']) in result_authors_ids
    assert str(test_author['_id']) not in result_authors_ids


@pytest.mark.asyncio
async def test_current_user_author_unauthorized(async_client):
    response = await async_client.get("/authors/user-author")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_show_author_successful(async_client, test_user, test_author, test_current_user):
    test_user['role'] = UserRoles.admin
    author_id = str(test_author['_id'])
    response = await async_client.get(f"/authors/{author_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id'] == str(test_author['_id'])


@pytest.mark.asyncio
async def test_show_author_invalid_data(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    author_id = str(ObjectId())
    response = await async_client.get(f"/authors/{author_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_show_author_admin_required(async_client, test_current_user):
    author_id = str(ObjectId())
    response = await async_client.get(f"/authors/{author_id}")

    assert response.status_code == status.HTTP_403_FORBIDDEN


# @pytest.mark.asyncio
# async def test_create_author_successful(async_client, test_current_user):
#     response = await async_client.post(f"/authors/", json=AuthorData)
#     result_author = response.json()
#
#     assert response.status_code == status.HTTP_200_OK
#     assert result_post['title'] == post_data['title']


# @pytest.mark.asyncio
# async def test_create_post_unauthorized(async_client):
#     post_data = {"title": "Test title", "content": "Test content"}
#     response = await async_client.post(f"/posts/", json=post_data)
#
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#
# @pytest.mark.asyncio
# async def test_create_post_missing_data(async_client, test_current_user):
#     post_data = {"title": "Test title"}
#     response = await async_client.post(f"/posts/", json=post_data)
#
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#
#
# @pytest.mark.asyncio
# async def test_create_post_invalid_data(async_client, test_current_user):
#     post_data = {"title": "Test title", "content": "too long text" * 1000}
#     response = await async_client.post(f"/posts/", json=post_data)
#
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#
#
# @pytest.mark.asyncio
# async def test_create_post_author_required(async_client, test_user, test_current_user):
#     test_user['role'] = UserRoles.user
#     post_data = {"title": "Test title", "content": "Test content"}
#     response = await async_client.post(f"/posts/", json=post_data)
#
#     assert response.status_code == status.HTTP_403_FORBIDDEN