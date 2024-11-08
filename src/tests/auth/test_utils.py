from src.auth.utils import create_token, decode_access_token, decode_refresh_token
from src.tests.fixtures import *


async def test_decode_access_token(test_user):
    token = await create_token(test_user['_id'], None, 'access_token')
    result = await decode_access_token(token)

    assert result['sub'] == str(test_user['_id'])


async def test_decode_refresh_token(test_user):
    token = await create_token(test_user['_id'], None, 'refresh_token')
    result = await decode_refresh_token(token)

    assert result['sub'] == str(test_user['_id'])
