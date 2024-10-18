import os
import jwt
import dotenv
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Union, Any, Literal

dotenv.load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')
ALGORITHM = os.getenv('ALGORITHM')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
TokenType = Literal["access_token", "refresh_token"]


async def get_hashed_password(password: str):
    return password_context.hash(password)


async def verify_password(password: str, hashed_pass: str):
    return password_context.verify(password, hashed_pass)


async def create_token(subject: Union[str, Any], expires_delta: int = None, token_type: TokenType = None):
    secret_key, expire_minutes = await define_token_params(token_type)
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=float(expire_minutes))

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key, ALGORITHM)
    return encoded_jwt


async def define_token_params(token_type: TokenType = None):
    token_config = {
        'access_token': {
            'secret_key': JWT_SECRET_KEY,
            'expire_minutes': ACCESS_TOKEN_EXPIRE_MINUTES
        },
        'refresh_token': {
            'secret_key': JWT_REFRESH_SECRET_KEY,
            'expire_minutes': REFRESH_TOKEN_EXPIRE_MINUTES
        }
    }

    # if token_type not in token_config:
    #     raise ValueError(f"Invalid token_type: {token_type}")
    return token_config[token_type]['secret_key'], token_config[token_type]['expire_minutes']


async def decode_access_token(access_token):
    return jwt.decode(access_token, JWT_SECRET_KEY, ALGORITHM)


async def decode_refresh_token(refresh_token):
    return jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, ALGORITHM)


async def validate_token(token: str, token_type: TokenType):
    try:
        decode_token_function = {
            'access_token': decode_access_token,
            'refresh_token': decode_refresh_token
        }
        return await decode_token_function[token_type](token)

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
