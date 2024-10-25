import pytest
from fastapi import HTTPException, status

from auth.utils import create_token
from tests.fixtures import *


@pytest.mark.asyncio
async def test_get_current_user_success(test_user):
    token = await create_token(test_user['_id'], None, 'access_token')
    result = await get_current_user(token)

    assert result == test_user


@pytest.mark.asyncio
async def test_get_current_user_not_found(test_user):
    token = await create_token(ObjectId(), None, 'access_token')

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_current_user_expired_token(test_user):
    token = await create_token(test_user['_id'], -20, 'access_token')

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Token expired"


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user('invalid_token')

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Could not validate credentials"
