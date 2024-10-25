import pytest
from fastapi import status

from tests.fixtures import *
from user.enums import UserRoles


@pytest.mark.asyncio
async def test_list_users(async_client, test_user, test_current_user, test_users_list):
    test_user['role'] = UserRoles.admin
    response = await async_client.get("/users/")

    result_users_ids = [user['_id'] for user in response.json()]
    test_users_ids = [str(user['_id']) for user in test_users_list]

    assert response.status_code == status.HTTP_200_OK
    assert result_users_ids.sort() == test_users_ids.sort()


@pytest.mark.asyncio
async def test_show_user_successful(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    user_id = str(test_user['_id'])
    response = await async_client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id'] == str(test_user['_id'])


@pytest.mark.asyncio
async def test_show_user_invalid_data(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    user_id = str(ObjectId())
    response = await async_client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_user_successful(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    response = await async_client.post(f"/users/", json=UserData)
    result_post = response.json()

    assert response.status_code == status.HTTP_200_OK
    for key in UserData:
        if key != 'password':
            assert result_post[key] == UserData[key]


@pytest.mark.asyncio
async def test_create_user_unauthorized(async_client):
    response = await async_client.post(f"/users/", json=UserData)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_user_missing_data(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    invalid_user_data = {"email": "user@example.com"}
    response = await async_client.post(f"/users/", json=invalid_user_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_user_invalid_data(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    UserData['last_name'] = "string" * 10
    response = await async_client.post(f"/users/", json=UserData)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_user_admin_required(async_client, test_current_user):
    response = await async_client.post(f"/users/", json=UserData)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_edit_user_successful(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    response = await async_client.patch(f"/users/{test_user['_id']}", json=UpdatedUserData)
    result_user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_user['first_name'] == UpdatedUserData['first_name']
    assert result_user['last_name'] == UpdatedUserData['last_name']


@pytest.mark.asyncio
async def test_edit_user_unauthorized(async_client, test_user):
    response = await async_client.patch(f"/users/{test_user['_id']}", json=UpdatedUserData)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_edit_user_invalid_post_id(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    response = await async_client.patch(f"/users/{str(ObjectId())}", json=UpdatedUserData)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_edit_user_blank_data(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    response = await async_client.patch(f"/users/{test_user['_id']}", json={})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_edit_user_missing_data(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    UpdatedUserData['last_name'] = "string" * 10
    response = await async_client.patch(f"/users/{test_user['_id']}", json=UpdatedUserData)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_edit_user_admin_required(async_client, test_user, test_current_user):
    response = await async_client.patch(f"/users/{test_user['_id']}", json=UpdatedUserData)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_destroy_user_successful(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    response = await async_client.delete(f"/users/{test_user['_id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['detail'] == 'User deleted successfully'


@pytest.mark.asyncio
async def test_destroy_user_unauthorized(async_client, test_user):
    response = await async_client.delete(f"/users/{test_user['_id']}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_delete_user_invalid_user_id(async_client, test_user, test_current_user):
    test_user['role'] = UserRoles.admin
    response = await async_client.delete(f"/users/{str(ObjectId())}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_user_admin_required(async_client, test_user, test_current_user):
    response = await async_client.delete(f"/users/{test_user['_id']}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
