import pytest
from fastapi import status

from tests.fixtures import *
from user.enums import UserRoles


@pytest.mark.asyncio
async def test_list_posts(async_client, test_posts_list):
    response = await async_client.get("/posts/")
    result_posts_ids = [post['_id'] for post in response.json()]
    test_posts_ids = [str(post['_id']) for post in test_posts_list]

    assert response.status_code == status.HTTP_200_OK
    assert result_posts_ids.sort() == test_posts_ids.sort()


@pytest.mark.asyncio
async def test_current_user_posts_successful(async_client, test_posts_list, test_current_user):
    response = await async_client.get("/posts/user-posts")
    result_posts_ids = [post['_id'] for post in response.json()]
    test_posts_ids = [str(post['_id']) for post in test_posts_list]

    assert response.status_code == status.HTTP_200_OK
    assert result_posts_ids.sort() == test_posts_ids.sort()


@pytest.mark.asyncio
async def test_current_user_posts_unauthorized(async_client):
    response = await async_client.get("/posts/user-posts")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_show_post_successful(async_client, test_post):
    post_id = str(test_post['_id'])
    response = await async_client.get(f"/posts/{post_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id'] == str(test_post['_id'])


@pytest.mark.asyncio
async def test_show_post_invalid_data(async_client):
    post_id = str(ObjectId())
    response = await async_client.get(f"/posts/{post_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_post_successful(async_client, test_current_user):
    post_data = {"title": "Test title", "content": "Test content"}
    response = await async_client.post(f"/posts/", json=post_data)
    result_post = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_post['title'] == post_data['title']


@pytest.mark.asyncio
async def test_create_post_unauthorized(async_client):
    post_data = {"title": "Test title", "content": "Test content"}
    response = await async_client.post(f"/posts/", json=post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_post_missing_data(async_client, test_current_user):
    post_data = {"title": "Test title"}
    response = await async_client.post(f"/posts/", json=post_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_post_invalid_data(async_client, test_current_user):
    post_data = {"title": "Test title", "content": "too long text" * 1000}
    response = await async_client.post(f"/posts/", json=post_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_post_author_required(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.user
    post_data = {"title": "Test title", "content": "Test content"}
    response = await async_client.post(f"/posts/", json=post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_edit_post_successful(async_client, test_current_user, test_post):
    post_data = {"title": "Updated title", "content": "Updated content"}
    response = await async_client.patch(f"/posts/{test_post['_id']}", json=post_data)
    result_post = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_post['title'] == post_data['title']
    assert result_post['content'] == post_data['content']


@pytest.mark.asyncio
async def test_edit_post_unauthorized(async_client, test_post):
    post_data = {"title": "Updated title", "content": "Updated content"}
    response = await async_client.patch(f"/posts/{test_post['_id']}", json=post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_edit_post_invalid_post_id(async_client, test_current_user):
    post_data = {"title": "Updated title", "content": "Updated content"}
    response = await async_client.patch(f"/posts/{str(ObjectId())}", json=post_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_edit_post_blank_data(async_client, test_post, test_current_user):
    response = await async_client.patch(f"/posts/{test_post['_id']}", json={})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_edit_post_invalid_data(async_client, test_current_user):
    post_data = {"title": "Test title", "content": "too long text" * 1000}
    response = await async_client.patch(f"/posts/{str(ObjectId())}", json=post_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_edit_post_author_required(async_client, test_user, test_current_user, test_post):
    test_user['role'] = UserRoles.user
    post_data = {"title": "Updated title", "content": "Updated content"}
    response = await async_client.patch(f"/posts/{test_post['_id']}", json=post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_edit_post_wrong_owner(async_client, test_current_user, test_post2):
    post_data = {"title": "Updated title", "content": "Updated content"}
    response = await async_client.patch(f"/posts/{test_post2['_id']}", json=post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_destroy_post_successful(async_client, test_current_user, test_post):
    response = await async_client.delete(f"/posts/{test_post['_id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['detail'] == 'Post deleted successfully'


@pytest.mark.asyncio
async def test_destroy_post_successful_with_admin_role(async_client, test_user, test_current_user, test_post):
    test_user['role'] = UserRoles.admin
    response = await async_client.delete(f"/posts/{test_post['_id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['detail'] == 'Post deleted successfully'


@pytest.mark.asyncio
async def test_destroy_post_unauthorized(async_client, test_post):
    response = await async_client.delete(f"/posts/{test_post['_id']}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_delete_post_invalid_post_id(async_client, test_current_user):
    response = await async_client.delete(f"/posts/{str(ObjectId())}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_post_author_required(async_client, test_user, test_current_user, test_post):
    test_user['role'] = UserRoles.user
    response = await async_client.delete(f"/posts/{test_post['_id']}")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_delete_post_wrong_owner(async_client, test_current_user, test_post2):
    response = await async_client.delete(f"/posts/{test_post2['_id']}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
