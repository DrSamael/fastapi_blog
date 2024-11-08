from fastapi import status

from src.tests.fixtures import *
from src.auth.utils import create_token


async def test_signup_successful(async_client):
    response = await async_client.post(f"/auth/signup", json=UserData)
    result_user = response.json()

    assert response.status_code == status.HTTP_200_OK
    for key in UserData:
        if key != 'password':
            assert result_user[key] == UserData[key]


async def test_signup_email_already_exists(async_client):
    await async_client.post(f"/auth/signup", json=UserData)
    response = await async_client.post(f"/auth/signup", json=UserData)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'User with this email already exist'


async def test_signup_invalid_data(async_client):
    response = await async_client.post(f"/auth/signup", json=UpdatedUserData)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_me_successful(async_client, test_user, test_current_user_author):
    response = await async_client.get(f"/auth/me")
    result_user = response.json()

    assert response.status_code == status.HTTP_200_OK
    for key in test_user:
        if key != 'password':
            assert result_user[key] == result_user[key]


async def test_get_me_unauthorized(async_client):
    response = await async_client.get(f"/auth/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_login_successful(async_client, test_user_with_encrypted_password):
    login_data = {
        "username": test_user_with_encrypted_password["email"],
        "password": "123123"
    }
    response = await async_client.post("/auth/login", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert "access_token" in result
    assert "refresh_token" in result


async def test_login_invalid_password(async_client, test_user_with_encrypted_password):
    login_data = {
        "username": test_user_with_encrypted_password["email"],
        "password": "wrong_password"
    }
    response = await async_client.post("/auth/login", data=login_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Incorrect email or password"


async def test_login_invalid_email(async_client, test_user_with_encrypted_password):
    login_data = {
        "username": 'wrong_email',
        "password": "123123"
    }
    response = await async_client.post("/auth/login", data=login_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Incorrect email or password"


async def test_login_blank_data(async_client):
    response = await async_client.post("/auth/login", data={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_refresh_token_successful(async_client, test_user):
    refresh_token = await create_token(test_user["_id"], 15, 'refresh_token')
    response = await async_client.get("/auth/refresh-token", headers={"refresh-token": refresh_token})

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert "access_token" in result
    assert "refresh_token" in result


async def test_refresh_token_blank(async_client):
    response = await async_client.get("/auth/refresh-token")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Refresh token missing"


async def test_refresh_token_invalid_user_id(async_client):
    refresh_token = await create_token(ObjectId(), 15, 'refresh_token')
    response = await async_client.get("/auth/refresh-token", headers={"refresh-token": refresh_token})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Could not find user"


async def test_refresh_token_expired(async_client, test_user):
    expired_token = await create_token(test_user["_id"], -15, 'refresh_token')
    response = await async_client.get("/auth/refresh-token", headers={"refresh-token": expired_token})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Token expired"


async def test_refresh_token_invalid(async_client):
    invalid_token = "invalid_refresh_token"
    response = await async_client.get("/auth/refresh-token", headers={"refresh-token": invalid_token})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Could not validate credentials"
