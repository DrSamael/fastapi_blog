from fastapi import status, HTTPException
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from src.tests.fixtures import *


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


@patch("src.auth.routers.validate_token")
async def test_refresh_token_successful(mock_validate_token, async_client, test_user):
    expires_delta = datetime.now(timezone.utc) + timedelta(minutes=float(15))
    mock_validate_token.return_value = {'exp': expires_delta, 'sub': test_user["_id"]}
    refresh_token = "valid_refresh_token"

    response = await async_client.get("/auth/refresh-token", headers={"refresh-token": refresh_token})

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert "access_token" in result
    assert "refresh_token" in result


async def test_refresh_token_blank(async_client, test_user):
    response = await async_client.get("/auth/refresh-token")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Refresh token missing"


@patch("src.auth.routers.validate_token")
async def test_refresh_token_invalid_user_id(mock_validate_token, async_client):
    expires_delta = datetime.now(timezone.utc) + timedelta(minutes=float(15))
    mock_validate_token.return_value = {'exp': expires_delta, 'sub': ObjectId()}
    refresh_token = "valid_refresh_token"

    response = await async_client.get("/auth/refresh-token", headers={"refresh-token": refresh_token})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Could not find user"


@patch("src.auth.routers.validate_token")
async def test_refresh_token_expired(mock_validate_token, async_client):
    expired_token = "expired_refresh_token"
    mock_validate_token.side_effect = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    response = await async_client.get("/auth/refresh-token", headers={"refresh-token": expired_token})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Token expired"


@patch("src.auth.routers.validate_token")
async def test_refresh_token_invalid(mock_validate_token, async_client):
    invalid_token = "invalid_refresh_token"
    mock_validate_token.side_effect = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                                    detail="Could not validate credentials")

    response = await async_client.get("/auth/refresh-token", headers={"refresh-token": invalid_token})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Could not validate credentials"
