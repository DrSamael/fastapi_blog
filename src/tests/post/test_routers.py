from fastapi import status
import json

from src.tests.fixtures import *
from src.database import redis


async def test_list_posts(async_client, test_posts_list):
    response = await async_client.get("/posts/")
    result_posts_ids = [post['_id'] for post in response.json()]
    test_posts_ids = [str(post['_id']) for post in test_posts_list]

    assert response.status_code == status.HTTP_200_OK
    assert result_posts_ids == test_posts_ids


async def test_current_user_posts_successful(async_client, test_posts_list, test_post2, test_current_user_simple):
    response = await async_client.get("/posts/user-posts")
    result_posts_ids = [post['_id'] for post in response.json()]
    test_posts_ids = [str(post['_id']) for post in test_posts_list]

    assert response.status_code == status.HTTP_200_OK
    assert result_posts_ids == test_posts_ids
    assert str(test_post2['_id']) not in result_posts_ids


async def test_current_user_posts_unauthorized(async_client):
    response = await async_client.get("/posts/user-posts")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_published_posts_successful(async_client, test_posts_list, test_post, test_current_user_author):
    await redis.delete("posts")
    response = await async_client.get("/posts/published")
    result_posts_ids = [post['_id'] for post in response.json()]
    test_posts_ids = [str(post['_id']) for post in test_posts_list]

    assert response.status_code == status.HTTP_200_OK
    assert result_posts_ids == test_posts_ids
    assert str(test_post['_id']) not in result_posts_ids


async def test_published_cached_posts_successful(async_client, test_posts_list, test_post, test_current_user_author):
    await redis.delete("posts")
    serialized_posts = [
        {**post, "_id": str(post["_id"]), "user_id": str(post["user_id"])}
        for post in test_posts_list
    ]
    await redis.set("posts", json.dumps(serialized_posts))

    response = await async_client.get("/posts/published")
    result_posts_ids = [post['_id'] for post in response.json()]
    test_posts_ids = [str(post['_id']) for post in test_posts_list]
    await redis.delete("posts")

    assert response.status_code == status.HTTP_200_OK
    assert result_posts_ids == test_posts_ids
    assert str(test_post['_id']) not in result_posts_ids


async def test_show_post_successful(async_client, test_post):
    post_id = str(test_post['_id'])
    response = await async_client.get(f"/posts/{post_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id'] == str(test_post['_id'])


async def test_show_post_invalid_data(async_client):
    post_id = str(ObjectId())
    response = await async_client.get(f"/posts/{post_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_create_post_successful(async_client, test_current_user_author):
    post_data = {"title": "Test title", "content": "Test content"}
    response = await async_client.post(f"/posts/", json=post_data)
    result_post = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_post['title'] == post_data['title']


async def test_create_post_unauthorized(async_client):
    post_data = {"title": "Test title", "content": "Test content"}
    response = await async_client.post(f"/posts/", json=post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_post_missing_data(async_client, test_current_user_author):
    post_data = {"title": "Test title"}
    response = await async_client.post(f"/posts/", json=post_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_create_post_invalid_data(async_client, test_current_user_author):
    post_data = {"title": "Test title", "content": "too long text" * 1000}
    response = await async_client.post(f"/posts/", json=post_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_create_post_author_required(async_client, test_current_user_simple):
    post_data = {"title": "Test title", "content": "Test content"}
    response = await async_client.post(f"/posts/", json=post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_edit_post_successful(async_client, test_post, test_current_user_author):
    post_data = {"title": "Updated title", "content": "Updated content"}
    response = await async_client.patch(f"/posts/{test_post['_id']}", json=post_data)
    result_post = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_post['title'] == post_data['title']
    assert result_post['content'] == post_data['content']


async def test_edit_post_unauthorized(async_client, test_post):
    post_data = {"title": "Updated title", "content": "Updated content"}
    response = await async_client.patch(f"/posts/{test_post['_id']}", json=post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_edit_post_invalid_post_id(async_client, test_current_user_author):
    post_data = {"title": "Updated title", "content": "Updated content"}
    response = await async_client.patch(f"/posts/{str(ObjectId())}", json=post_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_edit_post_blank_data(async_client, test_post, test_current_user_author):
    response = await async_client.patch(f"/posts/{test_post['_id']}", json={})

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_edit_post_invalid_data(async_client, test_post, test_current_user_author):
    post_data = {"title": "Test title", "content": "too long text" * 1000}
    response = await async_client.patch(f"/posts/{test_post['_id']}", json=post_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_edit_post_author_required(async_client, test_post, test_current_user_simple):
    post_data = {"title": "Updated title", "content": "Updated content"}
    response = await async_client.patch(f"/posts/{test_post['_id']}", json=post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_edit_post_wrong_owner(async_client, test_post2, test_current_user_author):
    post_data = {"title": "Updated title", "content": "Updated content"}
    response = await async_client.patch(f"/posts/{test_post2['_id']}", json=post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_destroy_post_successful(async_client, test_post, test_current_user_author):
    response = await async_client.delete(f"/posts/{test_post['_id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['detail'] == 'Post deleted successfully'


async def test_destroy_post_successful_with_admin_role(async_client, test_post, test_current_user_admin):
    response = await async_client.delete(f"/posts/{test_post['_id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['detail'] == 'Post deleted successfully'


async def test_destroy_post_unauthorized(async_client, test_post):
    response = await async_client.delete(f"/posts/{test_post['_id']}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_post_invalid_post_id(async_client, test_current_user_author):
    response = await async_client.delete(f"/posts/{str(ObjectId())}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_post_author_required(async_client, test_post, test_current_user_simple):
    response = await async_client.delete(f"/posts/{test_post['_id']}")

    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_delete_post_wrong_owner(async_client, test_post2, test_current_user_author):
    response = await async_client.delete(f"/posts/{test_post2['_id']}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
